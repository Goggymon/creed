from fastapi import FastAPI
from core.engine import CreedEngine

app = FastAPI()

engine = CreedEngine()


@app.get("/")
def health_check():
    return {"status": "CREED backend online"}


@app.post("/chat")
def chat(payload: dict):
    message = payload.get("message", "")

    if not message:
        return {"response": "No message provided."}

    response = engine.ai_module.chat([
        {"role": "user", "content": message}
    ])

    return {"response": response}