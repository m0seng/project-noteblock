import math
import numpy as np
import samplerate
import soundfile

instrument_paths = {
    0: "sounds/harp.ogg",
    1: "sounds/basedrum.ogg",
    2: "sounds/snare.ogg",
    3: "sounds/hat.ogg",
    4: "sounds/bass.ogg",
    5: "sounds/flute.ogg",
    6: "sounds/bell.ogg",
    7: "sounds/guitar.ogg",
    8: "sounds/chime.ogg",
    9: "sounds/xylophone.ogg",
    10: "sounds/iron_xylophone.ogg",
    11: "sounds/cow_bell.ogg",
    12: "sounds/didgeridoo.ogg",
    13: "sounds/bit.ogg",
    14: "sounds/banjo.ogg",
    15: "sounds/pling.ogg",
}

class InstrumentSounds:
    '''Loads every instrument at every pitch into memory. Does not actually consume much memory.'''
    def __init__(self, block_size: int):
        self.block_size = block_size
        self.pitch_ratios = tuple(0.5 * math.pow(2, pitch/12) for pitch in range(25))
        self._sounds: dict[int, list[np.ndarray]] = {}
        for id, path in instrument_paths.items():
            self._sounds[id] = []
            sound, _ = soundfile.read(path, dtype="float64", always_2d=True) # automatically scales to [-1, 1]
            for ratio in self.pitch_ratios:
                pitched_sound = samplerate.resample(sound, ratio, "sinc_best")
                pad_length = self.block_size - (pitched_sound.shape[0] % self.block_size)
                padded_sound = np.pad(pitched_sound, pad_width=((0,pad_length),(0,0)))
                self._sounds[id].append(padded_sound)

    def get_sound(self, instrument: int, pitch: int) -> np.ndarray:
        """Get the sound data for an instrument at a given pitch. Returns a numpy array."""
        return self._sounds[instrument][pitch]