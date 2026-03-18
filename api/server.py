from fastapi import FastAPI
from core.engine import CreedEngine
from fastapi.responses import StreamingResponse
from core.voice.wake import WakeWordDetector

app = FastAPI()
wake = WakeWordDetector(
    access_key="cqTOEYXYiQZbeRszo/tSaaAmjCcwcEsSCP2F5kCublmVUllIKXRILA==",
    keyword="computer",
)
engine = CreedEngine()


@app.get("/")
def health_check():
    return {"status": "CREED backend online"}


@app.post("/chat")
def chat(payload: dict):
    message = payload.get("message", "")

    def generator():
        for token in engine.stream_response(message):
            print("BACKEND TOKEN:", token)
            yield token

    return StreamingResponse(
        generator(),
        media_type="text/plain; charset=utf-8",
        headers={"Transfer-Encoding": "chunked"},
    )


def handle_wake():
    print(">>> WAKE TRIGGERED IN BACKEND <<<")


wake.on_detect = handle_wake
wake.start()
