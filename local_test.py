"""
Local testing script for the media merger function.
This script tests individual functions without requiring Google Cloud credentials.
"""

import os
import tempfile

def format_srt_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    milliseconds = int((secs - int(secs)) * 1000)
    
    return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d},{milliseconds:03d}"

def create_subtitle_file(subtitle_path, description_text):
    """
    Create an SRT subtitle file with the description text.
    The subtitle will be displayed throughout the entire video duration.
    """
    # For simplicity, we'll show the description for the first 30 seconds
    # You can modify this to show different parts of the description at different times
    
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

def test_subtitle_creation():
    """Test the subtitle creation functionality"""
    print("Testing subtitle creation...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        subtitle_path = os.path.join(temp_dir, "test_subtitle.srt")
        test_description = "This is a test description for the video. It demonstrates how the subtitle system works with longer text that needs to be split into multiple lines."
        
        create_subtitle_file(subtitle_path, test_description)
        
        # Read and display the generated subtitle
        with open(subtitle_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("Generated subtitle content:")
            print("=" * 40)
            print(content)
            print("=" * 40)

def test_time_formatting():
    """Test the SRT time formatting"""
    print("\nTesting time formatting...")
    
    test_times = [0, 30, 65, 3661.5, 7200]
    for seconds in test_times:
        formatted = format_srt_time(seconds)
        print(f"{seconds} seconds -> {formatted}")

def simulate_cloud_event():
    """Simulate a cloud storage event"""
    print("\nSimulating cloud storage event...")
    
    # Create a mock cloud event
    mock_event_data = {
        'bucket': 'test-raw-assets-bucket',
        'name': 'projectTest_video.mp4'
    }
    
    print(f"Simulated event: {mock_event_data}")
    
    # Extract project ID
    file_name = mock_event_data['name']
    if '_' in file_name:
        project_id = file_name.split('_')[0]
        print(f"Extracted project ID: {project_id}")
    else:
        print("Invalid filename format")

def main():
    """Run all tests"""
    print("Media Merger Local Testing")
    print("=" * 50)
    
    test_subtitle_creation()
    test_time_formatting()
    simulate_cloud_event()
    
    print("\nLocal testing completed!")
    print("To deploy to Google Cloud, run: .\\deploy.ps1")

if __name__ == "__main__":
    main()
