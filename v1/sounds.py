import math
import numpy as np
import samplerate
import soundfile

from instrument import Instrument, instruments

class Sounds():
    '''Loads every instrument at every pitch into memory. Does not actually consume much memory.'''
    def __init__(self, block_size: int):
        self.block_size = block_size
        self.pitch_ratios = tuple(0.5 * math.pow(2, pitch/12) for pitch in range(25))
        self._sounds: dict[int, list[np.ndarray]] = {}
        for instrument in instruments:
            self._sounds[instrument.id] = []
            sound, _ = soundfile.read(instrument.path, dtype="float64", always_2d=True) # automatically scales to [-1, 1]
            for ratio in self.pitch_ratios:
                pitched_sound = samplerate.resample(sound, ratio, "sinc_best")
                pad_length = self.block_size - (pitched_sound.shape[0] % self.block_size)
                padded_sound = np.pad(pitched_sound, pad_width=((0,pad_length),(0,0)))
                self._sounds[instrument.id].append(padded_sound)

    def get_sound(self, instrument: Instrument, pitch: int) -> np.ndarray:
        """Get the sound data for an instrument at a given pitch. Returns a numpy array."""
        return self._sounds[instrument.id][pitch]