import numpy as np

from note import Note
from instrument_sounds import InstrumentSounds

# NOTE: this code is reliant on block size being 1/20th of a second
# this is fine and it works but is something to keep in mind

class AudioGenerator():
    """Turns lists of Notes into blocks of audio."""
    
    def __init__(self, block_size: int, sounds: InstrumentSounds):
        self.block_size = block_size
        self.sounds = sounds
        self.current_sounds: list[tuple[np.ndarray, int]] = []

    def tick(self, notes: list[Note]) -> np.ndarray:
        self.process_new_notes(notes)
        return self.tick_audio()
        
    def process_new_notes(self, notes: list[Note]):
        for note in notes:
            sound = self.sounds.get_sound(note.instrument, note.pitch) * self.stereo_volumes(note)
            self.current_sounds.append((sound, 0))

    def tick_audio(self) -> np.ndarray:
        block = np.zeros((self.block_size, 2), dtype=np.float64)
        new_current_sounds = []
        for sound, start_index in self.current_sounds:
            end_index = start_index + self.block_size
            block += sound[start_index:end_index]
            if end_index < sound.shape[0]:
                new_current_sounds.append((sound, end_index))
        self.current_sounds = new_current_sounds
        return block

    def stereo_volumes(self, note: Note) -> np.ndarray:
        """Return the volumes of the left and right channels as a numpy array."""
        vol_left = note.volume * max(1 - note.pan, 1)
        vol_right = note.volume * max(1 + note.pan, 1)
        return np.array([vol_left, vol_right], dtype=np.float64)