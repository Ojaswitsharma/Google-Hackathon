from langchain_core.messages import HumanMessage
from dhairya.models import GraphState
from dhairya.langgraph_workflow import safe_world_app

class SafeWorldGenerator:
    """Main class that orchestrates safe world generation"""
    
    def __init__(self):
        self.app = safe_world_app
    
    def generate(self, user_input: str) -> dict:
        """Public method that returns your exact JSON format"""
        
        # Create initial state
        initial_state = GraphState(
            messages=[HumanMessage(content=user_input)],
            emotion="",
            keywords=[],
            interactive_elements=[],
            narrative="",
            video_prompt="",
            music_prompt="",
            world_type=""
        )
        
        try:
            # Execute LangGraph workflow
            final_state = self.app.invoke(initial_state)
            
            # Return in your specified format
            return {
                "emotion": final_state.get("emotion", "neutral"),
                "keywords": final_state.get("keywords", ["peace"]),
                "interactive_elements": final_state.get("interactive_elements", []),
                "narrative": final_state.get("narrative", "You find yourself in a peaceful space."),
                "video_prompt": final_state.get("video_prompt", "A serene landscape."),
                "music_prompt": final_state.get("music_prompt", "Calming ambient sounds.")
            }
            
        except Exception as e:
            print(f"Error in workflow: {e}")
            return self._create_fallback_response()