from pydantic import BaseModel
from typing import List, TypedDict
from langchain_core.messages import BaseMessage

class EmotionRequest(BaseModel):
    """What the API expects from users"""
    user_input: str

class SafeWorldResponse(BaseModel):
    """Exact JSON format you specified"""
    emotion: str
    keywords: List[str]
    interactive_elements: List[str]
    narrative: str
    video_prompt: str
    music_prompt: str

class GraphState(TypedDict):
    """Data that flows between LangGraph nodes"""
    messages: List[BaseMessage]
    emotion: str
    keywords: List[str]
    interactive_elements: List[str]
    narrative: str
    video_prompt: str
    music_prompt: str
    world_type: str