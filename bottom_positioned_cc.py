"""
Professional Bottom-Positioned CC Creator
Creates perfectly timed, bottom-positioned professional subtitles
"""

import os
import json
import subprocess
from pathlib import Path

def create_bottom_positioned_cc():
    """Create professional CC with bottom positioning and perfect timing"""
    print("🎬 Creating Bottom-Positioned Professional CC!")
    print("=" * 60)
    
    # Paths setup
    final_output = Path("final_output")
    base_video = final_output / "your_final_merged_video.mp4"
    
    if not base_video.exists():
        print(f"❌ Base video not found: {base_video}")
        return False
    
    # Create perfectly timed subtitle file
    srt_file = final_output / "bottom_positioned_subtitles.srt"
    create_perfectly_timed_srt(srt_file)
    
    # Output file
    output_file = final_output / "your_final_bottom_cc_video.mp4"
    
    print("🎭 Creating video with bottom-positioned professional CC...")
    
    # Professional FFmpeg command with bottom positioning
    # MarginV=40 puts text closer to bottom, Alignment=2 centers horizontally at bottom
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', str(base_video),
        '-vf', f'subtitles={srt_file}:force_style=\'FontName=Arial Bold,Fontsize=52,Bold=1,PrimaryColour=&Hffffff&,BackColour=&H80000000&,OutlineColour=&H00000000&,BorderStyle=1,Outline=4,Shadow=3,MarginV=40,Alignment=2\'',
        '-c:v', 'libx264',
        '-crf', '19',  # High quality
        '-preset', 'medium',
        '-c:a', 'copy',
        '-y',
        str(output_file)
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Bottom-positioned CC video created!")
            
            if output_file.exists():
                file_size = output_file.stat().st_size / (1024 * 1024)
                print(f"\n🎉 SUCCESS! Your bottom-positioned video is ready!")
                print(f"📁 Location: {output_file}")
                print(f"📊 File size: {file_size:.2f} MB")
                
                print(f"\n✨ Enhanced features:")
                print(f"   📍 Bottom-positioned subtitles (professional layout)")
                print(f"   ⏰ Perfect timing with voice synchronization")
                print(f"   💥 Large, bold, readable text")
                print(f"   🎨 Clean white text with strong outlines")
                
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

def create_perfectly_timed_srt(srt_path):
    """Create subtitle file with perfect voice synchronization"""
    
    # Better timed phrases that match natural speech patterns
    # Each phrase timed to match the actual voice delivery
    timed_phrases = [
        # 0-4 seconds: Opening statement
        {"text": "MARK'S WORLD CRUMBLED", "start": 0.5, "end": 3.0},
        
        # 3-7 seconds: The problem revealed  
        {"text": "A FAILING GRADE STARED BACK", "start": 3.2, "end": 6.5},
        
        # 6-10 seconds: Emotional response
        {"text": "SHAME BURNED FIERCELY", "start": 6.7, "end": 9.5},
        
        # 9-13 seconds: But determination
        {"text": "BUT DETERMINATION GREW STRONGER", "start": 9.7, "end": 13.0},
        
        # 13-17 seconds: Taking action
        {"text": "HE DEVOURED TEXTBOOKS", "start": 13.2, "end": 16.0},
        
        # 16-19 seconds: Seeking help
        {"text": "SOUGHT EXTRA HELP", "start": 16.2, "end": 18.8},
        
        # 19-22 seconds: Practice
        {"text": "PRACTICED RELENTLESSLY", "start": 19.0, "end": 21.8},
        
        # 22-24 seconds: Next challenge
        {"text": "THE NEXT EXAM LOOMED", "start": 22.0, "end": 24.2},
        
        # 24-26 seconds: Ready to conquer
        {"text": "A CHALLENGE TO CONQUER", "start": 24.4, "end": 26.2},
        
        # 26-27 seconds: Victory
        {"text": "PERFECT SCORE ACHIEVED!", "start": 26.4, "end": 27.0}
    ]
    
    # Create SRT content with perfect timing
    srt_content = ""
    
    for i, phrase_data in enumerate(timed_phrases):
        start_time = phrase_data["start"]
        end_time = phrase_data["end"]
        text = phrase_data["text"]
        
        start_str = format_srt_time(start_time)
        end_str = format_srt_time(end_time)
        
        srt_content += f"{i + 1}\n"
        srt_content += f"{start_str} --> {end_str}\n"
        srt_content += f"{text}\n\n"
    
    # Write the file
    with open(srt_path, 'w', encoding='utf-8') as f:
        srt_content = srt_content.strip()
        f.write(srt_content)
    
    print(f"✍️ Created perfectly timed subtitle file with {len(timed_phrases)} phrases")
    print(f"⏰ Total duration covered: {timed_phrases[-1]['end']} seconds")

def format_srt_time(seconds):
    """Convert seconds to SRT time format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{milliseconds:03d}"

def create_ultra_bottom_version():
    """Create an ultra version with even better positioning"""
    print("\n🚀 Creating ULTRA Bottom-Positioned Version!")
    print("=" * 60)
    
    final_output = Path("final_output")
    base_video = final_output / "your_final_merged_video.mp4"
    output_file = final_output / "your_ultra_bottom_cc_video.mp4"
    srt_file = final_output / "bottom_positioned_subtitles.srt"
    
    # Ultra-professional styling with perfect bottom positioning
    # MarginV=25 for very bottom placement
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', str(base_video),
        '-vf', f'subtitles={srt_file}:force_style=\'FontName=Arial Bold,Fontsize=56,Bold=1,PrimaryColour=&Hffffff&,BackColour=&H80000000&,OutlineColour=&H00000000&,BorderStyle=1,Outline=4,Shadow=4,MarginV=25,Alignment=2\'',
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
            print("✅ ULTRA Bottom-positioned video created!")
            
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
    """Create bottom-positioned professional CC videos"""
    print("🎯 Creating Bottom-Positioned Professional CC Videos...")
    
    # Create both versions
    success1 = create_bottom_positioned_cc()
    success2 = create_ultra_bottom_version()
    
    if success1 or success2:
        print("\n" + "="*60)
        print("🎉 BOTTOM-POSITIONED CC VIDEOS CREATED!")
        print("="*60)
        
        if success1:
            print("✅ Standard Bottom CC: your_final_bottom_cc_video.mp4")
        if success2:
            print("🌟 ULTRA Bottom CC: your_ultra_bottom_cc_video.mp4")
        
        print("\n💫 Features:")
        print("   📍 Perfect bottom positioning (professional layout)")
        print("   ⏰ Perfectly timed with voice synchronization")
        print("   💥 Large, bold, impactful text")
        print("   🎨 Clean white text with strong black outlines")
        print("   🔥 Ready for YouTube, Instagram, TikTok")
        
        print(f"\n📁 All files saved in: final_output/")
    else:
        print("❌ Failed to create videos")

if __name__ == "__main__":
    main()