import math
import numpy as np
import samplerate
import soundfile
from instrument import instruments

block_size = 2048
pitch_ratios = tuple(0.5 * math.pow(2, pitch/12) for pitch in range(25))
_sounds: dict[int, list[np.ndarray]] = {}
for id, instrument in instruments.items():
    _sounds[id] = []
    sound, _ = soundfile.read(instrument.path, dtype="float64", always_2d=True) # automatically scales to [-1, 1]
    for ratio in pitch_ratios:
        pitched_sound = samplerate.resample(sound, ratio, "sinc_best")
        pad_length = block_size - (pitched_sound.shape[0] % block_size)
        padded_sound = np.pad(pitched_sound, pad_width=((0,pad_length),(0,0)))
        _sounds[id].append(padded_sound)

def get_sound(instrument: int, pitch: int) -> np.ndarray:
    return _sounds[instrument][pitch]