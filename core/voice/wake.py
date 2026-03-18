import pvporcupine
import sounddevice as sd
import numpy as np
import threading


class WakeWordDetector:
    def __init__(self, access_key, keyword="computer"):
        self.access_key = access_key
        self.keyword = keyword
        self._running = False
        self._thread = None

        self.porcupine = pvporcupine.create(
            access_key=self.access_key, keywords=[self.keyword]
        )

        self.sample_rate = self.porcupine.sample_rate
        self.frame_length = self.porcupine.frame_length

    def _audio_callback(self, indata, frames, time, status):
        if not self._running:
            return

        pcm = (indata[:, 0] * 32767).astype(np.int16)
        result = self.porcupine.process(pcm)

        if result >= 0:
            print("Wake word detected!")
            self.on_detect()

    def on_detect(self):
        """
        Override this method or assign externally.
        """
        pass

    def start(self):
        if self._running:
            return

        self._running = True

        def run():
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                blocksize=self.frame_length,
                dtype="float32",
                callback=self._audio_callback,
            ):
                while self._running:
                    sd.sleep(100)

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
