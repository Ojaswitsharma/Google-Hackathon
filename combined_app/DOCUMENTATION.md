# 🌟 Safe Worlds API - Complete Documentation

## **Overview**

The Safe Worlds API is a sophisticated AI-powered mental wellness platform that transforms user emotional input into complete therapeutic multimedia experiences. It uses a 6-node LangGraph workflow powered by Google Flash 1.5 to create personalized safe worlds for youth mental health support.

## **🏗️ Architecture Overview**

### **Core Technologies**
- **🤖 AI Engine**: Google Flash 1.5 (Gemini) via LangChain
- **🎵 Audio**: Murf AI TTS (with gTTS fallback)
- **🎬 Video**: Pexels API for stock footage
- **🌐 API**: FastAPI with automatic documentation
- **🔄 Workflow**: LangGraph state management
- **💾 Storage**: Session-based file organization

### **File Structure**
```
combined_app/
├── main.py              # FastAPI server & endpoints
├── world_generator.py   # Main orchestrator class
├── langgraph_workflow.py # 6-node workflow definition
├── graph_nodes.py       # Individual processing nodes
├── models.py           # Pydantic data models
├── prompts.py          # LLM prompts for each step
├── requirements.txt    # Dependencies
├── .env                # Environment variables
└── output/            # Generated media files
    └── {session_id}/
        ├── story_audio.mp3    # Murf TTS audio
        ├── story_data.json    # Complete story metadata
        └── final_video.mp4    # Processed video (optional)
```

## **🔄 Complete Processing Workflow**

### **Step 1: API Request** 📥
Users send emotional input through a REST API:

```json
POST /generate_safe_world
{
  "user_input": "I'm feeling anxious and overwhelmed",
  "include_media": true,
  "duration_preference": "medium"
}
```

### **Step 2: Six-Node LangGraph Workflow** 🔗

#### **Node 1: Emotion Analysis** 🎭
- **Purpose**: Analyzes user's emotional state
- **AI Model**: Google Flash 1.5
- **Process**: 
  - Parses user input for emotional content
  - Identifies primary emotion from predefined categories
  - Extracts relevant keywords
- **Output**: Primary emotion + keywords
- **Example**: `"anxiety"` + `["overwhelming", "stress"]`

#### **Node 2: World Generation** 🌍
- **Purpose**: Creates therapeutic environment concept
- **Process**:
  - Maps emotions to appropriate world types
  - Generates interactive elements
  - Creates narrative framework
- **Emotion Mapping**:
  - Forest: anxiety, overwhelm (grounding)
  - Ocean: sadness, grief (release)
  - Mountain: anger, frustration (strength)
  - Garden: loneliness (growth, nurturing)
  - City: disconnection (community)
  - Fantasy: feeling trapped (magic, possibility)
  - Space: feeling insignificant (perspective)
- **Output**: World type, narrative, interactive elements, prompts

#### **Node 3: Story Generation** 📖
- **Purpose**: Creates immersive therapeutic narrative
- **Features**:
  - Second-person perspective ("You find yourself...")
  - Present tense for immediacy
  - Rich sensory details
  - Healing imagery and positive messaging
  - Adaptive length (40-180 words based on preference)
- **Quality Assurance**:
  - Validates story completion
  - Prevents cut-off sentences
  - Auto-completion for incomplete stories
- **Output**: Complete therapeutic story

#### **Node 4: Keyword Extraction** 🔑
- **Purpose**: Extracts visual elements for video search
- **Process**:
  - Analyzes story content
  - Identifies 1-2 concrete, visual objects
  - Filters for positive, peaceful imagery
  - Avoids negative or triggering terms
- **Output**: Video search keywords (e.g., "forest", "sunlight")

#### **Node 5: Audio Generation** 🎵
- **Purpose**: Creates high-quality narration
- **Primary Method**: Murf AI TTS
  - Professional voice synthesis
  - Downloads from Murf-provided URLs
  - High audio quality (22kHz+)
- **Fallback**: Google Text-to-Speech
- **Process**:
  1. Sends story to Murf API
  2. Downloads generated audio
  3. Calculates duration
  4. **Saves complete story data as JSON**
