EMOTION_ANALYSIS_PROMPT = """You are an emotion analysis AI for youth mental wellness.

Analyze this input and identify the main emotion and key words:

USER INPUT: "{user_input}"

Choose the primary emotion from: anxiety, sadness, anger, joy, overwhelm, lonely, excited, neutral

Extract 1-3 keywords that capture their feelings.

Return ONLY a JSON object:
{{
  "emotion": "primary_emotion_here",
  "keywords": ["word1", "word2"]
}}"""

WORLD_GENERATION_PROMPT = """You are a therapeutic world designer. Create a calming safe world.

EMOTION: {emotion}
KEYWORDS: {keywords}
USER INPUT: "{user_input}"

Choose world type based on emotion:
- Forest: anxiety, overwhelm (grounding)
- Ocean: sadness, grief (release)
- Mountain: anger, frustration (strength)
- Garden: loneliness (growth, nurturing)
- City: disconnection (community)
- Fantasy: feeling trapped (magic, possibility)
- Space: feeling insignificant (perspective)

Return ONLY a JSON object:
{{
  "world_type": "chosen_type",
  "interactive_elements": ["element1", "element2", "element3"],
  "narrative": "2-3 sentence calming journey.",
  "video_prompt": "Simple scene description.",
  "music_prompt": "Calming audio description."
}}"""