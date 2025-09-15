from langgraph.graph import StateGraph, END
from models import GraphState
from graph_nodes import (
    analyze_emotion_node,
    generate_world_node,
    generate_story_node,
    extract_video_keywords_node,
    generate_audio_node,
    generate_video_node
)

def create_safe_world_workflow():
    """
    Create a comprehensive 6-node LangGraph workflow:
    1. Analyze emotion from user input
    2. Generate safe world based on emotion
    3. Generate immersive story
    4. Extract video keywords from story
    5. Generate audio from story
    6. Generate video from keywords
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("analyze_emotion", analyze_emotion_node)
    workflow.add_node("generate_world", generate_world_node)
    workflow.add_node("generate_story", generate_story_node)
    workflow.add_node("extract_keywords", extract_video_keywords_node)
    workflow.add_node("generate_audio", generate_audio_node)
    workflow.add_node("generate_video", generate_video_node)
    
    # Define the flow
    workflow.set_entry_point("analyze_emotion")
    workflow.add_edge("analyze_emotion", "generate_world")
    workflow.add_edge("generate_world", "generate_story")
    workflow.add_edge("generate_story", "extract_keywords")
    workflow.add_edge("extract_keywords", "generate_audio")
    workflow.add_edge("generate_audio", "generate_video")
    workflow.add_edge("generate_video", END)
    
    return workflow.compile()

# Create the compiled graph
safe_world_app = create_safe_world_workflow()