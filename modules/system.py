from datetime import datetime


class Module:
    name = "system"
    intents = ["time","hello"]

    def __init__(self,lock):
        self.lock = lock

    def handle(self, intent, text, context):
        if intent == "time":
            from datetime import datetime
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}."

        if intent == "hello":
            return "Hello."

        return None


