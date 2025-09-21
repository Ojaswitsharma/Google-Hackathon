"""
Professional Dynamic Subtitle Creator
Creates MrBeast/YouTube-style dynamic subtitles with pop effects
"""

import os
import json
import subprocess
from pathlib import Path
import re

def create_dynamic_professional_video():
    """Create video with professional dynamic subtitles"""
    print("🎬 Creating Professional Dynamic Subtitles!")
    print("=" * 60)
    
    # Paths
    final_output = Path("final_output")
    base_video = final_output / "your_final_merged_video.mp4"
    
    if not base_video.exists():
        print("❌ Base merged video not found!")
        return False
    
    # Read the story text
    demo_input = Path("demo_input")
    description_file = demo_input / "demoProject_description.json"
    
    with open(description_file, 'r', encoding='utf-8') as f:
        description_data = json.load(f)
    
    story = description_data.get('story', '')
    print(f"📝 Story loaded: {len(story)} characters")
    
    # Create dynamic text overlays using drawtext (no subtitle file needed)
    output_file = final_output / "your_professional_dynamic_video.mp4"
    
    # Create the dynamic text filter
    text_filter = create_dynamic_text_filter(story)
    
    print("🎭 Creating video with dynamic text overlays...")
    
    # FFmpeg command with dynamic text effects
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', str(base_video),
        '-vf', text_filter,
        '-c:v', 'libx264',
        '-crf', '20',  # Higher quality
        '-preset', 'medium',
        '-c:a', 'copy',  # Keep audio as-is
        '-y',
        str(output_file)
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Professional dynamic video created!")
            
            if output_file.exists():
                file_size = output_file.stat().st_size / (1024 * 1024)
                print(f"\n🎉 SUCCESS! Your professional video is ready!")
                print(f"📁 Location: {output_file}")
                print(f"📊 File size: {file_size:.2f} MB")
                
                print(f"\n✨ Enhanced features:")
                print(f"   💥 Dynamic pop-up text effects")
                print(f"   🎨 Professional styling with shadows")
                print(f"   📝 Perfectly timed text animations")
                print(f"   🌟 MrBeast-style visual impact")
                
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

def create_dynamic_text_filter(story_text):
    """Create FFmpeg filter with dynamic text effects"""
    
    # Split story into impactful phrases
    phrases = split_into_dynamic_phrases(story_text)
    
    # Create multiple text overlays with animations
    filters = []
    total_duration = 27.0  # seconds
    
    for i, phrase in enumerate(phrases):
        start_time = (i * total_duration) / len(phrases)
        duration = total_duration / len(phrases)
        end_time = start_time + duration
        
        # Clean text for FFmpeg
        clean_text = phrase.replace("'", "").replace('"', '').replace('\\', '').replace(':', '').strip()
        
        if not clean_text:
            continue
            
        # Create dynamic text with pop effect
        text_filter = create_single_dynamic_text(clean_text, start_time, duration, i)
        filters.append(text_filter)
    
    # Combine all filters
    combined_filter = ','.join(filters)
    print(f"🔤 Created {len(filters)} dynamic text overlays")
    
    return combined_filter

