"""
Local demo script to test the media merging functionality
using the demo files in the public folder.
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

def setup_demo_files():
    """Setup demo files with proper naming convention"""
    print("Setting up demo files...")
    
    project_id = "demoProject"
    public_dir = Path("public")
    demo_dir = Path("demo_input")
    demo_dir.mkdir(exist_ok=True)
    
    # Copy and rename files
    files_mapping = {
        "WhatsApp Video 2025-09-08 at 19.05.09_c9fea5bf.mp4": f"{project_id}_video.mp4",
        "story_1757334136.mp3": f"{project_id}_audio.mp3",
        "disc.json": f"{project_id}_description.json"
    }
    
    for original, new_name in files_mapping.items():
        original_path = public_dir / original
        new_path = demo_dir / new_name
        
        if original_path.exists():
            shutil.copy2(original_path, new_path)
            print(f"Copied {original} -> {new_name}")
        else:
            print(f"Warning: {original} not found!")
    
    return project_id, demo_dir

def merge_demo_files(project_id, demo_dir):
    """Merge the demo files using FFmpeg"""
    print(f"\nStarting merge process for {project_id}...")
    
    # File paths
    video_path = demo_dir / f"{project_id}_video.mp4"
    audio_path = demo_dir / f"{project_id}_audio.mp3"
    description_path = demo_dir / f"{project_id}_description.json"
    
    # Check if all files exist
    if not all(f.exists() for f in [video_path, audio_path, description_path]):
        print("Error: Not all required files are present!")
        return False
    
    # Read description
    with open(description_path, 'r', encoding='utf-8') as f:
        description_data = json.load(f)
    
    # Extract description text (handle both "story" and "description" keys)
    description_text = description_data.get('story') or description_data.get('description', 'No description available')
    print(f"Description: {description_text[:100]}...")
    
    # Create subtitle file
    subtitle_path = demo_dir / f"{project_id}_subtitle.srt"
    create_subtitle_file(subtitle_path, description_text)
    print(f"Created subtitle file: {subtitle_path}")
    
    # Output file path
    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{project_id}_final.mp4"
    
    # FFmpeg command to merge video, audio, and add subtitle overlay
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', str(video_path),          # Input video
        '-i', str(audio_path),          # Input audio
        '-vf', f"subtitles={subtitle_path}:force_style='Fontsize=20,PrimaryColour=&Hffffff&,BackColour=&H80000000&,BorderStyle=3,Outline=2,Shadow=1,MarginV=30'",  # Add subtitle overlay
        '-c:v', 'libx264',              # Video codec
        '-c:a', 'aac',                  # Audio codec
        '-map', '0:v:0',                # Map video from first input
        '-map', '1:a:0',                # Map audio from second input
        '-shortest',                    # End when shortest stream ends
        '-y',                           # Overwrite output file
        str(output_path)
    ]
    
    print(f"Running FFmpeg command...")
    print(" ".join(ffmpeg_cmd))
    
    try:
        # Run FFmpeg
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
        print("\n✅ FFmpeg completed successfully!")
        print(f"Output file created: {output_path}")
        
        # Check if output file exists and get its size
        if output_path.exists():
            file_size = output_path.stat().st_size / (1024 * 1024)  # Size in MB
            print(f"Output file size: {file_size:.2f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ FFmpeg error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("\n❌ FFmpeg not found! Please install FFmpeg first.")
        print("Download from: https://ffmpeg.org/download.html")
        return False

def main():
    """Run the demo"""
    print("🎬 Media Merger Demo")
    print("=" * 50)
    
    # Setup demo files
    project_id, demo_dir = setup_demo_files()
    
    # Merge files
    success = merge_demo_files(project_id, demo_dir)
    
    if success:
        print("\n🎉 Demo completed successfully!")
        print(f"Check the 'demo_output' folder for {project_id}_final.mp4")
        print("\nThe final video should contain:")
        print("- Original video content")
        print("- Audio from the MP3 file")
        print("- Description text as subtitles overlay")
    else:
        print("\n❌ Demo failed!")
        print("Make sure FFmpeg is installed and accessible from command line")

if __name__ == "__main__":
    main()
