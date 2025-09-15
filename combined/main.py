from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from models import EmotionRequest, SafeWorldResponse
from world_generator import SafeWorldGenerator

app = FastAPI(
    title="Safe Worlds - AI Mental Wellness Generator",
    description="Generate personalized, immersive safe worlds for youth mental wellness",
    version="2.0.0"
)

# Initialize the generator
generator = SafeWorldGenerator()

# Mount static files for serving generated media
if not os.path.exists("output"):
    os.makedirs("output")
app.mount("/media", StaticFiles(directory="output"), name="media")

@app.post("/generate_safe_world", response_model=SafeWorldResponse)
async def generate_safe_world(request: EmotionRequest):
    """
    Generate a complete safe world experience including story, audio, and video
    """
    try:
        world_data = generator.generate(
            user_input=request.user_input,
            include_media=request.include_media,
            duration_preference=request.duration_preference
        )
        return SafeWorldResponse(**world_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating safe world: {str(e)}")

@app.post("/generate_safe_world_quick")
async def generate_safe_world_quick(request: EmotionRequest):
    """
    Generate a safe world quickly without media (for faster responses)
    """
    try:
        quick_request = EmotionRequest(
            user_input=request.user_input,
            include_media=False
        )
        world_data = generator.generate(
            user_input=quick_request.user_input,
            include_media=False
        )
        return SafeWorldResponse(**world_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quick safe world: {str(e)}")

@app.get("/media/audio/{session_id}")
async def get_audio(session_id: str):
    """
    Serve generated audio file
    """
    audio_path = f"output/{session_id}/story_audio.mp3"
    if os.path.exists(audio_path):
        return FileResponse(
            audio_path, 
            media_type="audio/mpeg",
            filename=f"safe_world_{session_id}.mp3"
        )
    raise HTTPException(status_code=404, detail="Audio file not found")

@app.get("/media/video/{session_id}")
async def get_video(session_id: str):
    """
    Serve generated video file
    """
    video_path = f"output/{session_id}/final_video.mp4"
    if os.path.exists(video_path):
        return FileResponse(
            video_path,
            media_type="video/mp4", 
            filename=f"safe_world_{session_id}.mp4"
        )
    raise HTTPException(status_code=404, detail="Video file not found")

@app.get("/session/{session_id}/status")
async def get_session_status(session_id: str):
    """
    Check the status of media generation for a session
    """
    output_folder = f"output/{session_id}"
    
    if not os.path.exists(output_folder):
        return {"status": "not_found"}
    
    audio_exists = os.path.exists(f"{output_folder}/story_audio.mp3")
    video_exists = os.path.exists(f"{output_folder}/final_video.mp4")
    
    return {
        "status": "found",
        "audio_ready": audio_exists,
        "video_ready": video_exists,
        "audio_url": f"/media/audio/{session_id}" if audio_exists else None,
        "video_url": f"/media/video/{session_id}" if video_exists else None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Safe Worlds Generator"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Safe Worlds - AI Mental Wellness Generator", 
        "version": "2.0.0",
        "features": [
            "Emotion Analysis",
            "Therapeutic World Generation", 
            "Immersive Story Creation",
            "Audio Narration",
            "Video Visualization"
        ],
        "endpoints": {
            "generate_complete": "/generate_safe_world",
            "generate_quick": "/generate_safe_world_quick",
            "media_audio": "/media/audio/{session_id}",
            "media_video": "/media/video/{session_id}",
            "session_status": "/session/{session_id}/status"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🌟 Starting Safe Worlds API Server...")
    print("📝 Features: Emotion Analysis → World Generation → Story → Audio → Video")
    print("🔗 Access API docs at: http://127.0.0.1:8004/docs")
    uvicorn.run(app, host="127.0.0.1", port=8004)