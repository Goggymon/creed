import subprocess
import threading
import queue
import sounddevice as sd
import numpy as np


class TTSModule:
    def __init__(self):
        self.queue = queue.Queue()
        self.sample_rate = 22050

        self.piper_path = r"D:\CREED\piper\piper.exe"
        self.model_path = r"D:\CREED\piper\voices\en_US-ryan-medium.onnx"

        self.worker = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker.start()

    def speak(self, text):
        clean_text = (
            text.replace("*", "")
                .replace(":", ".")
                .replace("#", "")
        )
        self.queue.put(clean_text)

    def stop(self):
        # Just clear queue; run() will handle interruption
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except queue.Empty:
                break

    def _worker_loop(self):
        while True:
            text = self.queue.get()
            if text is None:
                break

            try:
                result = subprocess.run(
                    [
                        self.piper_path,
                        "-m", self.model_path,
                        "--output-raw",
                        "--quiet"
                    ],
                    input=(text + "\n").encode("utf-8"),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL
                )

                audio = result.stdout

                if audio:
                    audio_np = np.frombuffer(audio, dtype=np.int16)
                    sd.play(audio_np, self.sample_rate)
                    sd.wait()

            except Exception as e:
                print("TTS Error:", e)

            self.queue.task_done()