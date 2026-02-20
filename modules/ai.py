# creed/modules/ai.py

import requests


class Module:
    def __init__(self, data_lock=None):
        self.name = "ai"          # REQUIRED for loader
        self.data_lock = data_lock
        self.model = "phi3"
        self.endpoint = "http://localhost:11434/api/chat"
        self.timeout = 20

    def chat(self, history):
        try:
            response = requests.post(
                self.endpoint,
                json={
                    "model": self.model,
                    "messages": history,
                    "stream": False
                },
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()

            if "message" in data and "content" in data["message"]:
                return data["message"]["content"]

            return "CREED: Unexpected response format."

        except requests.exceptions.ConnectionError:
            return "CREED: Ollama service is not running."

        except requests.exceptions.Timeout:
            return "CREED: Request timed out."

        except requests.exceptions.RequestException as e:
            return f"CREED: Network error: {str(e)}"

        except Exception as e:
            return f"CREED: Internal error: {str(e)}"