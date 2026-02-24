from fastapi import FastAPI
from core.engine import CreedEngine
from fastapi.responses import StreamingResponse

app = FastAPI()

engine = CreedEngine()


@app.get("/")
def health_check():
    return {"status": "CREED backend online"}

@app.post("/chat")
def chat(payload: dict):
    message = payload.get("message", "")

    def generator():
        for token in engine.stream_response(message):
            yield token

    return StreamingResponse(generator(), media_type="text/plain")