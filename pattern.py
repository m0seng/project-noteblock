from abc import ABC, abstractmethod
import random

from note import Note

class Pattern(ABC):
    """Pattern interface. You should be able to get_notes(timestamp) from any Pattern."""
    @abstractmethod
    def get_notes(self, timestamp: int) -> list[Note]:
        pass

class DummyPattern(Pattern):
    """Dummy pattern which returns notes with random pitch/volume/pan."""
    def __init__(self, ticks_per_note: int = 10):
        self.ticks_per_note = ticks_per_note

    def get_notes(self, timestamp: int):
        if timestamp % self.ticks_per_note == 0:
            return [Note(
                pitch=random.randint(0, 24),
                volume=random.random(),
                pan=(random.random()*2)-1)]
        else:
            return []