import os
import importlib
from pydoc import text
import threading
import time
from datetime import datetime
from urllib import response
from core.router import IntentRouter

class CreedEngine:
    def __init__(self):
        self.modules = {}
        self.router = IntentRouter()
        self.running = False
        self.context = {
            "last_intent": None,
            "last_module": None,
            "last_topic":None
        }  
        self.history = []
        self.data_lock = threading.Lock() 
        self.ai_module = None
        self.auto_load_modules()

    def auto_load_modules(self, folder="modules"):
        if not os.path.exists(folder):
            print(f"[!] Modules folder '{folder}' not found.")
            return

        for file in os.listdir(folder):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = file[:-3]
                module_path = f"{folder}.{module_name}"

                try:
                    module = importlib.import_module(module_path)

                    if hasattr(module, "Module"):
                       instance = module.Module(self.data_lock)
                       self.modules[instance.name] = instance

                       if instance.name == "ai":
                           self.ai_module = instance

                       if hasattr(instance, "intents"):
                           for intent in instance.intents:
                               self.router.register(intent, instance)

                       print(f"[+] Auto-loaded module: {instance.name}")

                    else:
                        print(f"[WARNING] Module '{module_name}' has no 'Module' class.")

                except Exception as e:
                    print(f"[ERROR] Failed to load module '{module_name}': {e}")

    def handle_input(self, text):
        text = text.strip()

        if text.lower() == "exit":
            return "Creed shutting down.", False

    # Store user message
        self.history.append({"role": "user", "content": text})

        intent, module = self.router.dispatch(text)

        response = None

        if module:
            response = module.handle(intent, text, self.context)

            self.context["last_intent"] = intent
            self.context["last_module"] = module.name

        if not response:
            if self.ai_module:
                response = self.ai_module.chat(self.history)
            else:
                response = "I don't understand that yet."

    # Store assistant response
        self.history.append({"role": "assistant", "content": response})

        return response, True



    def input_available(self):
        return True

    def check_reminders(self):
        now = datetime.now().strftime("%H:%M")

        for module in self.modules.values():
            if hasattr(module, "check_reminders"):
                module.check_reminders()


    def run(self):
        print("\n[Creed] Ready.\n")

        self.running = True

        # Start reminder thread
        thread = threading.Thread(target=self.reminder_worker, daemon=True)
        thread.start()

        try:
            while self.running:
                user_input = input("> ")

                response, continue_flag = self.handle_input(user_input)

                print(f"Creed: {response}")

                self.running = continue_flag

        except KeyboardInterrupt:
            print("\nCreed shutting down.")
            self.running = False


    def reminder_worker(self):
        while self.running:
            for module in self.modules.values():
                if hasattr (module, "check_reminders"):
                    module.check_reminders()
            time.sleep(3)
