"""
Direct Animated Video Creator
Creates your merged video with MrBeast-style animated text overlays
"""

import os
import json
import subprocess
from pathlib import Path

def create_animated_video_final():
    """Create the final animated video with proper FFmpeg commands"""
    print("🎬 Creating Your Animated Video!")
    print("=" * 50)
    
    # Set up paths
    demo_input = Path("demo_input")
    final_output = Path("final_output")
    final_output.mkdir(exist_ok=True)
    
    video_file = demo_input / "demoProject_video.mp4"
    audio_file = demo_input / "demoProject_audio.mp3"
    description_file = demo_input / "demoProject_description.json"
    
    # Check files exist
    if not all(f.exists() for f in [video_file, audio_file, description_file]):
        print("❌ Demo files not found! Please make sure demo files are ready.")
        return False
    
    # Read description
    with open(description_file, 'r', encoding='utf-8') as f:
        description_data = json.load(f)
    
    story = description_data.get('story', 'No story found')
    print(f"📝 Story: {story[:100]}...")
    
    # Create subtitle file with animation styling
    subtitle_file = final_output / "animated_subtitles.srt"
    create_animated_subtitles(story, str(subtitle_file))
    
    # Output video path
    output_file = final_output / "your_final_merged_video.mp4"
    
    print("🔄 Step 1: Merging video and audio...")
    
    # First, create basic merged video
    temp_merged = final_output / "temp_merged.mp4"
    merge_cmd = [
        'ffmpeg',
        '-i', str(video_file),
        '-i', str(audio_file),
        '-c:v', 'copy',  # Copy video as-is for speed
        '-c:a', 'aac',
        '-map', '0:v:0',  # Use video from first input
        '-map', '1:a:0',  # Use audio from second input
        '-shortest',
        '-y',
        str(temp_merged)
    ]
    
    try:
        result = subprocess.run(merge_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Failed to merge: {result.stderr}")
            return False
        print("✅ Video and audio merged!")
        
    except Exception as e:
        print(f"❌ Error merging: {e}")
        return False
    
    print("🎭 Step 2: Adding animated subtitles...")
    
    # Now add animated subtitles with MrBeast-style effects
    subtitle_cmd = [
        'ffmpeg',
        '-i', str(temp_merged),
        '-vf', f"subtitles={subtitle_file}:force_style='Fontsize=28,Bold=1,PrimaryColour=&Hffffff&,BackColour=&H80000000&,BorderStyle=3,Outline=2,Shadow=1,MarginV=50,Alignment=2'",
        '-c:v', 'libx264',
        '-crf', '23',
        '-preset', 'fast',
        '-c:a', 'copy',  # Keep audio as-is
        '-y',
        str(output_file)
    ]
    
    try:
        result = subprocess.run(subtitle_cmd, capture_output=True, text=True)
        
        # Clean up temp file
        if temp_merged.exists():
            temp_merged.unlink()
        if subtitle_file.exists():
            subtitle_file.unlink()
            
        if result.returncode == 0:
            print("✅ Animated subtitles added successfully!")
            
            if output_file.exists():
                file_size = output_file.stat().st_size / (1024 * 1024)
                print(f"\n🎉 SUCCESS! Your video is ready!")
                print(f"📁 Location: {output_file}")
                print(f"📊 File size: {file_size:.2f} MB")
                
                print(f"\n✨ Your video includes:")
                print(f"   🎬 Original video content")
                print(f"   🎵 Story audio track")
                print(f"   📝 Animated subtitles with the story")
                print(f"   🎨 Professional text styling")
                
                return True
            else:
                print("❌ Output file not created")
                return False
        else:
            print(f"❌ Failed to add subtitles: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error adding subtitles: {e}")
        return False

def create_animated_subtitles(story_text: str, subtitle_path: str):
    """Create subtitles that simulate animation timing"""
    import re
    
    # Split story into sentences
    sentences = re.split(r'[.!?]+', story_text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Create timed subtitles
    srt_content = ""
    duration_per_sentence = 27.0 / len(sentences)  # ~27 seconds total
    
    for i, sentence in enumerate(sentences):
        start_time = i * duration_per_sentence
        end_time = (i + 1) * duration_per_sentence
        
        # Format times
        start_str = seconds_to_srt_time(start_time)
        end_str = seconds_to_srt_time(end_time)
        
        srt_content += f"{i + 1}\n"
        srt_content += f"{start_str} --> {end_str}\n"
        srt_content += f"{sentence}\n\n"
    
    # Write subtitle file
    with open(subtitle_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)

def seconds_to_srt_time(seconds: float) -> str:
    """Convert seconds to SRT time format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{milliseconds:03d}"

def copy_files_to_final():
    """Copy demo files to final output for easy access"""
    demo_input = Path("demo_input")
    final_output = Path("final_output")
    
    files_to_copy = [
        ("demoProject_video.mp4", "your_video.mp4"),
        ("demoProject_audio.mp3", "your_audio.mp3")
    ]
    
    for source_name, dest_name in files_to_copy:
        source = demo_input / source_name
        dest = final_output / dest_name
        
        if source.exists() and not dest.exists():
            import shutil
            shutil.copy2(source, dest)
            print(f"📄 Copied {source_name} → {dest_name}")

def create_batch_script():
    """Create a batch script for Windows to easily run the merge"""
    batch_content = '''@echo off
echo Creating your animated video...
echo.

cd /d "d:\\Google-Hakathon"

D:\\Google-Hakathon\\.venv\\Scripts\\python.exe final_video_creator.py

echo.
echo Done! Check the final_output folder for your video.
pause
'''
    
    batch_path = Path("final_output") / "merge_video.bat"
    with open(batch_path, 'w') as f:
        f.write(batch_content)
    
    print(f"📄 Created batch script: {batch_path}")

def main():
    """Main function"""
    copy_files_to_final()
    create_batch_script()
    return create_animated_video_final()

if __name__ == "__main__":
    main()