import json
import os
from datetime import datetime, timedelta


class Module:
    name = "memory"
    intents = ["remember", "recall", "delete", "remind"]

    def __init__(self,lock):
        self.lock = lock
        self.file = "data.json"
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump({"notes": [], "reminders": []}, f)

    def _load(self):
        with self.lock:
            with open(self.file, "r") as f:
                return json.load(f)

    def _save(self, data):
        with self.lock:
            with open(self.file, "w") as f:
                json.dump(data, f, indent=4)

    def handle(self, intent, text, context):
        data = self._load()

        # -------- REMEMBER --------
        if intent == "remember":
            lower_text = text.lower()
            index = lower_text.find("remember")
            content = text[index + len("remember"):].strip()

            if not content:
                return "What would you like me to remember?"

            if ":" in content:
                tag, note = content.split(":", 1)
                tag = tag.strip()
                note = note.strip()
            else:
                tag = "general"
                note = content.strip()

            data["notes"].append({
                "tag": tag,
                "note": note,
                "timestamp": datetime.now().isoformat()
            })

            context["last_topic"] = tag

            self._save(data)
            return f"Noted under '{tag}'."

        # -------- RECALL --------
        if intent == "recall":
            if not data["notes"]:
                return "No saved notes."

            return "\n".join(
                f"{i+1}. [{n['tag']}] {n['note']}"
                for i, n in enumerate(data["notes"])
            )

        # -------- DELETE --------
        if intent == "delete":
            try:
                index = int(text.lower().split("delete", 1)[1].strip()) - 1
                removed = data["notes"].pop(index)
                self._save(data)
                return f"Deleted: {removed['note']}"
            except:
                return "Invalid note number."

        # -------- REMIND --------
        if intent == "remind":
            content = text.lower().split("remind", 1)[1].strip()
            now = datetime.now()

            if content.startswith("in "):
                parts = content.split(" ", 2)

                if len(parts) >= 3:
                    try:
                        amount = int(parts[1])
                    except:
                        return "Invalid time amount."

                    unit = parts[2].split()[0]
                    message = content.split(" ", 2)[2]

                    if "minute" in unit:
                        target = now + timedelta(minutes=amount)
                    elif "hour" in unit:
                        target = now + timedelta(hours=amount)
                    else:
                        return "Unsupported time unit."

                    data["reminders"].append({
                        "time": target.isoformat(),
                        "message": message
                    })

                    self._save(data)
                    return f"Reminder set for {target.strftime('%H:%M:%S')}."

            return "Invalid reminder format."

        return None

    def check_reminders(self):
        data = self._load()
        now = datetime.now()

        remaining = []
        triggered = []

        for reminder in data["reminders"]:
            reminder_time = datetime.fromisoformat(reminder["time"])

            if now >= reminder_time:
                triggered.append(reminder)
            else:
                remaining.append(reminder)

        for reminder in triggered:
            print(f"\nCreed: Reminder — {reminder['message']}")

        if triggered:
            data["reminders"] = remaining
            self._save(data)

