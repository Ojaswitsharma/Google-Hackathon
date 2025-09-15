from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
import json
import re
from dhairya.models import GraphState
from dhairya.prompts import EMOTION_ANALYSIS_PROMPT, WORLD_GENERATION_PROMPT

# Initialize LLM (shared across nodes)
llm = ChatOpenAI(
    base_url="http://192.168.1.12:1234/v1",
    api_key="not-needed",
    model="mistral-7b-instruct-v0.3"
)

def analyze_emotion_node(state: GraphState) -> GraphState:
    """
    LangGraph Node 1: Analyze user's emotional state
    """
    print("--- ANALYZING EMOTION ---")
    
    user_input = state['messages'][-1].content
    
    prompt = PromptTemplate(
        template=EMOTION_ANALYSIS_PROMPT,
        input_variables=["user_input"]
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        response = chain.invoke({"user_input": user_input})
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            state['emotion'] = result.get('emotion', 'neutral')
            state['keywords'] = result.get('keywords', ['calm'])
        else:
            # Fallback emotion detection
            state['emotion'] = _detect_emotion_fallback(user_input)
            state['keywords'] = ['peace']
            
    except Exception as e:
        print(f"Error in emotion analysis: {e}")
        state['emotion'] = 'neutral'
        state['keywords'] = ['calm']
    
    return state

def generate_world_node(state: GraphState) -> GraphState:
    """
    LangGraph Node 2: Generate the safe world based on emotion analysis
    """
    print("--- GENERATING SAFE WORLD ---")
    
    user_input = state['messages'][0].content
    emotion = state['emotion']
    keywords = state['keywords']
    
    prompt = PromptTemplate(
        template=WORLD_GENERATION_PROMPT,
        input_variables=["user_input", "emotion", "keywords"]
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        response = chain.invoke({
            "user_input": user_input,
            "emotion": emotion,
            "keywords": ', '.join(keywords)
        })
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            state['world_type'] = result.get('world_type', 'forest')
            state['interactive_elements'] = result.get('interactive_elements', [])
            state['narrative'] = result.get('narrative', '')
            state['video_prompt'] = result.get('video_prompt', '')
            state['music_prompt'] = result.get('music_prompt', '')
        else:
            # Fallback world generation
            _create_fallback_world(state)
            
    except Exception as e:
        print(f"Error in world generation: {e}")
        _create_fallback_world(state)
    
    return state

def _detect_emotion_fallback(user_input: str) -> str:
    """Simple keyword-based emotion detection for fallback"""
    input_lower = user_input.lower()
    
    if any(word in input_lower for word in ["anxious", "worry", "nervous", "overwhelm"]):
        return "anxiety" 
    elif any(word in input_lower for word in ["sad", "depressed", "down", "hurt"]):
        return "sadness"
    elif any(word in input_lower for word in ["angry", "mad", "frustrated"]):
        return "anger"
    elif any(word in input_lower for word in ["lonely", "alone", "isolated"]):
        return "lonely"
    elif any(word in input_lower for word in ["excited", "happy", "amazing"]):
        return "joy"
    else:
        return "neutral"

def _create_fallback_world(state: GraphState):
    """Create fallback world when LLM generation fails"""
    emotion = state['emotion']
    
    world_map = {
        "anxiety": "forest",
        "sadness": "garden", 
        "anger": "mountain",
        "lonely": "garden",
        "joy": "fantasy",
        "neutral": "forest"
    }
    
    world_type = world_map.get(emotion, "forest")
    
    state['world_type'] = world_type
    state['interactive_elements'] = [
        f"a peaceful spot to rest in the {world_type}",
        "gentle sounds of nature",
        "soft, calming light"
    ]
    state['narrative'] = f"You enter a serene {world_type} where every breath brings you peace and every moment helps you feel more centered."
    state['video_prompt'] = f"A beautiful, peaceful {world_type} with soft lighting and gentle movement"
    state['music_prompt'] = f"Calming {world_type} ambience with natural sounds and peaceful atmosphere"
