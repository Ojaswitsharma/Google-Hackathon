"""
Enhanced Media Merger with Animated Text Overlays
Integrates MrBeast-style text animations into video merging
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from animated_text_overlay import MrBeastStyleTextGenerator

def get_audio_duration(audio_path: str) -> float:
    """Get audio duration using FFprobe"""
    try:
        cmd = [
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(audio_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
        
    except (subprocess.CalledProcessError, ValueError):
        print("⚠️  Could not detect audio duration, using 30 seconds default")
        return 30.0

def create_animated_video_with_text(video_path: str, audio_path: str, 
                                  description_text: str, output_path: str) -> bool:
    """
    Create video with animated text overlays using MrBeast-style effects
    """
    print("🎬 Creating animated video with text overlays...")
    
    # Get audio duration for proper timing
    audio_duration = get_audio_duration(audio_path)
    print(f"📏 Audio duration: {audio_duration:.2f} seconds")
    
    # Generate animated text filter
    text_generator = MrBeastStyleTextGenerator()
    text_filter = text_generator.generate_ffmpeg_animated_filter(description_text, audio_duration)
    
    print("🔤 Generated animated text filter")
    
    # Create FFmpeg command with animated text overlay
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', video_path,                    # Input video
        '-i', audio_path,                    # Input audio
        '-filter_complex', f'{text_filter};[v][1:a]concat=n=1:v=1:a=1[outv][outa]',  # Text overlay filter
        '-map', '[outv]',                    # Map processed video
        '-map', '[outa]',                    # Map audio
        '-c:v', 'libx264',                   # Video codec
        '-c:a', 'aac',                       # Audio codec
        '-b:a', '128k',                      # Audio bitrate
        '-shortest',                         # End when shortest stream ends
        '-y',                                # Overwrite output file
        output_path
    ]
    
    print("🎭 Running FFmpeg with animated text overlays...")
    
    try:
        # Run FFmpeg command
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Video created successfully with animated text!")
            return True
        else:
            print(f"❌ FFmpeg error (exit code {result.returncode}):")
            print("STDERR:", result.stderr[-500:])  # Show last 500 chars of error
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg not found! Please ensure FFmpeg is installed.")
        return False
    except Exception as e:
        print(f"❌ Error creating animated video: {e}")
        return False

def process_demo_with_animations():
    """Process the demo files with animated text overlays"""
    print("🚀 Processing Demo with MrBeast-Style Animations")
    print("=" * 60)
    
    # Paths
    demo_input = Path("demo_input")
    final_output = Path("final_output")
    final_output.mkdir(exist_ok=True)
    
    # Find demo files
    video_file = demo_input / "demoProject_video.mp4"
    audio_file = demo_input / "demoProject_audio.mp3"
    description_file = demo_input / "demoProject_description.json"
    
    # Check if files exist
    if not all(f.exists() for f in [video_file, audio_file, description_file]):
        print("❌ Demo files not found! Run demo.py first to set up files.")
        return False
    
    # Read description
    with open(description_file, 'r', encoding='utf-8') as f:
        description_data = json.load(f)
    
    description_text = description_data.get('story') or description_data.get('description', 'No description')
    print(f"📝 Description: {description_text[:100]}...")
    
    # Output file
    output_file = final_output / "demoProject_animated_final.mp4"
    
    # Create animated video
    success = create_animated_video_with_text(
        str(video_file),
        str(audio_file),
        description_text,
        str(output_file)
    )
    
    if success:
        print(f"\n🎉 SUCCESS! Animated video created:")
        print(f"📁 Location: {output_file}")
        
        # Get file size
        if output_file.exists():
            file_size = output_file.stat().st_size / (1024 * 1024)  # MB
            print(f"📊 File size: {file_size:.2f} MB")
            
        print(f"\n✨ Features included:")
        print(f"   🎬 Original video content")
        print(f"   🎵 Synchronized audio track")
        print(f"   🔤 Animated text overlays (70% → 120% → 100% scale)")
        print(f"   ⏱️  Text synchronized with audio timing")
        print(f"   🎨 MrBeast-style text effects")
        
    return success

if __name__ == "__main__":
    process_demo_with_animations()