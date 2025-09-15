from fastapi import FastAPI
from dhairya.models import EmotionRequest, SafeWorldResponse
from dhairya.world_generator import SafeWorldGenerator

app = FastAPI()
generator = SafeWorldGenerator()

@app.post("/generate_safe_world", response_model=SafeWorldResponse)
async def generate_safe_world(request: EmotionRequest):
    world_data = generator.generate(request.user_input)
    return SafeWorldResponse(**world_data)

@app.get("/")
async def root():
    return {"message": "LangGraph Safe World Generator API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8004)