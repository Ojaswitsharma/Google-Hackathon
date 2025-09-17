import uuid
import time
from datetime import datetime
from langchain_core.messages import HumanMessage
from models import GraphState, MediaContent
from langgraph_workflow import safe_world_app

class SafeWorldGenerator:
    """Main class that orchestrates complete safe world generation"""
    
    def __init__(self):
        self.app = safe_world_app
    
    def generate(self, user_input: str, include_media: bool = True, duration_preference: str = "short") -> dict:
        """
        Generate a complete safe world experience
        
        Args:
            user_input: User's emotional input
            include_media: Whether to generate audio/video
            duration_preference: "short", "medium", or "long"
        
        Returns:
            Complete safe world data with all generated content
        """
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().isoformat()
        
        # Create initial state
        initial_state = GraphState(
            messages=[HumanMessage(content=user_input)],
            emotion="",
            keywords=[],
            interactive_elements=[],
            narrative="",
            video_prompt="",
            music_prompt="",
            world_type="",
            generated_story="",
            story_keywords=[],
            media_content={},
            session_id=session_id,
            include_media=include_media,
            duration_preference=duration_preference,
            story_generated=False,
            audio_generated=False,
            video_generated=False
        )
        
        try:
            print(f"\n🌟 Starting Safe World Generation (Session: {session_id})")
            print(f"📝 User Input: {user_input}")
            print(f"🎬 Include Media: {include_media}")
            print(f"⏱️ Duration: {duration_preference}")
            
            # Execute complete LangGraph workflow
            final_state = self.app.invoke(initial_state)
            
            # Build media content object
            media_content = None
            if include_media and final_state.get('media_content'):
                media_content = MediaContent(
                    story_text=final_state.get('generated_story'),
                    audio_path=final_state['media_content'].get('audio_path'),
                    video_path=final_state['media_content'].get('video_path'),
                    video_url=final_state['media_content'].get('video_url'),
                    audio_duration=final_state['media_content'].get('audio_duration')
                )
            
            # Return complete response
            response = {
                "emotion": final_state.get("emotion", "neutral"),
                "keywords": final_state.get("keywords", ["peace"]),
                "interactive_elements": final_state.get("interactive_elements", []),
                "narrative": final_state.get("narrative", "You find yourself in a peaceful space."),
                "video_prompt": final_state.get("video_prompt", "A serene landscape."),
                "music_prompt": final_state.get("music_prompt", "Calming ambient sounds."),
                "world_type": final_state.get("world_type", "forest"),
                "generated_story": final_state.get("generated_story"),
                "media_content": media_content.dict() if media_content else None,
                "session_id": session_id,
                "created_at": timestamp
            }
            
            # Print generation summary
            self._print_generation_summary(response, final_state)
            
            return response
            
        except Exception as e:
            print(f"❌ Error in workflow: {e}")
            return self._create_fallback_response(session_id, timestamp)
    
    def _create_fallback_response(self, session_id: str, timestamp: str) -> dict:
        """Create a fallback response when generation fails"""
        return {
            "emotion": "neutral",
            "keywords": ["peace", "calm"],
            "interactive_elements": [
                "a quiet place to breathe",
                "gentle sounds of nature",
                "warm, soft lighting"
            ],
            "narrative": "You find yourself in a peaceful sanctuary where you can rest and recharge.",
            "video_prompt": "A beautiful, serene natural landscape",
            "music_prompt": "Gentle ambient sounds with nature",
            "world_type": "forest",
            "generated_story": "You step into a tranquil forest clearing where sunlight filters through the leaves. The gentle sounds of nature surround you as you find a comfortable place to rest. With each breath, you feel more peaceful and centered. This is your safe space, where you can always return when you need calm.",
            "media_content": None,
            "session_id": session_id,
            "created_at": timestamp
        }
    
    def _print_generation_summary(self, response: dict, final_state: dict):
        """Print a summary of what was generated"""
        print(f"\n✅ Safe World Generation Complete!")
        print(f"🎭 Detected Emotion: {response['emotion']}")
        print(f"🌍 Generated World: {response['world_type']}")
        print(f"🔑 Keywords: {', '.join(response['keywords'])}")
        
        if response.get('generated_story'):
            print(f"📖 Story Generated: ✅ ({len(response['generated_story'].split())} words)")
        
        if response.get('media_content'):
            media = response['media_content']
            if media.get('audio_path'):
                print(f"🎵 Audio Generated: ✅ ({media.get('audio_duration', 0):.1f}s)")
            if media.get('video_path'):
                print(f"🎬 Video Generated: ✅")
            
        print(f"📁 Session ID: {response['session_id']}")
        print("-" * 50)