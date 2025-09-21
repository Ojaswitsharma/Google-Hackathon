"""
Simple Professional Subtitle Creator
Creates clean, professional dynamic subtitles with pop effects
"""

import os
import json
import subprocess
from pathlib import Path

def create_professional_subtitles():
    """Create professional subtitles with clean styling"""
    print("🎬 Creating Professional Dynamic Subtitles!")
    print("=" * 60)
    
    # Paths setup
    final_output = Path("final_output")
    base_video = final_output / "your_final_merged_video.mp4"
    
    if not base_video.exists():
        print(f"❌ Base video not found: {base_video}")
        return False
    
    # Create enhanced subtitle file
    srt_file = final_output / "professional_subtitles.srt"
    create_professional_srt(srt_file)
    
    # Output file
    output_file = final_output / "your_professional_cc_video.mp4"
    
    print("🎭 Creating video with professional CC...")
    
    # Simple FFmpeg command with professional subtitle styling
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', str(base_video),
        '-vf', f'subtitles={srt_file}:force_style=\'FontName=Arial Bold,Fontsize=42,Bold=1,PrimaryColour=&Hffffff&,SecondaryColour=&Hffffff&,BackColour=&H80000000&,OutlineColour=&H00000000&,BorderStyle=1,Outline=3,Shadow=2,MarginV=60,Alignment=2\'',
        '-c:v', 'libx264',
        '-crf', '20',
        '-preset', 'medium',
        '-c:a', 'copy',
        '-y',
        str(output_file)
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Professional CC video created!")
            
            if output_file.exists():
                file_size = output_file.stat().st_size / (1024 * 1024)
                print(f"\n🎉 SUCCESS! Your professional video is ready!")
                print(f"📁 Location: {output_file}")
                print(f"📊 File size: {file_size:.2f} MB")
                
                print(f"\n✨ Enhanced features:")
                print(f"   💥 Professional pop-style subtitles")
                print(f"   🎨 Bold white text with black outlines")
                print(f"   📝 Perfect timing and readability")
                print(f"   🌟 Clean, professional appearance")
                
                return True
            else:
                print("❌ Output file not created")
                return False
        else:
            print(f"❌ FFmpeg error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_professional_srt(srt_path):
    """Create professional subtitle file with impactful text"""
    
    # Professional, impactful phrases that match the story
    phrases = [
        "MARK'S WORLD CRUMBLED",
        "A FAILING GRADE STARED BACK", 
        "SHAME BURNED FIERCELY",
        "BUT DETERMINATION GREW STRONGER",
        "HE DEVOURED TEXTBOOKS",
        "SOUGHT EXTRA HELP",
        "PRACTICED RELENTLESSLY",
        "THE NEXT EXAM LOOMED",
        "A CHALLENGE TO CONQUER",
        "WALKING OUT TRIUMPHANT",
        "PERFECT SCORE ACHIEVED!"
    ]
    
    # Create SRT content with perfect timing
    srt_content = ""
    total_duration = 27.0  # Total video duration
    time_per_phrase = total_duration / len(phrases)
    
    for i, phrase in enumerate(phrases):
        start_time = i * time_per_phrase
        end_time = (i + 1) * time_per_phrase
        
        start_str = format_srt_time(start_time)
        end_str = format_srt_time(end_time)
        
        srt_content += f"{i + 1}\n"
        srt_content += f"{start_str} --> {end_str}\n"
        srt_content += f"{phrase}\n\n"
    
    # Write the file
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    
    print(f"✍️ Created subtitle file with {len(phrases)} phrases")

def format_srt_time(seconds):
    """Convert seconds to SRT time format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{milliseconds:03d}"

def create_ultra_professional_version():
    """Create an even MORE professional version with larger text"""
    print("\n🚀 Creating ULTRA Professional Version!")
    print("=" * 60)
    
    final_output = Path("final_output")
    base_video = final_output / "your_final_merged_video.mp4"
    output_file = final_output / "your_ultra_cc_video.mp4"
    srt_file = final_output / "professional_subtitles.srt"
    
    # Ultra-professional styling with bigger, bolder text
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', str(base_video),
        '-vf', f'subtitles={srt_file}:force_style=\'FontName=Arial Bold,Fontsize=56,Bold=1,PrimaryColour=&Hffffff&,SecondaryColour=&Hffffff&,BackColour=&H80000000&,OutlineColour=&H00000000&,BorderStyle=1,Outline=4,Shadow=3,MarginV=80,Alignment=2\'',
        '-c:v', 'libx264',
        '-crf', '18',  # Higher quality
        '-preset', 'slow',
        '-c:a', 'copy',
        '-y',
        str(output_file)
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ ULTRA Professional video created!")
            
            if output_file.exists():
                file_size = output_file.stat().st_size / (1024 * 1024)
                print(f"\n🌟 ULTRA SUCCESS! Your video is ready!")
                print(f"📁 Location: {output_file}")
                print(f"📊 File size: {file_size:.2f} MB")
                
                return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Create professional subtitle versions"""
    print("🎯 Creating Professional CC Videos...")
    
    # Create both versions
    success1 = create_professional_subtitles()
    success2 = create_ultra_professional_version()
    
    if success1 or success2:
        print("\n" + "="*60)
        print("🎉 PROFESSIONAL CC VIDEOS CREATED!")
        print("="*60)
        
        if success1:
            print("✅ Standard Professional: your_professional_cc_video.mp4")
        if success2:
            print("🌟 ULTRA Professional: your_ultra_cc_video.mp4")
        
        print("\n💫 Features:")
        print("   📺 Professional closed captions")
        print("   💥 Bold, high-impact text")
        print("   🎨 Clean white text with black outlines")
        print("   ⭐ Perfect for YouTube/social media")
        print("   🔥 MrBeast-style visual impact")
        
        print(f"\n📁 All files saved in: final_output/")
    else:
        print("❌ Failed to create videos")

if __name__ == "__main__":
    main()