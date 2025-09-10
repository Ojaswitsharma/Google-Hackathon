#!/usr/bin/env python3

import requests
import random
import subprocess
import os
from dotenv import load_dotenv
import json
from gtts import gTTS
from mutagen.mp3 import MP3

# Load environment variables from .env file
load_dotenv()

# Pexels API key
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_VIDEO_SEARCH_URL = "https://api.pexels.com/videos/search"

# Google AI Studio Gemini 1.5 Flash API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_AI_STUDIO_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

def gemini_generate(prompt, max_tokens=256):
    headers = {"Content-Type": "application/json"}
    url = f"{GOOGLE_AI_STUDIO_API_URL}?key={GOOGLE_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.7}
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            return ""
    else:
        raise RuntimeError(f"Gemini API error: {response.status_code} {response.text}")

def generate_story(prompt, min_words=60, max_words=70):
    system_prompt = f"Write a story based on the following prompt. The story should be between {min_words} and {max_words} words.\nPrompt: {prompt}"
    story = gemini_generate(system_prompt, max_tokens=max_words*2)
    words = story.split()
    story = " ".join(words[:max_words])
    return story

def extract_keywords(text, num_keywords=1):
    system_prompt = (
        f"From the following story, extract one keyword that is the main tangible object or subject of the story, which is concrete, easy to find a stock video for, and is NOT likely to fetch a depressing or violent video (e.g., avoid words like war, death, sadness, fight, blood, etc). Only return the single keyword, nothing else.\nStory: {text}"
    )
    keywords_text = gemini_generate(system_prompt, max_tokens=8)
    keyword = keywords_text.strip().split(",")[0]
    return [keyword]

def search_pexels_video(keywords):
    headers = {"Authorization": PEXELS_API_KEY}
    query = " ".join(keywords)
    params = {"query": query, "per_page": 10}  # Get up to 10 videos
    response = requests.get(PEXELS_VIDEO_SEARCH_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        videos = data.get("videos", [])
        if videos:
            video = random.choice(videos)
            return video["video_files"][0]["link"]
    return None

def download_video(video_url, filename):
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    return False

def process_video(input_path, output_path, duration):
    import ffmpeg
    probe = ffmpeg.probe(input_path)
    video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
    video_duration = float(video_streams[0]['duration']) if video_streams else 0
    # If video is shorter than audio, loop it
    if video_duration < duration:
        import tempfile
        import shutil
        loops = int(duration // video_duration) + 1
        temp_dir = tempfile.mkdtemp()
        temp_list_path = os.path.join(temp_dir, 'concat_list.txt')
        with open(temp_list_path, 'w') as f:
            for _ in range(loops):
                f.write(f"file '{os.path.abspath(input_path)}'\n")
        temp_looped_path = os.path.join(temp_dir, 'looped.mp4')
        concat_cmd = [
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', temp_list_path,
            '-c', 'copy', temp_looped_path
        ]
        subprocess.run(concat_cmd, check=True)
        input_path = temp_looped_path
    # Trim to audio duration
    # crop_filter = 'crop=ih*9/16:ih:(iw-ih*9/16)/2:0'  # 9:16 aspect ratio crop (commented out)
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output file if exists
        '-i', input_path,
        '-t', str(duration),
        # '-vf', crop_filter,  # Commented out to keep original aspect ratio
        '-c:v', 'libx264',
        '-c:a', 'aac',
        output_path
    ]
    subprocess.run(cmd, check=True)
    if 'temp_looped_path' in locals():
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    prompt = input("Enter a prompt for your story: ")
    story = generate_story(prompt)
    # Save story to JSON file
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    import time
    safe_keyword = story.split()[0].replace(" ", "_")
    timestamp = int(time.time())
    story_json_path = os.path.join(output_folder, f"story_{timestamp}.json")
    with open(story_json_path, "w") as f:
        json.dump({"story": story}, f, indent=2)
    print(f"Story saved to {story_json_path}")
    # Save story as audio using gTTS
    audio_path = os.path.join(output_folder, f"story_{timestamp}.mp3")
    tts = gTTS(story)
    tts.save(audio_path)
    print(f"Story audio saved to {audio_path}")
    # Get audio duration
    audio = MP3(audio_path)
    audio_duration = audio.info.length
    print(f"Audio duration: {audio_duration:.2f} seconds")
    keywords = extract_keywords(story)
    print("Extracted Keywords:", keywords)
    video_url = search_pexels_video(keywords)
    if video_url:
        print("Relevant video URL:", video_url)
        os.makedirs(output_folder, exist_ok=True)
        safe_keyword = keywords[0].replace(" ", "_")
        filename = os.path.join(output_folder, f"{safe_keyword}_{timestamp}.mp4")
        print(f"Downloading video to {filename}...")
        if download_video(video_url, filename):
            print("Video downloaded successfully.")
            # Process video: trim and crop to audio duration
            processed_filename = os.path.join(output_folder, f"{safe_keyword}_{timestamp}_processed.mp4")
            print(f"Processing video to {audio_duration:.2f}s and 9:16 aspect ratio: {processed_filename}")
            process_video(filename, processed_filename, audio_duration)
            print("Processed video saved.")
            # Delete original video
            try:
                os.remove(filename)
                print(f"Deleted original video: {filename}")
            except Exception as e:
                print(f"Failed to delete original video: {e}")
        else:
            print("Failed to download video.")
    else:
        print("No relevant video found.")
