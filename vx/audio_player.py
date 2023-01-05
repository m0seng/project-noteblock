import queue
import numpy as np
import sounddevice as sd

class AudioPlayer:
    def __init__(self, audio_queue: queue.Queue):
        self.audio_queue = audio_queue
        self.stream = sd.OutputStream(
            samplerate=48000,
            blocksize=2400,
            device="Speakers (Realtek High Definition Audio(SST)), Windows DirectSound", # TODO: change this lmao
            callback=self.sd_callback)
        self.stream.start()

    def sd_callback(self, outdata: np.ndarray, frames: int, time, status):
        try:
            data = self.audio_queue.get_nowait()
        except queue.Empty as e:
            print("no audio data, filling with blanks...")
            outdata.fill(0)
            return
        outdata[:] = data