- **Output**: MP3 file + metadata + JSON data file

#### **Node 6: Video Generation** 🎬
- **Purpose**: Creates visual accompaniment
- **Process**:
  1. Searches Pexels API with extracted keywords
  2. Downloads appropriate stock footage
  3. Processes video with FFmpeg
  4. Synchronizes with audio duration
  5. Applies calming visual effects
- **Output**: MP4 file synchronized with audio

### **Step 3: Session Management** 📁
- **Unique Session ID**: 8-character UUID for each request
- **File Organization**: Structured output directory
- **Generated Files**:
  - `story_audio.mp3` - Murf AI narration
  - `story_data.json` - Complete story metadata
  - `final_video.mp4` - Synchronized video (optional)
- **Persistence**: Files remain accessible for future retrieval

### **Step 4: API Response** 📤
Complete response with all generated content:

```json
{
  "emotion": "anxiety",
  "world_type": "Forest",
  "narrative": "You enter a sun-dappled forest...",
  "generated_story": "Complete immersive story text...",
  "keywords": ["forest", "sunlight"],
  "interactive_elements": [
    "glowing mushrooms that softly illuminate the path",
    "gentle stream with smooth stones to skip",
    "birds singing calming melodies"
  ],
  "video_prompt": "A sunlit forest path, dappled light...",
  "music_prompt": "Ambient sounds of a forest...",
  "media_content": {
    "story_text": "Complete story text",
    "audio_path": "output/c87ff8ae/story_audio.mp3",
    "story_json_path": "output/c87ff8ae/story_data.json",
    "audio_duration": 23.1,
    "video_path": "output/c87ff8ae/final_video.mp4"
  },
  "session_id": "c87ff8ae",
  "created_at": "2025-09-17T14:30:00"
}
```

## **📱 API Endpoints**

### **Core Generation Endpoints**

#### **`POST /generate_safe_world`**
- **Purpose**: Complete workflow with multimedia generation
- **Request Body**:
  ```json
  {
    "user_input": "string",
    "include_media": true,
    "duration_preference": "short|medium|long"
  }
  ```
- **Response**: Complete SafeWorldResponse object
- **Processing Time**: 30-60 seconds (includes audio/video generation)

#### **`POST /generate_safe_world_quick`**
- **Purpose**: Fast generation without media
- **Features**: Text-only response for immediate feedback
- **Processing Time**: 5-10 seconds

### **Media Serving Endpoints**

#### **`GET /media/audio/{session_id}`**
- **Purpose**: Download generated audio file
- **Returns**: MP3 file with proper headers
- **Filename**: `safe_world_{session_id}.mp3`

#### **`GET /media/video/{session_id}`**
- **Purpose**: Download generated video file
- **Returns**: MP4 file with proper headers
- **Filename**: `safe_world_{session_id}.mp4`

### **Utility Endpoints**

#### **`GET /session/{session_id}/status`**
- **Purpose**: Check generation status and media availability
- **Response**:
  ```json
  {
    "status": "found",
    "audio_ready": true,
    "video_ready": true,
    "audio_url": "/media/audio/{session_id}",
    "video_url": "/media/video/{session_id}"
  }
  ```

#### **`GET /health`**
- **Purpose**: Health check for monitoring
- **Response**: `{"status": "healthy", "service": "Safe Worlds Generator"}`

#### **`GET /`**
- **Purpose**: API information and available endpoints
- **Response**: Complete API documentation summary

## **🎯 Key Features & Innovations**

### **✅ Advanced AI Integration**
1. **Google Flash 1.5**: Latest Gemini model for superior language understanding
2. **Multi-Stage Processing**: Each node specialized for specific tasks
3. **Intelligent Validation**: Story completion logic prevents truncated content
4. **Adaptive Responses**: Content varies based on emotional state and preferences

### **🎵 Professional Audio Generation**
1. **Murf AI TTS**: High-quality voice synthesis
2. **Fallback System**: gTTS backup ensures reliability
3. **Duration Tracking**: Precise audio length calculation
4. **Format Optimization**: MP3 encoding for web delivery

