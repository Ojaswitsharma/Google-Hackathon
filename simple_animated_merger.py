"""
Simplified Animated Text System that works reliably with FFmpeg
Creates MrBeast-style text pop-ups with proper scaling animation
"""

import os
import json
import subprocess
from pathlib import Path

def create_simple_animated_video(video_path: str, audio_path: str, 
                                description_text: str, output_path: str) -> bool:
    """
    Create video with simple but effective animated text overlays
    """
    print("🎬 Creating video with animated text overlays...")
    
    # Split description into key phrases
    phrases = split_text_into_phrases(description_text)
    
    # Get audio duration
    audio_duration = get_audio_duration(audio_path)
    print(f"📏 Audio duration: {audio_duration:.2f} seconds")
    
    # Calculate timing for each phrase
    time_per_phrase = audio_duration / len(phrases)
    
    # Create animated drawtext filters
    filters = []
    for i, phrase in enumerate(phrases):
        start_time = i * time_per_phrase
        duration = time_per_phrase
        
        # Clean the text for FFmpeg
        clean_text = phrase.replace("'", "").replace('"', '').replace('\\', '')
        
        # Create animated text filter with scale effect
        filter_str = create_animated_drawtext(clean_text, start_time, duration, i)
        filters.append(filter_str)
    
    # Combine all filters
    video_filter = '[0:v]' + ','.join(filters) + '[v]'
    
    print(f"🔤 Created {len(filters)} animated text overlays")
    
    # FFmpeg command
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-filter_complex', f'{video_filter};[v][1:a]concat=n=1:v=1:a=1[outv][outa]',
        '-map', '[outv]',
        '-map', '[outa]',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'fast',
        '-crf', '23',
        '-y',
        output_path
    ]
    
    print("🎭 Running FFmpeg...")
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Animated video created successfully!")
            return True
        else:
            print(f"❌ FFmpeg error: {result.stderr}")
            
            # Try simpler approach without complex filters
            return create_basic_video_with_subtitles(video_path, audio_path, 
                                                   description_text, output_path)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return create_basic_video_with_subtitles(video_path, audio_path, 
                                               description_text, output_path)

def create_animated_drawtext(text: str, start_time: float, duration: float, index: int) -> str:
    """
    Create a single animated drawtext filter
    """
    end_time = start_time + duration
    
    # Position (center with slight offset)
    y_offset = (index % 3) * 40 - 40  # -40, 0, 40
    
    # Simple scale animation using fontsize
    # Start small, grow big, then normal
    scale_duration = min(0.3, duration * 0.3)  # 30% of duration for scaling
    
    fontsize_expr = f"if(lt(t,{start_time + scale_duration})," \
                   f"35+25*(t-{start_time})/{scale_duration}," \
                   f"if(gt(t,{end_time - scale_duration})," \
                   f"60-10*(t-{end_time - scale_duration})/{scale_duration}," \
                   f"60))"
    
    return f"drawtext=text='{text}'" \
           f":fontsize={fontsize_expr}" \
           f":fontcolor=white" \
           f":bordercolor=black" \
           f":borderw=3" \
           f":x=(w-text_w)/2" \
           f":y=(h-text_h)/2{'+' + str(y_offset) if y_offset >= 0 else str(y_offset)}" \
           f":enable='between(t,{start_time},{end_time})'"

def create_basic_video_with_subtitles(video_path: str, audio_path: str, 
                                    description_text: str, output_path: str) -> bool:
    """
    Fallback: Create video with basic subtitle overlay
    """
    print("🔄 Creating basic video with subtitles...")
    
    # Create subtitle file
    srt_path = Path(output_path).parent / "temp_subtitles.srt"
    create_basic_srt(description_text, str(srt_path), get_audio_duration(audio_path))
    
    # Simple FFmpeg command with subtitle overlay
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-vf', f"subtitles={srt_path}:force_style='Fontsize=24,PrimaryColour=&Hffffff&,BackColour=&H80000000&'",
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        '-y',
        output_path
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        # Clean up temp file
        if srt_path.exists():
            srt_path.unlink()
            
        if result.returncode == 0:
            print("✅ Basic video with subtitles created!")
            return True
        else:
            print(f"❌ Failed to create video: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating basic video: {e}")
        return False

def split_text_into_phrases(text: str) -> list:
    """Split text into meaningful phrases for animation"""
    import re
    
    # Split by sentences first
    sentences = re.split(r'[.!?]+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    phrases = []
    for sentence in sentences:
        # Split long sentences by commas or natural breaks
        if len(sentence) > 80:
            parts = re.split(r'[,;]+', sentence)
            phrases.extend([p.strip() for p in parts if p.strip()])
        else:
            phrases.append(sentence)
    
    return phrases[:8]  # Limit to 8 phrases max

def create_basic_srt(text: str, srt_path: str, duration: float):
    """Create a basic SRT subtitle file"""
    phrases = split_text_into_phrases(text)
    time_per_phrase = duration / len(phrases)
    
    srt_content = ""
    for i, phrase in enumerate(phrases):
        start_time = i * time_per_phrase
        end_time = (i + 1) * time_per_phrase
        
        start_str = seconds_to_srt_time(start_time)
        end_str = seconds_to_srt_time(end_time)
        
        srt_content += f"{i + 1}\n"
        srt_content += f"{start_str} --> {end_str}\n"
        srt_content += f"{phrase}\n\n"
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)

def seconds_to_srt_time(seconds: float) -> str:
    """Convert seconds to SRT time format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{milliseconds:03d}"

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

def main():
    """Process demo with animated text"""
    print("🚀 Creating MrBeast-Style Animated Video")
    print("=" * 50)
    
    # Paths
    demo_input = Path("demo_input")
    final_output = Path("final_output")
    final_output.mkdir(exist_ok=True)
    
    video_file = demo_input / "demoProject_video.mp4"
    audio_file = demo_input / "demoProject_audio.mp3"
    description_file = demo_input / "demoProject_description.json"
    output_file = final_output / "demoProject_animated_final.mp4"
    
    # Check files
    if not all(f.exists() for f in [video_file, audio_file, description_file]):
        print("❌ Demo files not found!")
        return False
    
    # Read description
    with open(description_file, 'r', encoding='utf-8') as f:
        description_data = json.load(f)
    
    description_text = description_data.get('story') or description_data.get('description', 'No description')
    
    # Create animated video
    success = create_simple_animated_video(
        str(video_file),
        str(audio_file),
        description_text,
        str(output_file)
    )
    
    if success:
        print(f"\n🎉 SUCCESS! Your animated video is ready!")
        print(f"📁 Location: {output_file}")
        
        if output_file.exists():
            file_size = output_file.stat().st_size / (1024 * 1024)
            print(f"📊 File size: {file_size:.2f} MB")
    
    return success

if __name__ == "__main__":
    main()