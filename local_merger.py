"""
Local version of the media merger for testing without Google Cloud.
This simulates the Cloud Function behavior using local files.
"""

import os
import json
import shutil
import tempfile
import subprocess
from pathlib import Path

def format_srt_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 1000)
    
    return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d},{milliseconds:03d}"

def create_subtitle_file(subtitle_path, description_text):
    """Create an SRT subtitle file with the description text."""
    # Split long descriptions into chunks for better readability
    max_chars_per_line = 60  # Reduced for better readability
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
    
    # Create SRT content - show each chunk for longer duration
    srt_content = ""
    duration_per_chunk = 8  # 8 seconds per chunk
    
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

def check_required_files_local(input_dir, project_id):
    """Check if all required files are present locally"""
    input_path = Path(input_dir)
    
    files = {
        'video': None,
        'audio': None,
        'description': None
    }
    
    # Look for files with the project_id prefix
    for file_path in input_path.glob(f"{project_id}_*"):
        filename = file_path.name
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

def merge_files_local(input_dir, output_dir, project_id):
    """Merge files locally using FFmpeg"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Check for required files
    file_check = check_required_files_local(input_dir, project_id)
    if not file_check['all_present']:
        print(f"❌ Missing files: {file_check['missing']}")
        return False
    
    files = file_check['files']
    
    # File paths
    video_path = input_path / files['video']
    audio_path = input_path / files['audio']
    description_path = input_path / files['description']
    
    print(f"📹 Video: {video_path}")
    print(f"🎵 Audio: {audio_path}")
    print(f"📝 Description: {description_path}")
    
    try:
        # Read description
        with open(description_path, 'r', encoding='utf-8') as f:
            description_data = json.load(f)
        
        # Extract description text (handle both "story" and "description" keys)
        description_text = description_data.get('story') or description_data.get('description', 'No description available')
        print(f"📄 Description text: {description_text[:100]}...")
        
        # Create subtitle file
        subtitle_path = input_path / f"{project_id}_subtitle.srt"
        create_subtitle_file(subtitle_path, description_text)
        print(f"📄 Created subtitle file: {subtitle_path}")
        
        # Output file path
        output_file = output_path / f"{project_id}_final.mp4"
        
        # FFmpeg command with improved subtitle styling
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', str(video_path),          # Input video
            '-i', str(audio_path),          # Input audio
            '-vf', f"subtitles={subtitle_path}:force_style='Fontsize=24,PrimaryColour=&Hffffff&,BackColour=&H80000000&,BorderStyle=3,Outline=2,Shadow=1,MarginV=40,Alignment=2'",  # Centered subtitles
            '-c:v', 'libx264',              # Video codec
            '-c:a', 'aac',                  # Audio codec
            '-b:a', '128k',                 # Audio bitrate
            '-map', '0:v:0',                # Map video from first input
            '-map', '1:a:0',                # Map audio from second input (replace original audio)
            '-shortest',                    # End when shortest stream ends
            '-y',                           # Overwrite output file
            str(output_file)
        ]
        
        print(f"\n🔄 Running FFmpeg...")
        print("Command:", " ".join(ffmpeg_cmd))
        
        # Run FFmpeg
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("\n✅ FFmpeg completed successfully!")
            
            # Check output file
            if output_file.exists():
                file_size = output_file.stat().st_size / (1024 * 1024)  # Size in MB
                print(f"📁 Output file: {output_file}")
                print(f"📊 File size: {file_size:.2f} MB")
                return True
            else:
                print("❌ Output file was not created!")
                return False
        else:
            print(f"\n❌ FFmpeg error (exit code {result.returncode}):")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except FileNotFoundError as e:
        if "ffmpeg" in str(e).lower():
            print("\n❌ FFmpeg not found!")
            print("Please install FFmpeg:")
            print("- Windows: Download from https://ffmpeg.org/download.html")
            print("- Or use: choco install ffmpeg (if you have Chocolatey)")
            print("- Or use: scoop install ffmpeg (if you have Scoop)")
        else:
            print(f"❌ File not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function to run local merging"""
    print("🎬 Local Media Merger")
    print("=" * 50)
    
    # Use demo files if available, otherwise use current directory
    input_dir = "demo_input" if Path("demo_input").exists() else "public"
    output_dir = "demo_output"
    
    print(f"📂 Input directory: {input_dir}")
    print(f"📂 Output directory: {output_dir}")
    
    # Find project IDs in the input directory
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"❌ Input directory '{input_dir}' not found!")
        return
    
    # Look for files with project IDs
    project_ids = set()
    for file_path in input_path.iterdir():
        if file_path.is_file() and '_' in file_path.stem:
            project_id = file_path.stem.split('_')[0]
            project_ids.add(project_id)
    
    if not project_ids:
        print("❌ No project files found!")
        print("Files should be named like: projectX_video.mp4, projectX_audio.mp3, projectX_description.json")
        return
    
    print(f"🔍 Found project IDs: {list(project_ids)}")
    
    # Process each project
    for project_id in project_ids:
        print(f"\n🚀 Processing project: {project_id}")
        success = merge_files_local(input_dir, output_dir, project_id)
        
        if success:
            print(f"✅ Successfully merged {project_id}")
        else:
            print(f"❌ Failed to merge {project_id}")

if __name__ == "__main__":
    main()
