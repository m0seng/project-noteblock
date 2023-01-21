import math
import numpy as np
import samplerate
import soundfile

instrument_paths = {
    0: "sounds/wav/harp.wav",
    1: "sounds/wav/basedrum.wav",
    2: "sounds/wav/snare.wav",
    3: "sounds/wav/hat.wav",
    4: "sounds/wav/bass.wav",
    5: "sounds/wav/flute.wav",
    6: "sounds/wav/bell.wav",
    7: "sounds/wav/guitar.wav",
    8: "sounds/wav/chime.wav",
    9: "sounds/wav/xylophone.wav",
    10: "sounds/wav/iron_xylophone.wav",
    11: "sounds/wav/cow_bell.wav",
    12: "sounds/wav/didgeridoo.wav",
    13: "sounds/wav/bit.wav",
    14: "sounds/wav/banjo.wav",
    15: "sounds/wav/pling.wav",
}

class InstrumentSounds:
    '''Loads every instrument at every pitch into memory. Does not actually consume much memory.'''
    def __init__(self, block_size: int):
        self.block_size = block_size
        self.pitch_ratios = tuple(2 * math.pow(2, -pitch/12) for pitch in range(25))
        self._sounds: dict[int, list[np.ndarray]] = {}
        for id, path in instrument_paths.items():
            print(f"loading instrument id {id}...")
            self._sounds[id] = []
            sound, _ = soundfile.read(path, dtype="float64", always_2d=True) # automatically scales to [-1, 1]
            for ratio in self.pitch_ratios:
                pitched_sound = samplerate.resample(sound, ratio, "sinc_best")
                pad_length = self.block_size - (pitched_sound.shape[0] % self.block_size)
                padded_sound = np.pad(pitched_sound, pad_width=((0,pad_length),(0,0)))
                self._sounds[id].append(padded_sound)
                # print(f"loaded instrument id {id} with ratio {ratio}")

    def get_sound(self, instrument: int, pitch: int) -> np.ndarray:
        """Get the sound data for an instrument at a given pitch. Returns a numpy array."""
        return self._sounds[instrument][pitch]