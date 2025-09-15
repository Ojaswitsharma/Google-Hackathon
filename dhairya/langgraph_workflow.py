from langgraph.graph import StateGraph, END
from dhairya.models import GraphState
from dhairya.graph_nodes import analyze_emotion_node, generate_world_node

def create_safe_world_workflow():
    """
    Create a simple 2-node LangGraph workflow:
    1. Analyze emotion from user input
    2. Generate safe world based on emotion
    """
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("analyze_emotion", analyze_emotion_node)
    workflow.add_node("generate_world", generate_world_node)
    
    # Define the flow
    workflow.set_entry_point("analyze_emotion")
    workflow.add_edge("analyze_emotion", "generate_world")
    workflow.add_edge("generate_world", END)
    
    return workflow.compile()

# Create the compiled graph
safe_world_app = create_safe_world_workflow()