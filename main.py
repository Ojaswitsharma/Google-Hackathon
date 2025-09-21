import os
import json
import tempfile
import subprocess
from google.cloud import storage
from google.cloud import functions_v1
import functions_framework

# Initialize Google Cloud Storage client
storage_client = storage.Client()

# Configuration
RAW_ASSETS_BUCKET = os.environ.get('RAW_ASSETS_BUCKET', 'your-raw-assets-bucket')
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'your-output-bucket')

@functions_framework.cloud_event
def merge_media_files(cloud_event):
    """
    Cloud Function triggered when a file is uploaded to the raw-assets bucket.
    Checks if all three files (video, audio, description) are present for a project ID,
    then merges them into a final video with embedded description.
    """
    try:
        # Extract file information from the Cloud Event
        data = cloud_event.data
        bucket_name = data['bucket']
        file_name = data['name']
        
        print(f"File uploaded: {file_name} in bucket: {bucket_name}")
        
        # Extract project ID from filename (assuming format: projectX_type.extension)
        if '_' not in file_name:
            print(f"Invalid filename format: {file_name}")
            return
            
        project_id = file_name.split('_')[0]
        print(f"Detected project ID: {project_id}")
        
        # Check if all required files are present
        required_files = check_required_files(bucket_name, project_id)
        
        if not required_files['all_present']:
            print(f"Not all files present for project {project_id}. Missing: {required_files['missing']}")
            return
            
        print(f"All files present for project {project_id}. Starting merge process...")
        
        # Download and merge files
        merge_result = merge_files(bucket_name, project_id, required_files['files'])
        
        if merge_result:
            print(f"Successfully merged files for project {project_id}")
        else:
            print(f"Failed to merge files for project {project_id}")
            
    except Exception as e:
        print(f"Error in merge_media_files: {str(e)}")
        raise


def check_required_files(bucket_name, project_id):
    """
    Check if all required files (video, audio, description) are present in the bucket
    for the given project ID.
    """
    bucket = storage_client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=project_id))
    
    files = {
        'video': None,
        'audio': None,
        'description': None
    }
    
    for blob in blobs:
        filename = blob.name
        if filename.startswith(f"{project_id}_"):
            if filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                files['video'] = filename
            elif filename.endswith(('.mp3', '.wav', '.aac', '.m4a')):
                files['audio'] = filename
            elif filename.endswith('.json'):
                files['description'] = filename
    
    missing = [key for key, value in files.items() if value is None]
    all_present = len(missing) == 0
    
    return {
        'all_present': all_present,
        'missing': missing,
        'files': files
    }


def merge_files(bucket_name, project_id, files):
    """
    Download the files and merge them using FFmpeg.
    Creates a video with the original video, merged audio, and description overlay.
    """
    bucket = storage_client.bucket(bucket_name)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Download files
            video_path = os.path.join(temp_dir, files['video'])
            audio_path = os.path.join(temp_dir, files['audio'])
            description_path = os.path.join(temp_dir, files['description'])
            
            print("Downloading files...")
            bucket.blob(files['video']).download_to_filename(video_path)
            bucket.blob(files['audio']).download_to_filename(audio_path)
            bucket.blob(files['description']).download_to_filename(description_path)
            
            # Read description
            with open(description_path, 'r', encoding='utf-8') as f:
                description_data = json.load(f)
            
            # Extract description text
            description_text = description_data.get('description', 'No description available')
            
            # Create subtitle file for description
            subtitle_path = os.path.join(temp_dir, f"{project_id}_subtitle.srt")
            create_subtitle_file(subtitle_path, description_text)
            
            # Output file path
            output_path = os.path.join(temp_dir, f"{project_id}_final.mp4")
            
            # FFmpeg command to merge video, audio, and add subtitle overlay
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', video_path,          # Input video
                '-i', audio_path,          # Input audio
                '-vf', f"subtitles={subtitle_path}:force_style='Fontsize=16,PrimaryColour=&Hffffff&,BackColour=&H80000000&,BorderStyle=3,Outline=1,Shadow=0,MarginV=50'",  # Add subtitle overlay
                '-c:v', 'libx264',         # Video codec
                '-c:a', 'aac',             # Audio codec
                '-map', '0:v:0',           # Map video from first input
                '-map', '1:a:0',           # Map audio from second input
                '-shortest',               # End when shortest stream ends
                '-y',                      # Overwrite output file
                output_path
            ]
            
            print(f"Running FFmpeg command: {' '.join(ffmpeg_cmd)}")
            
            # Run FFmpeg
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
            print("FFmpeg completed successfully")
            
            # Upload merged file to output bucket
            upload_result = upload_merged_file(output_path, project_id)
            
            return upload_result
            
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr}")
            return False
        except Exception as e:
            print(f"Error in merge_files: {str(e)}")
            return False


def create_subtitle_file(subtitle_path, description_text):
    """
    Create an SRT subtitle file with the description text.
    The subtitle will be displayed throughout the entire video duration.
    """
    # For simplicity, we'll show the description for the first 30 seconds
    # You can modify this to show different parts of the description at different times
    
    # Split long descriptions into chunks for better readability
    max_chars_per_line = 80
    max_lines = 2
    
    words = description_text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line + " " + word) <= max_chars_per_line:
            current_line += (" " + word) if current_line else word
        else:
            lines.append(current_line)
            current_line = word
            
    if current_line:
        lines.append(current_line)
    
    # Group lines into subtitle chunks
    subtitle_chunks = []
    for i in range(0, len(lines), max_lines):
        chunk = lines[i:i+max_lines]
        subtitle_chunks.append('\n'.join(chunk))
    
    # Create SRT content
    srt_content = ""
    duration_per_chunk = 10  # 10 seconds per chunk
    
    for i, chunk in enumerate(subtitle_chunks):
        start_time = i * duration_per_chunk
        end_time = (i + 1) * duration_per_chunk
        
        start_time_str = format_srt_time(start_time)
        end_time_str = format_srt_time(end_time)
        
        srt_content += f"{i + 1}\n"
        srt_content += f"{start_time_str} --> {end_time_str}\n"
        srt_content += f"{chunk}\n\n"
    
    # Write SRT file
    with open(subtitle_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)


def format_srt_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 1000)
    
    return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d},{milliseconds:03d}"


def upload_merged_file(file_path, project_id):
    """
    Upload the merged video file to the output bucket.
    """
    try:
        output_bucket = storage_client.bucket(OUTPUT_BUCKET)
        output_filename = f"{project_id}_final.mp4"
        
        blob = output_bucket.blob(output_filename)
        blob.upload_from_filename(file_path)
        
        print(f"Uploaded merged file: {output_filename} to bucket: {OUTPUT_BUCKET}")
        return True
        
    except Exception as e:
        print(f"Error uploading merged file: {str(e)}")
        return False


# For local testing
if __name__ == "__main__":
    print("Cloud Function for media file merging")
    print("This function is designed to run in Google Cloud Functions environment")
