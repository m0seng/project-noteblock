import math
import numpy as np
import samplerate
import soundfile
from instrument import instruments

class SoundLoader:
    '''Loads every instrument at every pitch into memory. Does not actually consume much memory.'''
    def __init__(self, block_size: int = 2048):
        self.block_size = block_size
        self.pitch_ratios = tuple(0.5 * math.pow(2, pitch/12) for pitch in range(25))
        self._sounds: dict[int, list[np.ndarray]] = {}
        for id, instrument in instruments.items():
            self._sounds[id] = []
            sound, _ = soundfile.read(instrument.path, dtype="float64", always_2d=True) # automatically scales to [-1, 1]
            for ratio in self.pitch_ratios:
                pitched_sound = samplerate.resample(sound, ratio, "sinc_best")
                self._sounds[id].append(pitched_sound)

    def get_sound(self, instrument: int, pitch: int) -> np.ndarray:
        """Get the sound data for an instrument at a given pitch. Returns a numpy array."""
        return self._sounds[instrument][pitch]