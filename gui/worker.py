import token

from PySide6.QtCore import QThread, Signal
import requests


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

            print("STATUS:", response.status_code)

            for chunk in response.iter_content(chunk_size=1):

                if not self._running:
                    break

                if chunk:
                    token = chunk.decode("utf-8", errors="ignore")
                    self.new_token.emit(token)
            self.finished_signal.emit()

        except Exception as e:
            self.error_signal.emit(str(e))

    def stop(self):
        self._running = False
