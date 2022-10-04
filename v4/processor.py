from abc import ABC, abstractmethod
from .savable import Savable
from .note import Note
from .event import Event

# props = stuff that gets saved
# state = stuff that doesn't

# mono_tick: always goes up, has lookahead
# seq_tick: tick in sequence, can go back
# rt_tick: mono_tick but no lookahead

# use with statement to modify props from outside!

class Processor(Savable, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_props()
        self.init_state()
        self.visual_event = Event()

    @abstractmethod
    def init_props(self):
        ...

    @abstractmethod
    def init_state(self):
        ...

    @abstractmethod
    def audio_tick(self, input: list[Note] = [], mono_tick: int = 0, seq_tick: int = 0) -> list[Note]:
        ...

    @abstractmethod
    def visual_tick(self, rt_tick: int = 0):
        """TRIGGER VISUAL EVENT AT THE END!"""
        ...