### **🎬 Dynamic Video Creation**
1. **Contextual Search**: Keywords extracted from story content
2. **Stock Footage**: Pexels API for high-quality visuals
3. **Audio Sync**: FFmpeg processing for perfect timing
4. **Peaceful Content**: Filtering ensures appropriate imagery

### **📊 Comprehensive Data Storage**
1. **Session Management**: Unique identifiers for each generation
2. **JSON Metadata**: Complete story data with structured information
3. **File Organization**: Clean directory structure
4. **Persistent Storage**: Files remain accessible post-generation

## **🚀 Setup & Running**

### **Environment Requirements**
```bash
# Python 3.8+
# Virtual environment recommended

# Key dependencies:
- fastapi
- uvicorn
- langchain
- langchain-google-genai
- google-generativeai
- murf
- requests
- pydantic
```

### **Environment Variables**
```env
GOOGLE_API_KEY=your_google_ai_key
PEXELS_API_KEY=your_pexels_key
ELEVENLABS_API_KEY=your_elevenlabs_key (optional)
```

### **Starting the Server**
```bash
# Method 1: Direct execution
cd /home/os/safeworld-video/combined_app
source ../svenv/bin/activate
python main.py

# Method 2: Using uvicorn
uvicorn main:app --host 127.0.0.1 --port 8004

# Method 3: Using the startup script
./start_server.sh
```

### **Access Points**
- **API Server**: http://127.0.0.1:8004
- **Documentation**: http://127.0.0.1:8004/docs
- **OpenAPI Schema**: http://127.0.0.1:8004/openapi.json

## **🔧 Configuration Options**

### **Duration Preferences**
- **Short**: 40-60 words, ~15-20 second audio
- **Medium**: 70-100 words, ~25-35 second audio  
- **Long**: 120-180 words, ~45-60 second audio

### **Emotion Categories**
- anxiety, sadness, anger, joy, overwhelm, lonely, excited, neutral

### **World Types**
- Forest, Ocean, Mountain, Garden, City, Fantasy, Space

## **🔍 Troubleshooting**

### **Common Issues**

#### **Port Already in Use**
```bash
# Kill existing process
lsof -ti:8004 | xargs kill -9 2>/dev/null || true
```

#### **Missing Dependencies**
```bash
# Reinstall requirements
pip install -r requirements.txt
```

#### **API Key Issues**
- Verify `.env` file contains valid API keys
- Check Google API quota and billing
- Ensure Pexels API key has sufficient requests

#### **Story Truncation**
- Updated with completion validation logic
- Automatic story finishing for incomplete responses
- Token limit management

### **Monitoring & Logs**
- Server logs show processing steps for each node
- Session IDs enable request tracking
- File system shows generation success/failure

## **💎 Unique Capabilities**

### **🧠 Therapeutic Design**
- Evidence-based emotion-to-environment mapping
- Trauma-informed content generation
- Youth-focused language and imagery
- Positive psychology principles

### **🎭 Emotion Intelligence**
- Multi-dimensional emotion analysis
- Context-aware world selection
- Adaptive narrative generation
- Personalized interactive elements

### **🎨 Multi-Modal Generation**
- Synchronized audio-visual experiences
- Professional-quality voice synthesis
- Contextually appropriate video selection
- Cohesive multimedia storytelling

### **🔄 Production-Ready Architecture**
- FastAPI with automatic documentation
- RESTful API design
- Session-based state management
- Comprehensive error handling
- Scalable file organization

## **📈 Future Enhancements**

### **Planned Features**
- User profile persistence
- Emotion tracking over time
- Custom voice selection
- Interactive story elements
- Mobile app integration
- Therapist dashboard
- Analytics and insights

### **Technical Improvements**
- Containerized deployment
- Database integration
- Redis caching
- Load balancing
- CDN integration for media files

---

## **📧 Technical Support**

This documentation covers the complete Safe Worlds API system. For technical issues or feature requests, refer to the codebase structure outlined above.

**Last Updated**: September 17, 2025  
**Version**: 2.0.0  
**AI Model**: Google Flash 1.5 (Gemini)  
**Status**: Production Ready ✅
