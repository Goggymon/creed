import requests


class Module:
    name = "ai"
    intents = []

    def __init__(self, lock):
        self.lock = lock
        self.host = "http://192.168.68.60:11434"  

    def chat(self, history):
        # ----- SYSTEM PROMPT -----
        system_prompt = {
            "role": "system",
            "content": (
                "You are Creed, a modular AI assistant built for productivity and clarity. "
                "Be concise. Avoid unnecessary verbosity. "
                "Maintain context from previous messages. "
                "If unsure, ask for clarification."
            )
        }

        # ----- SLIDING WINDOW -----
        # Take last 6 messages max (3 exchanges)
        window = history[-6:] if len(history) > 6 else history

        messages = [system_prompt] + window
        response = requests.post(
            f"{self.host}/api/chat",
            json={
                "model": "phi3",   # or whatever model you’re using
                "messages": messages,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()
        return response.json()["message"]["content"]

