"""
Animated Text Overlay System for Video Merging
Creates MrBeast-style text animations with scale effects
"""

import os
import json
import re
import math
from pathlib import Path
from typing import List, Dict, Tuple

class AnimatedTextOverlay:
    def __init__(self, framerate: float = 30.0):
        self.framerate = framerate
        self.frame_duration = 1.0 / framerate
        
    def create_text_timing(self, text: str, audio_duration: float) -> List[Dict]:
        """
        Parse text and create timing for animated overlays
        """
        # Split text into sentences for better pacing
        sentences = re.split(r'[.!?]+', text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Calculate timing per sentence
        time_per_sentence = audio_duration / len(sentences)
        
        text_segments = []
        current_time = 0.0
        
        for i, sentence in enumerate(sentences):
            # Split sentence into key phrases (for multiple text pops)
            words = sentence.split()
            
            # Group words into phrases (3-5 words per phrase)
            phrases = []
            current_phrase = []
            
            for word in words:
                current_phrase.append(word)
                if len(current_phrase) >= 4 or word in ['and', 'but', 'or', 'so']:
                    phrases.append(' '.join(current_phrase))
                    current_phrase = []
            
            if current_phrase:
                phrases.append(' '.join(current_phrase))
            
            # If only one phrase, use the whole sentence
            if len(phrases) == 1:
                phrases = [sentence]
            
            # Calculate timing for each phrase
            phrase_duration = time_per_sentence / len(phrases)
            
            for phrase in phrases:
                text_segments.append({
                    'text': phrase,
                    'start_time': current_time,
                    'duration': phrase_duration,
                    'end_time': current_time + phrase_duration
                })
                current_time += phrase_duration
        
        return text_segments
    
    def generate_scale_animation_filter(self, text_segments: List[Dict]) -> str:
        """
        Generate FFmpeg drawtext filter with scale animations
        """
        filters = []
        
        for i, segment in enumerate(text_segments):
            start_time = segment['start_time']
            duration = segment['duration']
            text = segment['text'].replace("'", "\\'").replace('"', '\\"')
            
            # Animation timing (in seconds)
            scale_up_duration = 3 / self.framerate  # 3 frames
            scale_down_duration = 3 / self.framerate  # 3 frames
            stable_duration = duration - scale_up_duration - scale_down_duration
            
            if stable_duration < 0:
                stable_duration = duration * 0.6
                scale_up_duration = duration * 0.2
                scale_down_duration = duration * 0.2
            
            # Scale animation keyframes
            # 70% -> 120% -> 100%
            scale_expr = self.create_scale_expression(
                start_time, scale_up_duration, scale_down_duration, stable_duration
            )
            
            # Position (center of screen)
            x_pos = "(w-text_w)/2"
            y_pos = "(h-text_h)/2"
            
            # Create drawtext filter
            filter_str = f"drawtext=text='{text}'" \
                        f":fontfile='Arial'" \
                        f":fontsize=60" \
                        f":fontcolor=white" \
                        f":bordercolor=black" \
                        f":borderw=3" \
                        f":x={x_pos}" \
                        f":y={y_pos}" \
                        f":enable='between(t,{start_time},{start_time + duration})'" \
                        f":{scale_expr}"
            
            filters.append(filter_str)
        
        return ','.join(filters)
    
    def create_scale_expression(self, start_time: float, scale_up_dur: float, 
                               scale_down_dur: float, stable_dur: float) -> str:
        """
        Create FFmpeg scale expression for the animation
        """
        # Time markers
        t1 = start_time
        t2 = start_time + scale_up_dur
        t3 = start_time + scale_up_dur + stable_dur
        t4 = start_time + scale_up_dur + stable_dur + scale_down_dur
        
        # Scale values
        scale_start = 0.7
        scale_peak = 1.2
        scale_final = 1.0
        
        scale_expr = f"fontsize=if(lt(t,{t1}),0," \
                    f"if(lt(t,{t2})," \
                    f"{int(60 * scale_start)} + {int(60 * (scale_peak - scale_start))} * (t-{t1})/{scale_up_dur}," \
                    f"if(lt(t,{t3})," \
                    f"{int(60 * scale_peak)}," \
                    f"if(lt(t,{t4})," \
                    f"{int(60 * scale_peak)} - {int(60 * (scale_peak - scale_final))} * (t-{t3})/{scale_down_dur}," \
                    f"{int(60 * scale_final)}))))"
        
        return scale_expr

class MrBeastStyleTextGenerator:
    """
    Generate MrBeast-style text overlays with animations
    """
    
    def __init__(self):
        self.overlay = AnimatedTextOverlay()
    
    def create_animated_subtitles(self, description_text: str, audio_duration: float) -> str:
        """
        Create animated subtitle file with MrBeast-style effects
        """
        # Parse text into timed segments
        text_segments = self.overlay.create_text_timing(description_text, audio_duration)
        
        # Generate advanced SRT with styling
        srt_content = ""
        
        for i, segment in enumerate(text_segments, 1):
            start_time = self.seconds_to_srt_time(segment['start_time'])
            end_time = self.seconds_to_srt_time(segment['end_time'])
            
            # Add styling for impact
            styled_text = f"<font color='yellow' size='24'><b>{segment['text']}</b></font>"
            
            srt_content += f"{i}\n"
            srt_content += f"{start_time} --> {end_time}\n"
            srt_content += f"{styled_text}\n\n"
        
        return srt_content
    
    def generate_ffmpeg_animated_filter(self, description_text: str, audio_duration: float) -> str:
        """
        Generate complete FFmpeg filter for animated text overlays
        """
        text_segments = self.overlay.create_text_timing(description_text, audio_duration)
        
        # Create multiple text overlay filters
        filters = []
        
        for i, segment in enumerate(text_segments):
            text = segment['text'].replace("'", "\\'").replace('"', '\\"')
            start_time = segment['start_time']
            duration = segment['duration']
            
            # Calculate positions (center screen, slight vertical offset)
            y_offset = -50 + (i % 3) * 30  # Small vertical variations
            
            # Create the animated drawtext filter
            filter_str = self.create_single_text_filter(
                text, start_time, duration, y_offset, i
            )
            
            filters.append(filter_str)
        
        # Join filters with proper syntax
        return '[0:v]' + ','.join(filters) + '[v]'
    
    def create_single_text_filter(self, text: str, start_time: float, 
                                 duration: float, y_offset: int, index: int) -> str:
        """
        Create a single animated text filter with MrBeast-style scaling
        """
        # Base font size
        base_size = 48
        
        # Scale animation parameters (simplified for FFmpeg compatibility)
        scale_up_time = 0.1  # 3 frames at 30fps
        scale_down_time = 0.1  # 3 frames at 30fps
        
        end_time = start_time + duration
        
        # Simplified scale expression that works with FFmpeg
        # Use conditional statements for scaling
        scale_expr = f"if(lt(t,{start_time + scale_up_time})," \
                    f"{int(base_size * 0.7)} + {int(base_size * 0.5)} * (t-{start_time})/{scale_up_time}," \
                    f"if(gt(t,{end_time - scale_down_time})," \
                    f"{int(base_size * 1.2)} - {int(base_size * 0.2)} * (t-{end_time - scale_down_time})/{scale_down_time}," \
                    f"{int(base_size * 1.2)})" \
                    f")"
        
        # Create the drawtext filter
        filter_str = f"drawtext=text='{text}'" \
                    f":fontsize={scale_expr}" \
                    f":fontcolor=white" \
                    f":bordercolor=black" \
                    f":borderw=3" \
                    f":x=(w-text_w)/2" \
                    f":y=(h-text_h)/2{'+' + str(y_offset) if y_offset >= 0 else str(y_offset)}" \
                    f":enable='between(t,{start_time},{end_time})'"
        
        return filter_str
    
    def seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        milliseconds = int((secs - int(secs)) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{milliseconds:03d}"

def get_audio_duration(audio_path: str) -> float:
    """Get audio duration using FFprobe"""
    import subprocess
    
    try:
        cmd = [
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
        
    except (subprocess.CalledProcessError, ValueError):
        # Fallback: assume 30 seconds if can't detect
        return 30.0

# Example usage
if __name__ == "__main__":
    generator = MrBeastStyleTextGenerator()
    
    # Example text
    sample_text = "Mark's world crumbled; a failing grade stared back from his history exam. Shame burned, but not as fiercely as his determination. He devoured textbooks, sought extra help, and practiced relentlessly."
    
    # Generate animated filter
    filter_str = generator.generate_ffmpeg_animated_filter(sample_text, 20.0)
    print("Generated FFmpeg Filter:")
    print(filter_str)