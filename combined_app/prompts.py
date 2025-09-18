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

STORY_GENERATION_PROMPT = """You are a therapeutic storyteller creating immersive healing narratives for youth.

Create a COMPLETE calming, immersive story based on:
WORLD TYPE: {world_type}
EMOTION: {emotion} 
NARRATIVE THEME: {narrative}

The story should be approximately {min_words}-{max_words} words and MUST:
- Use second person ("You find yourself...")
- Be present tense and immersive
- Focus on sensory details (what you see, hear, feel)
- Include gentle, healing imagery
- End with a COMPLETE sentence expressing peace and empowerment
- Avoid any negative or triggering content
- NEVER cut off mid-sentence or mid-thought

IMPORTANT: Ensure your story has a proper ending with complete sentences. Do not stop abruptly.

Create a story that makes the reader feel transported to this safe world and ends with closure and peace."""

KEYWORD_EXTRACTION_PROMPT = """From the following story, extract 1-2 keywords that are:
- Concrete, visual objects or scenes
- Suitable for finding beautiful, peaceful stock videos
- NOT negative, violent, or depressing
- Examples: forest, ocean, sunrise, flowers, mountains, clouds

Story: {text}

Return only the keywords separated by commas, nothing else."""