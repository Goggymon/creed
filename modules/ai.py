import requests


class Module:
    name = "ai"
    intents = []

    def __init__(self, lock):
        self.lock = lock
        self.host = "http://192.168.68.60:11434"  

    def chat(self, history):
        response = requests.post(
            f"{self.host}/api/chat",
            json={
                "model": "phi3",
                "messages": [
                    {"role": "user", "content": history[-1]["content"]}
                ],
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()
        return response.json()["message"]["content"]
