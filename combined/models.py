from pydantic import BaseModel
from typing import List, TypedDict, Optional
from langchain_core.messages import BaseMessage

class EmotionRequest(BaseModel):
    """What the API expects from users"""
    user_input: str
    include_media: bool = True  # Whether to generate audio/video
    duration_preference: str = "short"  # short, medium, long

class MediaContent(BaseModel):
    """Media files generated for the safe world"""
    story_text: Optional[str] = None
    audio_path: Optional[str] = None
    video_path: Optional[str] = None
    video_url: Optional[str] = None  # Pexels video URL
    audio_duration: Optional[float] = None

class SafeWorldResponse(BaseModel):
    """Complete safe world with all generated content"""
    emotion: str
    keywords: List[str]
    interactive_elements: List[str]
    narrative: str
    video_prompt: str
    music_prompt: str
    world_type: str
    # New fields for complete experience
    generated_story: Optional[str] = None
    media_content: Optional[MediaContent] = None
    session_id: str
    created_at: str

class GraphState(TypedDict):
    """Enhanced state that flows between all nodes"""
    # Original fields
    messages: List[BaseMessage]
    emotion: str
    keywords: List[str]
    interactive_elements: List[str]
    narrative: str
    video_prompt: str
    music_prompt: str
    world_type: str
    
    # New fields for complete workflow
    generated_story: str
    story_keywords: List[str]  # Keywords extracted from story for video search
    media_content: dict
    session_id: str
    include_media: bool
    duration_preference: str
    
    # Processing status
    story_generated: bool
    audio_generated: bool
    video_generated: bool