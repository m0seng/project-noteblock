from dataclasses import dataclass
import copy
import numpy as np

from instrument import Instrument, harp

@dataclass(slots=True)
class Note:
    '''A class representing a note from a Minecraft note block.

    Contains additional metadata to be used by other components.
    '''
    instrument: Instrument = harp
    pitch: int = 0
    volume: float = 1 # 0 to 1
    pan: float = 0 # -1 to 1
    sustain: int = 1
    is_main: bool = True

    def altered_copy(self, **kwargs) -> "Note":
        '''Return a copy of the note, with modified attributes based on keyword arguments.'''
        new_note = copy.copy(self) # deepcopy will duplicate instrument objects!
        for k, v in kwargs.items():
            if hasattr(new_note, k):
                setattr(new_note, k, v)
        return new_note

    def stereo_volumes(self) -> np.ndarray:
        """Return the volumes of the left and right channels as a numpy array."""
        vol_left = self.volume * max(1 - self.pan, 1)
        vol_right = self.volume * max(1 + self.pan, 1)
        return np.array([vol_left, vol_right], dtype=np.float64)