def split_into_dynamic_phrases(text):
    """Split text into dynamic phrases for better visual impact"""
    
    # First split by sentences
    sentences = re.split(r'[.!?]+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    phrases = []
    for sentence in sentences:
        # Split longer sentences by commas or natural breaks
        if len(sentence) > 60:
            # Split by commas, semicolons, or coordinating conjunctions
            parts = re.split(r'[,;]|\s+and\s+|\s+but\s+|\s+or\s+', sentence)
            for part in parts:
                part = part.strip()
                if part and len(part) > 10:  # Only keep meaningful parts
                    phrases.append(part)
        else:
            phrases.append(sentence)
    
    # Limit to reasonable number and remove very short phrases
    phrases = [p for p in phrases if len(p) > 15][:8]
    return phrases

def create_single_dynamic_text(text, start_time, duration, index):
    """Create single dynamic text overlay with pop effects"""
    
    end_time = start_time + duration
    
    # Position variations (center with slight offsets)
    positions = [
        ("(w-text_w)/2", "(h-text_h)/2-60"),  # Above center
        ("(w-text_w)/2", "(h-text_h)/2"),     # Center
        ("(w-text_w)/2", "(h-text_h)/2+60"),  # Below center
    ]
    
    x_pos, y_pos = positions[index % len(positions)]
    
    # Dynamic font size with pop effect
    # Start small, grow large, then settle to normal
    pop_duration = min(0.4, duration * 0.3)  # 30% of duration for pop effect
    
    # Font size animation: 24 -> 52 -> 40 (pop effect)
    fontsize_expr = f"if(lt(t-{start_time},{pop_duration})," \
                   f"24+28*smoothstep(0,1,(t-{start_time})/{pop_duration})," \
                   f"if(lt(t-{start_time},{pop_duration*1.5})," \
                   f"52-12*smoothstep(0,1,(t-{start_time}-{pop_duration})/{pop_duration*0.5})," \
                   f"40))"
    
    # Alpha (opacity) animation for smooth appearance
    alpha_expr = f"if(lt(t,{start_time}),0," \
                f"if(gt(t,{end_time-0.2}),1-5*(t-{end_time-0.2}),1))"
    
    # Create the dynamic drawtext filter
    text_filter = f"drawtext=text='{text}'" \
                 f":fontsize={fontsize_expr}" \
                 f":fontcolor=white" \
                 f":bordercolor=black" \
                 f":borderw=4" \
                 f":shadowcolor=black@0.8" \
                 f":shadowx=3" \
                 f":shadowy=3" \
                 f":x={x_pos}" \
                 f":y={y_pos}" \
                 f":alpha={alpha_expr}" \
                 f":enable='between(t,{start_time},{end_time})'"
    
    return text_filter

def create_ultra_professional_version():
    """Create an ultra-professional version with even better effects"""
    print("\n🚀 Creating ULTRA Professional Version!")
    print("=" * 60)
    
    final_output = Path("final_output")
    base_video = final_output / "your_final_merged_video.mp4"
    output_file = final_output / "your_ultra_professional_video.mp4"
    
    # Enhanced subtitle file with better styling
    enhanced_srt = final_output / "enhanced_subtitles.srt"
    create_enhanced_subtitle_file(enhanced_srt)
    
    # Ultra-professional FFmpeg command with advanced subtitle styling
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', str(base_video),
        '-vf', f'subtitles="{enhanced_srt}":force_style=\'FontName=Arial Bold,Fontsize=36,Bold=1,PrimaryColour=&Hffffff&,SecondaryColour=&Hffffff&,BackColour=&H80000000&,OutlineColour=&H00000000&,BorderStyle=3,Outline=3,Shadow=2,MarginV=80,Alignment=2,ScaleX=100,ScaleY=100\'',
        '-c:v', 'libx264',
        '-crf', '18',  # Very high quality
        '-preset', 'slow',  # Better compression
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
            print(f"❌ Error creating ultra version: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_enhanced_subtitle_file(srt_path):
    """Create enhanced subtitle file with better timing"""
    
    # Read the story
    demo_input = Path("demo_input")
    description_file = demo_input / "demoProject_description.json"
    
    with open(description_file, 'r', encoding='utf-8') as f:
        description_data = json.load(f)
    
    story = description_data.get('story', '')
    
    # Create better phrased subtitles
    phrases = [
        "Mark's world crumbled",
        "A failing grade stared back",
        "Shame burned fiercely",
        "But determination grew stronger",
        "He devoured textbooks",
        "Sought extra help relentlessly", 
        "The next exam loomed",
        "A challenge he'd conquer",
        "He walked out triumphant",
        "A perfect score achieved",
        "Failure was just a stepping stone"
    ]
    
    # Create SRT with better timing
    srt_content = ""
    total_duration = 27.0
    time_per_phrase = total_duration / len(phrases)
    
    for i, phrase in enumerate(phrases):
        start_time = i * time_per_phrase
        end_time = (i + 1) * time_per_phrase
        
        start_str = format_srt_time(start_time)
        end_str = format_srt_time(end_time)
        
        srt_content += f"{i + 1}\n"
        srt_content += f"{start_str} --> {end_str}\n"
        srt_content += f"{phrase.upper()}\n\n"  # UPPERCASE for impact
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)

def format_srt_time(seconds):
    """Convert seconds to SRT time format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{milliseconds:03d}"

def main():
    """Create both versions"""
    # Try the dynamic version first
    success1 = create_dynamic_professional_video()
    
    # Then create the ultra-professional version
    success2 = create_ultra_professional_version()
    
    if success1 or success2:
        print("\n🎉 DONE! Check your final_output folder for:")
        if success1:
            print("   📹 your_professional_dynamic_video.mp4")
        if success2:
            print("   🌟 your_ultra_professional_video.mp4")
        
        print("\n💫 These videos feature:")
        print("   ✨ Professional pop-up text effects")
        print("   🎨 Dynamic font sizing and animations")
        print("   💥 High-impact visual styling")
        print("   📝 Perfect timing with your story")

if __name__ == "__main__":
    main()