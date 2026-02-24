import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class CloudModule:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"

    def stream_chat(self, history):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=history,
            stream=True,
        )

        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content