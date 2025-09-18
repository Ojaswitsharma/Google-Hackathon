# Safe Worlds - AI Mental Wellness Generator

A combined FastAPI application that generates personalized, immersive safe worlds for youth mental wellness. This integrates the Dhairya branch's LangGraph workflow with Murf AI TTS for high-quality audio generation.

## Features

- **Emotion Analysis**: Detects user's emotional state from input
- **Therapeutic World Generation**: Creates safe, personalized virtual environments  
- **Immersive Story Creation**: Generates calming narratives
- **High-Quality Audio**: Uses Murf AI TTS for natural-sounding narration
- **Video Visualization**: Fetches relevant videos from Pexels
- **RESTful API**: Complete FastAPI with JSON responses

## Quick Start

1. **Install Dependencies**:
   ```bash
   cd combined_app
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   Make sure `.env` contains:
   ```
   PEXELS_API_KEY=your_pexels_key
   GOOGLE_API_KEY=your_google_key
   ```

3. **Start the Server**:
   ```bash
   python main.py
   ```
   
   The API will be available at: http://127.0.0.1:8004

4. **Test the API**:
   ```bash
   python test_api.py
   ```

## API Endpoints

### Core Generation
- `POST /generate_safe_world` - Complete world with audio/video
- `POST /generate_safe_world_quick` - Fast generation (no media)

### Media Access
- `GET /media/audio/{session_id}` - Download generated audio
- `GET /media/video/{session_id}` - Download processed video
- `GET /session/{session_id}/status` - Check media generation status

### Utility
- `GET /health` - Health check
- `GET /` - API information and endpoints

## Example Usage

### Quick Generation (No Media)
```python
import requests

response = requests.post("http://127.0.0.1:8004/generate_safe_world_quick", json={
    "user_input": "I'm feeling anxious about my upcoming exam",
    "include_media": False
})

data = response.json()
print(f"Emotion: {data['emotion']}")
print(f"World: {data['world_type']}")
print(f"Story: {data['generated_story']}")
```

### Full Generation (With Media)
```python
response = requests.post("http://127.0.0.1:8004/generate_safe_world", json={
    "user_input": "I'm feeling stressed and need to relax",
    "include_media": True,
    "duration_preference": "short"
})

data = response.json()
session_id = data['session_id']

# Access generated media
audio_url = f"http://127.0.0.1:8004/media/audio/{session_id}"
video_url = f"http://127.0.0.1:8004/media/video/{session_id}"
```

## Response Format

```json
{
  "emotion": "anxiety",
  "keywords": ["calm", "peace"],
  "interactive_elements": ["a quiet place to breathe", "gentle sounds"],
  "narrative": "You enter a serene forest...",
  "video_prompt": "A peaceful forest with soft lighting",
  "music_prompt": "Calming forest ambience",
  "world_type": "forest",
  "generated_story": "You find yourself in a peaceful forest clearing...",
  "media_content": {
    "story_text": "Story text here...",
    "audio_path": "output/abc123/story_audio.mp3",
    "video_path": "output/abc123/final_video.mp4",
    "audio_duration": 45.2
  },
  "session_id": "abc123",
  "created_at": "2025-09-17T..."
}
```

## Technical Architecture

- **FastAPI**: Web framework and API server
- **LangGraph**: Multi-node workflow for content generation
- **Murf AI**: High-quality text-to-speech synthesis
- **Pexels API**: Stock video content
- **FFmpeg**: Video processing and synchronization

## Key Integrations

1. **Murf TTS Integration**: Replaced gTTS with Murf AI for premium audio quality
2. **Fallback System**: Graceful degradation to gTTS if Murf fails
3. **Session Management**: Unique session IDs for media organization
4. **Media Serving**: Static file serving for audio/video downloads
5. **Error Handling**: Comprehensive error handling with fallbacks

## Development

- API documentation: http://127.0.0.1:8004/docs
- Health check: http://127.0.0.1:8004/health
- Test suite: `python test_api.py`

## File Structure

```
combined_app/
├── main.py                 # FastAPI server
├── models.py              # Pydantic models
├── world_generator.py     # Main generation orchestrator
├── langgraph_workflow.py  # LangGraph workflow definition
├── graph_nodes.py         # Individual workflow nodes (with Murf TTS)
├── prompts.py            # LLM prompts
├── test_api.py           # Test suite
├── requirements.txt      # Dependencies
└── .env                  # Environment variables
```
