from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List
from langchain_core.messages import HumanMessage
import json
import re
import os
import time
import requests
import random
import subprocess
import tempfile
import shutil
from gtts import gTTS
from mutagen.mp3 import MP3
from dotenv import load_dotenv
from models import GraphState
from prompts import (
    EMOTION_ANALYSIS_PROMPT, 
    WORLD_GENERATION_PROMPT, 
    STORY_GENERATION_PROMPT,
    KEYWORD_EXTRACTION_PROMPT
)

# Import Murf for TTS
try:
    from murf import Murf
    MURF_AVAILABLE = True
except ImportError:
    MURF_AVAILABLE = False
    print("Warning: Murf SDK not available, falling back to gTTS")

# Load environment variables
load_dotenv()

# Initialize Google Flash 1.5 LLM (shared across nodes)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    max_tokens=512,  # Ensure enough tokens for complete stories
    convert_system_message_to_human=True
)

# API Keys
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PEXELS_VIDEO_SEARCH_URL = "https://api.pexels.com/videos/search"

def analyze_emotion_node(state: GraphState) -> GraphState:
    """Node 1: Analyze user's emotional state"""
    print("--- ANALYZING EMOTION ---")
    
    user_input = state['messages'][-1].content
    
    prompt = PromptTemplate(
        template=EMOTION_ANALYSIS_PROMPT,
        input_variables=["user_input"]
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        response = chain.invoke({"user_input": user_input})
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            state['emotion'] = result.get('emotion', 'neutral')
            state['keywords'] = result.get('keywords', ['calm'])
        else:
            state['emotion'] = _detect_emotion_fallback(user_input)
            state['keywords'] = ['peace']
            
    except Exception as e:
        print(f"Error in emotion analysis: {e}")
        state['emotion'] = 'neutral'
        state['keywords'] = ['calm']
    
    return state

def generate_world_node(state: GraphState) -> GraphState:
    """Node 2: Generate the safe world based on emotion analysis"""
    print("--- GENERATING SAFE WORLD ---")
    
    user_input = state['messages'][0].content
    emotion = state['emotion']
    keywords = state['keywords']
    
    prompt = PromptTemplate(
        template=WORLD_GENERATION_PROMPT,
        input_variables=["user_input", "emotion", "keywords"]
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        response = chain.invoke({
            "user_input": user_input,
            "emotion": emotion,
            "keywords": ', '.join(keywords)
        })
        
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            state['world_type'] = result.get('world_type', 'forest')
            state['interactive_elements'] = result.get('interactive_elements', [])
            state['narrative'] = result.get('narrative', '')
            state['video_prompt'] = result.get('video_prompt', '')
            state['music_prompt'] = result.get('music_prompt', '')
        else:
            _create_fallback_world(state)
            
    except Exception as e:
        print(f"Error in world generation: {e}")
        _create_fallback_world(state)
    
    return state

def generate_story_node(state: GraphState) -> GraphState:
    """Node 3: Generate immersive story based on the world"""
    print("--- GENERATING STORY ---")
    
    if not state.get('include_media', True):
        state['generated_story'] = ""
        state['story_generated'] = False
        return state
    
    world_type = state['world_type']
    emotion = state['emotion']
    narrative = state['narrative']
    
    # Determine story length based on preference
    duration_map = {
        "short": {"min_words": 40, "max_words": 60},
        "medium": {"min_words": 70, "max_words": 100},
        "long": {"min_words": 120, "max_words": 180}
    }
    
    duration_prefs = duration_map.get(state.get('duration_preference', 'short'), duration_map['short'])
    
    prompt = PromptTemplate(
        template=STORY_GENERATION_PROMPT,
        input_variables=["world_type", "emotion", "narrative", "min_words", "max_words"]
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        response = chain.invoke({
            "world_type": world_type,
            "emotion": emotion,
            "narrative": narrative,
            "min_words": duration_prefs["min_words"],
            "max_words": duration_prefs["max_words"]
        })
        
        # Clean up the story and validate completion
        story = response.strip()
        
        # Check if story ends properly (not cut off mid-sentence)
        if not story.endswith(('.', '!', '?')) or story.endswith(','):
            print("⚠️ Story appears incomplete, attempting to complete...")
            # Try to regenerate with explicit completion instruction
            completion_prompt = PromptTemplate(
                template="""Complete this therapeutic story properly. The story below was cut off. Please provide a proper, complete ending that brings peace and closure. Return ONLY the complete story:

Incomplete story: {incomplete_story}

Make sure to end with a complete, peaceful conclusion.""",
                input_variables=["incomplete_story"]
            )
            
            try:
                completion_chain = completion_prompt | llm | StrOutputParser()
                story = completion_chain.invoke({"incomplete_story": story}).strip()
                print("✅ Story completion attempted")
            except Exception as e:
                print(f"⚠️ Could not complete story: {e}")
                # Add a simple completion if all else fails
                if not story.endswith(('.', '!', '?')):
                    story += " Here, in this safe space, you find the peace you seek."
        
        words = story.split()
        # Only truncate if significantly over limit (allow some flexibility)
        if len(words) > duration_prefs["max_words"] + 20:
            story = " ".join(words[:duration_prefs["max_words"]])
            # Ensure we don't cut off mid-sentence after truncation
            if not story.endswith(('.', '!', '?')):
                story += "."
        
        state['generated_story'] = story
        state['story_generated'] = True
        print(f"✅ Story generated: {len(words)} words")
        
    except Exception as e:
        print(f"Error in story generation: {e}")
        state['generated_story'] = _create_fallback_story(state)
        state['story_generated'] = True
    
    return state

def extract_video_keywords_node(state: GraphState) -> GraphState:
    """Node 4: Extract keywords from story for video search"""
    print("--- EXTRACTING VIDEO KEYWORDS ---")
    
    if not state.get('include_media', True) or not state.get('story_generated', False):
        state['story_keywords'] = []
        return state
    
    story = state['generated_story']
    
    try:
        # Use Gemini API for keyword extraction
        if GOOGLE_API_KEY:
            keywords = _extract_keywords_gemini(story)
        else:
            # Fallback to local LLM
            keywords = _extract_keywords_local(story)
        
        state['story_keywords'] = keywords
        
    except Exception as e:
        print(f"Error in keyword extraction: {e}")
        state['story_keywords'] = [state['world_type']]  # Fallback to world type
    
    return state

def generate_audio_node(state: GraphState) -> GraphState:
    """Node 5: Generate audio from story using Murf AI"""
    print("--- GENERATING AUDIO WITH MURF AI ---")
    
    if not state.get('include_media', True) or not state.get('story_generated', False):
        state['audio_generated'] = False
        return state
    
    try:
        story = state['generated_story']
        session_id = state['session_id']
        
        # Create output directory
        output_folder = f"output/{session_id}"
        os.makedirs(output_folder, exist_ok=True)
        
        # Generate audio using Murf AI
        audio_path = os.path.join(output_folder, f"story_audio.mp3")
        audio_duration = _murf_tts(story, audio_path)
        
        # Save story as JSON file
        story_data = {
            "story_text": story,
            "emotion": state.get('emotion', 'unknown'),
            "world_type": state.get('world_type', 'unknown'),
            "keywords": state.get('story_keywords', []),
            "session_id": session_id,
            "narrative": state.get('narrative', ''),
            "interactive_elements": state.get('interactive_elements', []),
            "video_prompt": state.get('video_prompt', ''),
            "music_prompt": state.get('music_prompt', ''),
            "created_at": state.get('created_at', ''),
            "include_media": state.get('include_media', True),
            "duration_preference": state.get('duration_preference', 'medium')
        }
        
        story_json_path = os.path.join(output_folder, f"story_data.json")
        with open(story_json_path, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, indent=2, ensure_ascii=False)
        
        print(f"Story data saved as JSON: {story_json_path}")
        
        if audio_duration:
            # Update state
            if 'media_content' not in state:
                state['media_content'] = {}
            
            state['media_content']['audio_path'] = audio_path
            state['media_content']['audio_duration'] = audio_duration
            state['media_content']['story_json_path'] = story_json_path
            state['audio_generated'] = True
            
            print(f"Murf audio generated: {audio_path} ({audio_duration:.2f}s)")
        else:
            print("Failed to generate audio with Murf AI, falling back to gTTS")
            # Fallback to gTTS
            tts = gTTS(story)
            tts.save(audio_path)
            
            # Get audio duration
            audio = MP3(audio_path)
            audio_duration = audio.info.length
            
            # Update state
            if 'media_content' not in state:
                state['media_content'] = {}
            
            state['media_content']['audio_path'] = audio_path
            state['media_content']['audio_duration'] = audio_duration
            state['media_content']['story_json_path'] = story_json_path
            state['audio_generated'] = True
            
            print(f"gTTS fallback audio generated: {audio_path} ({audio_duration:.2f}s)")
        
    except Exception as e:
        print(f"Error in audio generation: {e}")
        state['audio_generated'] = False
    
    return state

def generate_video_node(state: GraphState) -> GraphState:
    """Node 6: Generate video from keywords"""
    print("--- GENERATING VIDEO ---")
    
    if not state.get('include_media', True) or not state.get('audio_generated', False):
        state['video_generated'] = False
        return state
    
    try:
        keywords = state.get('story_keywords', [state['world_type']])
        session_id = state['session_id']
        audio_duration = state['media_content']['audio_duration']
        
        output_folder = f"output/{session_id}"
        
        # Search for video on Pexels
        video_url = _search_pexels_video(keywords)
        
        if video_url:
            # Download and process video
            raw_video_path = os.path.join(output_folder, "raw_video.mp4")
            processed_video_path = os.path.join(output_folder, "final_video.mp4")
            
            if _download_video(video_url, raw_video_path):
                _process_video(raw_video_path, processed_video_path, audio_duration)
                
                # Update state
                state['media_content']['video_path'] = processed_video_path
                state['media_content']['video_url'] = video_url
                state['video_generated'] = True
                
                # Clean up raw video
                try:
                    os.remove(raw_video_path)
                except:
                    pass
                
                print(f"Video generated: {processed_video_path}")
            else:
                state['video_generated'] = False
        else:
            state['video_generated'] = False
            
    except Exception as e:
        print(f"Error in video generation: {e}")
        state['video_generated'] = False
    
    return state

# Helper Functions

def _detect_emotion_fallback(user_input: str) -> str:
    """Simple keyword-based emotion detection for fallback"""
    input_lower = user_input.lower()
    
    if any(word in input_lower for word in ["anxious", "worry", "nervous", "overwhelm"]):
        return "anxiety" 
    elif any(word in input_lower for word in ["sad", "depressed", "down", "hurt"]):
        return "sadness"
    elif any(word in input_lower for word in ["angry", "mad", "frustrated"]):
        return "anger"
    elif any(word in input_lower for word in ["lonely", "alone", "isolated"]):
        return "lonely"
    elif any(word in input_lower for word in ["excited", "happy", "amazing"]):
        return "joy"
    else:
        return "neutral"

def _create_fallback_world(state: GraphState):
    """Create fallback world when LLM generation fails"""
    emotion = state['emotion']
    
    world_map = {
        "anxiety": "forest",
        "sadness": "garden", 
        "anger": "mountain",
        "lonely": "garden",
        "joy": "fantasy",
        "neutral": "forest"
    }
    
    world_type = world_map.get(emotion, "forest")
    
    state['world_type'] = world_type
    state['interactive_elements'] = [
        f"a peaceful spot to rest in the {world_type}",
        "gentle sounds of nature",
        "soft, calming light"
    ]
    state['narrative'] = f"You enter a serene {world_type} where every breath brings you peace and every moment helps you feel more centered."
    state['video_prompt'] = f"A beautiful, peaceful {world_type} with soft lighting and gentle movement"
    state['music_prompt'] = f"Calming {world_type} ambience with natural sounds and peaceful atmosphere"

def _create_fallback_story(state: GraphState) -> str:
    """Create fallback story"""
    world_type = state['world_type']
    emotion = state['emotion']
    
    return f"You find yourself in a peaceful {world_type}, where the gentle sounds of nature wash away your {emotion}. With each breath, you feel more centered and calm. This is your safe space, where healing begins."

def _extract_keywords_gemini(text: str) -> List[str]:
    """Extract keywords using Google Flash 1.5 via LangChain"""
    try:
        prompt = PromptTemplate(
            template="From the following story, extract 1-2 keywords that are concrete, visual objects suitable for finding stock videos. Avoid negative or violent terms. Return only the keywords separated by commas.\n\nStory: {text}",
            input_variables=["text"]
        )
        
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({"text": text})
        
        # Parse keywords from result
        keywords = [kw.strip() for kw in result.split(',')]
        return [kw for kw in keywords if kw and len(kw) > 2][:2]  # Limit to 2 keywords
        
    except Exception as e:
        print(f"Error extracting keywords with Google Flash: {e}")
        return ["nature"]

def _extract_keywords_local(text: str) -> List[str]:
    """Extract keywords using local LLM"""
    prompt = PromptTemplate(
        template=KEYWORD_EXTRACTION_PROMPT,
        input_variables=["text"]
    )
    
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"text": text})
    
    # Parse result
    keywords = [k.strip() for k in result.split(",")[:2]]
    return [k for k in keywords if k and len(k) > 2]

def _search_pexels_video(keywords: List[str]) -> str:
    """Search for video on Pexels"""
    if not PEXELS_API_KEY:
        return None
    
    headers = {"Authorization": PEXELS_API_KEY}
    query = " ".join(keywords[:2])  # Use max 2 keywords
    params = {"query": query, "per_page": 10}
    
    response = requests.get(PEXELS_VIDEO_SEARCH_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        videos = data.get("videos", [])
        if videos:
            video = random.choice(videos)
            return video["video_files"][0]["link"]
    return None

def _download_video(video_url: str, filename: str) -> bool:
    """Download video from URL"""
    try:
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Error downloading video: {e}")
    return False

def _process_video(input_path: str, output_path: str, duration: float):
    """Process video to match audio duration"""
    try:
        import ffmpeg
        
        # Get video info
        probe = ffmpeg.probe(input_path)
        video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
        video_duration = float(video_streams[0]['duration']) if video_streams else 0
        
        # If video is shorter than audio, loop it
        if video_duration < duration:
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
            subprocess.run(concat_cmd, check=True, capture_output=True)
            input_path = temp_looped_path
        
        # Trim to audio duration
        cmd = [
            'ffmpeg', '-y', '-i', input_path, '-t', str(duration),
            '-c:v', 'libx264', '-c:a', 'aac', output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Clean up temp directory
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir)
            
    except Exception as e:
        print(f"Error processing video: {e}")
        # Copy original as fallback
        shutil.copy2(input_path, output_path)

def _murf_tts(text: str, output_path: str, voice_id: str = "en-UK-pearl") -> float:
    """Generate audio using Murf AI TTS"""
    if not MURF_AVAILABLE:
        return False
    
    try:
        client = Murf(
            api_key="ap2_5f1b1f03-645f-45c1-a96d-18f8d4d3ec4a"
        )
        res = client.text_to_speech.generate(
            text=text,
            voice_id=voice_id,
            rate=10
        )
        
        # Check if Murf returned a URL
        if hasattr(res, 'audio_file') and res.audio_file:
            audio_url = res.audio_file
            print(f"Murf Audio URL: {audio_url}")
            
            # Download the audio file from the URL
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(audio_response.content)
                print(f"Audio downloaded and saved to: {output_path}")
                
                # Return the actual duration from Murf response
                duration = getattr(res, 'audio_length_in_seconds', 15)
                return duration
            else:
                print(f"Failed to download audio from URL: {audio_response.status_code}")
                return False
        else:
            print("Murf AI TTS error: No audio URL returned.")
            return False
            
    except Exception as e:
        print(f"Error with Murf TTS: {e}")
        return False