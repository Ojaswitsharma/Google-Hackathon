"""
Simple Video Creator - Final Working Version
Creates your merged video with subtitles
"""

import os
import json
import subprocess
from pathlib import Path

def create_final_video():
    """Create the final video with subtitles"""
    print("🎬 Creating Your Final Video!")
    print("=" * 50)
    
    # Get absolute paths
    base_dir = Path("d:/Google-Hakathon")
    demo_input = base_dir / "demo_input"
    final_output = base_dir / "final_output"
    final_output.mkdir(exist_ok=True)
    
    # Input files
    video_file = demo_input / "demoProject_video.mp4"
    audio_file = demo_input / "demoProject_audio.mp3"
    description_file = demo_input / "demoProject_description.json"
    
    # Check files exist
    if not all(f.exists() for f in [video_file, audio_file, description_file]):
        print("❌ Demo files not found!")
        return False
    
    # Read description
    with open(description_file, 'r', encoding='utf-8') as f:
        description_data = json.load(f)
    
    story = description_data.get('story', 'No story found')
    print(f"📝 Story loaded: {len(story)} characters")
    
    # Create subtitle file
    subtitle_file = final_output / "story_subtitles.srt"
    create_story_subtitles(story, subtitle_file)
    print(f"📄 Created subtitles: {subtitle_file}")
    
    # Output file
    output_file = final_output / "your_final_merged_video.mp4"
    
    print("🔄 Merging video, audio, and subtitles...")
    
    # Single FFmpeg command to do everything
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', str(video_file),
        '-i', str(audio_file),
        '-vf', f'subtitles="{subtitle_file}":force_style=\'Fontsize=24,Bold=1,PrimaryColour=&Hffffff&,BackColour=&H80000000&,Outline=2,Shadow=1,MarginV=40\'',
        '-c:v', 'libx264',
        '-crf', '23',
        '-preset', 'fast',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-map', '0:v:0',  # Video from first input
        '-map', '1:a:0',  # Audio from second input
        '-shortest',
        '-y',
        str(output_file)
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Video created successfully!")
            
            if output_file.exists():
                file_size = output_file.stat().st_size / (1024 * 1024)
                print(f"\n🎉 SUCCESS! Your video is ready!")
                print(f"📁 Location: {output_file}")
                print(f"📊 File size: {file_size:.2f} MB")
                
                # Also create copies with simpler names
                copy_to_simple_names(video_file, audio_file, output_file, final_output)
                
                print(f"\n✨ Your video includes:")
                print(f"   🎬 Original video content")
                print(f"   🎵 Story audio track") 
                print(f"   📝 Story as subtitles")
                print(f"   🎨 Professional styling")
                
                return True
            else:
                print("❌ Output file not created")
                return False
        else:
            print(f"❌ FFmpeg failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_story_subtitles(story: str, subtitle_path: Path):
    """Create properly formatted subtitles"""
    import re
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', story.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    print(f"📝 Split story into {len(sentences)} sentences")
    
    # Create SRT content
    srt_content = ""
    total_duration = 27.0  # seconds
    time_per_sentence = total_duration / len(sentences)
    
    for i, sentence in enumerate(sentences):
        start_time = i * time_per_sentence
        end_time = (i + 1) * time_per_sentence
        
        start_str = format_srt_time(start_time)
        end_str = format_srt_time(end_time)
        
        srt_content += f"{i + 1}\n"
        srt_content += f"{start_str} --> {end_str}\n"
        srt_content += f"{sentence}\n\n"
    
    # Write file
    with open(subtitle_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)

def format_srt_time(seconds: float) -> str:
    """Convert seconds to SRT time format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{milliseconds:03d}"

def copy_to_simple_names(video_file: Path, audio_file: Path, output_file: Path, final_output: Path):
    """Copy files with simple names for easy access"""
    import shutil
    
    copies = [
        (video_file, final_output / "your_video.mp4"),
        (audio_file, final_output / "your_audio.mp3"),
        (final_output / "story_subtitles.srt", final_output / "your_story_subtitles.srt")
    ]
    
    for source, dest in copies:
        if source.exists() and not dest.exists():
            try:
                shutil.copy2(source, dest)
                print(f"📄 Created: {dest.name}")
            except Exception as e:
                print(f"⚠️  Could not copy {dest.name}: {e}")

def main():
    """Run the video creator"""
    return create_final_video()

if __name__ == "__main__":
    main()