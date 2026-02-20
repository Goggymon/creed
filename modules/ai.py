import requests
from requests.exceptions import RequestException, Timeout

print("Using new AI handler")

def chat(self, history):
    system_prompt = {
        "role": "system",
        "content": (
            "You are Creed, a modular AI assistant. "
            "Be concise. Maintain context. "
            "If unsure, ask for clarification."
        )
    }

    # Sliding window (last 2 exchanges max for speed)
    window = history[-4:] if len(history) > 4 else history
    messages = [system_prompt] + window

    payload = {
        "model": "phi3",
        "messages": messages,
        "stream": False,
        "options": {
            "num_predict": 150,
            "temperature": 0.6
        }
    }

    try:
        response = requests.post(
            f"{self.host}/api/chat",
            json=payload,
            timeout=20
        )

        response.raise_for_status()
        return response.json()["message"]["content"]

    except requests.exceptions.Timeout:
        return "AI response timed out. Please try again."

    except requests.exceptions.ConnectionError:
        return "AI service is currently unavailable."

    except requests.exceptions.RequestException:
        return "AI request failed."

    except Exception:
        return "Unexpected AI error occurred."



class Module:
    name = "ai"
    intents = []

    def __init__(self, lock):
        self.lock = lock
        self.host = "http://localhost:11434"  

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
        window = history[-2:] if len(history) > 2 else history

        messages = [system_prompt] + window
        response = requests.post(
            f"{self.host}/api/chat",
            json={
                "model": "phi3",
                "messages": messages,
                "stream": False,
                "options": {
                    "num_predict": 150,
                    "temperature": 0.6
                }
            }
        )

        response.raise_for_status()
        return response.json()["message"]["content"]

