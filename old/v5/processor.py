from abc import ABC, abstractmethod
from .savable import Savable
from .note import Note

# props = stuff that gets saved
# state = stuff that doesn't

# mono_tick: always goes up, has lookahead
# seq_tick: tick in sequence, can go back
# is_next: still going up?
# rt_tick: mono_tick but no lookahead

# use with statement to modify props from outside!

class Processor(Savable, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_props()
        self.init_state()

    @abstractmethod
    def init_props(self):
        ...

    @abstractmethod
    def init_state(self):
        ...

    @abstractmethod
    def audio_tick(self, notes: list[Note] = [], mono_tick: int = 0, seq_tick: int = 0, is_next: bool = True) -> list[Note]:
        ...

    @abstractmethod
    def visual_tick(self, rt_tick: int = 0):
        """trigger visual event at the end?"""
        ...