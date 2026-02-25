import threading
from modules.cloud import CloudModule
from modules.tts import TTSModule
from core.router import IntentRouter


class CreedEngine:
    def __init__(self):
        self.router = IntentRouter()
        self.running = False

        self.history = []
        self.context = {}

        self.cloud = CloudModule()
        self.tts = TTSModule()

        self.modules = {}
        self.router = IntentRouter()
        self.lock = threading.Lock()
        self.load_modules()

        # Personality system prompt
        self.history.append(
            {
                "role": "system",
                "content": (
                    "You are CREED, a sharp and intelligent AI assistant. "
                    "Respond concisely but clearly. "
                    "Use 2–4 short sentences unless detailed explanation is requested."
                ),
            }
        )

    def stream_response(self, text):
        self.history.append({"role": "user", "content": text})

        full_response = ""

        try:
            for token in self.cloud.stream_chat(self.history):
                full_response += token
                yield token

            self.history.append({"role": "assistant", "content": full_response})

        except Exception as e:
            yield f"\n[Cloud Error] {str(e)}"

    def run(self):
        print("\n[Creed] Ready.\n")
        self.running = True

        while self.running:
            user_input = input("> ")

            if user_input.strip().lower() == "exit":
                self.tts.stop()
                print("Creed shutting down.")
                break

            # Interrupt any current speech
            self.tts.stop()

            print("Creed: ", end="", flush=True)

            spoken_buffer = ""

            for token in self.stream_response(user_input):
                print(token, end="", flush=True)
                spoken_buffer += token

                # Speak only complete sentences
                if spoken_buffer.strip().endswith((".", "?", "!")):
                    self.tts.speak(spoken_buffer.strip())
                    spoken_buffer = ""

            if spoken_buffer.strip():
                self.tts.speak(spoken_buffer.strip())

            print()

    def load_modules(self):
        from modules.memory import Module as MemoryModule
        from modules.system import Module as SystemModule

        memory = MemoryModule(self.lock)
        system = SystemModule(self.lock)

        self.modules["memory"] = memory
        self.modules["system"] = system

        for module in self.modules.values():
            for intent in getattr(module, "intents", []):
                self.router.register(intent, module)

        print("[+] Modules loaded:", ", ".join(self.modules.keys()))
