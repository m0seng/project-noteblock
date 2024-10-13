from abc import ABC, abstractmethod

from note import Note

class Effect(ABC):
    """Effect interface. You should be able to tick(notes) any Effect."""
    @abstractmethod
    def tick(self, notes: list[Note]) -> list[Note]:
        """Returns a modified list of notes based on the effect."""
        pass

class SimpleSlapbackEffect(Effect):
    def __init__(self, ratio: float = 0.8):
        self.ratio = ratio
        self.last_notes = []

    def tick(self, notes: list[Note]):
        new_notes = notes + [note.altered_copy(volume=note.volume*self.ratio) for note in self.last_notes]
        self.last_notes = notes
        return new_notes