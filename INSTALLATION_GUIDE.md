# 📦 Safe Worlds - Requirements Installation Guide

## 🎯 Quick Installation

### For Basic Usage (Recommended)
```bash
pip install -r requirements.txt
```

## 📋 Requirements Files Overview

### `requirements.txt` - Core Dependencies
- **FastAPI & Uvicorn**: Web framework and ASGI server
- **LangChain & LangGraph**: AI workflow orchestration
- **Google AI**: Gemini 1.5 Flash LLM integration
- **Audio/Video**: TTS, video processing, media handling
- **Essential utilities**: Environment, HTTP, data validation

### `requirements-dev.txt` - Development Tools
- **Testing**: pytest, test utilities
- **Code Quality**: black, flake8, mypy
- **Documentation**: sphinx
- **Development**: jupyter, pre-commit hooks

### `requirements-prod.txt` - Production Extras
- **Performance**: gunicorn, redis, async utilities
- **Database**: PostgreSQL, migrations
- **Monitoring**: prometheus, structured logging
- **Security**: authentication, encryption

## 🔧 Installation Methods

### Method 1: Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv safeworld-env
source safeworld-env/bin/activate  # On Windows: safeworld-env\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Method 2: Conda Environment
```bash
# Create conda environment
conda create -n safeworld python=3.11
conda activate safeworld

# Install requirements
pip install -r requirements.txt
```

### Method 3: Docker (Advanced)
```bash
# Build Docker image with all dependencies
docker build -t safeworld:latest .

# Run container
docker run -p 8004:8004 -p 3000:3000 safeworld:latest
```

## 🌐 Environment Variables Required

Create a `.env` file in the `combined_app/` directory:
```env
# AI Services
GOOGLE_API_KEY=your_google_api_key_here
MURF_API_KEY=your_murf_api_key_here

# Media Services
PEXELS_API_KEY=your_pexels_api_key_here

# Optional: Development
DEBUG=true
LOG_LEVEL=INFO
```

## 🚀 Verification Steps

### 1. Test Core Dependencies
```bash
python -c "import fastapi, langchain, langgraph; print('✅ Core AI dependencies OK')"
```

### 2. Test Media Processing
```bash
python -c "import moviepy, gtts, mutagen; print('✅ Media processing OK')"
```

### 3. Test Google AI
```bash
python -c "from langchain_google_genai import ChatGoogleGenerativeAI; print('✅ Google AI OK')"
```

### 4. Test Server Start
```bash
cd combined_app
python main.py
# Should show: "🌟 Starting Safe Worlds API Server..."
```

## 🔍 Package Details

### Core Framework (17.2MB)
- `fastapi==0.116.2` - Modern Python web framework
- `uvicorn==0.35.0` - Lightning-fast ASGI server
- `pydantic==2.11.7` - Data validation using Python type hints

### AI & LLM (45.8MB)
- `langchain==0.3.27` - LLM application framework
- `langgraph==0.6.7` - Workflow orchestration for AI agents
- `langchain-google-genai==2.0.10` - Google Gemini integration

### Media Processing (78.3MB)
- `moviepy==2.2.1` - Video editing and processing
- `opencv-python==4.12.0.88` - Computer vision library
- `ffmpeg-python==0.2.0` - Python FFmpeg wrapper

### Audio/TTS (12.4MB)
- `gtts==2.5.4` - Google Text-to-Speech
- `murf==2.0.2` - Professional AI voice synthesis
- `mutagen==1.47.0` - Audio metadata handling

## ⚠️ Common Issues & Solutions

### Issue: ModuleNotFoundError
**Solution**: Ensure virtual environment is activated
```bash
source safeworld-env/bin/activate  # or svenv/bin/activate
pip install -r requirements.txt
```

### Issue: Google AI Authentication
**Solution**: Set proper API key
```bash
export GOOGLE_API_KEY="your_actual_api_key"
```

### Issue: FFmpeg not found
**Solution**: Install system FFmpeg
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Issue: Audio device errors
**Solution**: Install audio system dependencies
```bash
# Ubuntu/Debian
sudo apt install portaudio19-dev python3-pyaudio

# macOS
brew install portaudio
```

## 📊 Total Size Estimate
- **Core requirements**: ~150MB
- **With development**: ~200MB  
- **With production**: ~250MB
- **Full installation**: ~300MB

## 🎯 Minimal Installation
For basic functionality only:
```bash
pip install fastapi uvicorn langchain langchain-google-genai langgraph gtts moviepy python-dotenv requests
```

**Ready to generate Safe Worlds! 🌟**
