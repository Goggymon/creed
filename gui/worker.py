import requests
from PySide6.QtCore import QThread, Signal


class ChatWorker(QThread):
    new_token = Signal(str)
    finished_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message
        self._running = True

    def run(self):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"message": self.message},
                stream=True,
            )

            for chunk in response.iter_content(chunk_size=None):
                if not self._running:
                    break
                if chunk:
                    token = chunk.decode("utf-8")
                    self.new_token.emit(token)

            self.finished_signal.emit()

        except Exception as e:
            self.error_signal.emit(str(e))

    def stop(self):
        self._running = False
