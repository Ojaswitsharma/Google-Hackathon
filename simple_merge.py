"""
Simple media merger without FFmpeg dependency.
This creates a basic combination and shows you exactly what files you have.
"""

import json
import shutil
from pathlib import Path

def create_simple_merge():
    """Create a simple demonstration of what we have"""
    print("🎬 Creating Simple Media Merge Demo")
    print("=" * 50)
    
    # Input files from public folder
    public_dir = Path("public")
    output_dir = Path("final_output")
    output_dir.mkdir(exist_ok=True)
    
    # Your files
    video_file = public_dir / "WhatsApp Video 2025-09-08 at 19.05.09_c9fea5bf.mp4"
    audio_file = public_dir / "story_1757334136.mp3" 
    desc_file = public_dir / "disc.json"
    
    print("📁 Your Input Files:")
    for file_path in [video_file, audio_file, desc_file]:
        if file_path.exists():
            size = file_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ {file_path.name} ({size:.2f} MB)")
        else:
            print(f"   ❌ {file_path.name} (NOT FOUND)")
    
    # Read and display the story
    if desc_file.exists():
        with open(desc_file, 'r') as f:
            story_data = json.load(f)
        story = story_data.get('story', 'No story found')
        print(f"\n📝 Your Story:")
        print(f"   {story}")
        
        # Create a detailed subtitle file
        subtitle_content = create_detailed_subtitles(story)
        subtitle_file = output_dir / "your_story_subtitles.srt"
        with open(subtitle_file, 'w', encoding='utf-8') as f:
            f.write(subtitle_content)
        print(f"\n📄 Created subtitle file: {subtitle_file}")
    
    # Copy files to output with better names
    if video_file.exists():
        shutil.copy2(video_file, output_dir / "your_video.mp4")
        print(f"✅ Copied video to: {output_dir / 'your_video.mp4'}")
    
    if audio_file.exists():
        shutil.copy2(audio_file, output_dir / "your_audio.mp3")
        print(f"✅ Copied audio to: {output_dir / 'your_audio.mp3'}")
    
    # Create the FFmpeg command for manual execution
    create_ffmpeg_command_file(output_dir)
    
    print(f"\n🎯 What's in your final_output folder:")
    for file in output_dir.iterdir():
        if file.is_file():
            size = file.stat().st_size / (1024 * 1024)
            print(f"   📄 {file.name} ({size:.2f} MB)")

def create_detailed_subtitles(story_text):
    """Create a detailed subtitle file"""
    # Split story into sentences
    sentences = [s.strip() + '.' for s in story_text.split('.') if s.strip()]
    
    subtitle_content = ""
    time_per_sentence = 4  # 4 seconds per sentence
    
    for i, sentence in enumerate(sentences):
        start_time = i * time_per_sentence
        end_time = (i + 1) * time_per_sentence
        
        start_str = format_srt_time(start_time)
        end_str = format_srt_time(end_time)
        
        subtitle_content += f"{i + 1}\n"
        subtitle_content += f"{start_str} --> {end_str}\n"
        subtitle_content += f"{sentence}\n\n"
    
    return subtitle_content

def format_srt_time(seconds):
    """Convert seconds to SRT time format"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d},000"

def create_ffmpeg_command_file(output_dir):
    """Create a batch file with the FFmpeg command for manual execution"""
    ffmpeg_command = f"""@echo off
echo Starting video merge...

ffmpeg -i your_video.mp4 -i your_audio.mp3 -vf "subtitles=your_story_subtitles.srt:force_style='Fontsize=24,PrimaryColour=&Hffffff&,BackColour=&H80000000&,BorderStyle=3,Outline=2,Shadow=1,MarginV=40,Alignment=2'" -c:v libx264 -c:a aac -map 0:v:0 -map 1:a:0 -shortest -y your_final_merged_video.mp4

echo Done! Check your_final_merged_video.mp4
pause
"""
    
    batch_file = output_dir / "merge_video.bat"
    with open(batch_file, 'w') as f:
        f.write(ffmpeg_command)
    
    print(f"📝 Created FFmpeg command file: {batch_file}")
    print(f"   To use: Install FFmpeg, then double-click this file")

if __name__ == "__main__":
    create_simple_merge()
