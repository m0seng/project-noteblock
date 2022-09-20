from abc import ABC, abstractmethod
from save_mixin import SaveMixin
import undo_manager as undoman
from event import Event

# props = stuff that gets saved
# state = stuff that doesn't

# mono_tick: always goes up, has lookahead
# seq_tick: tick in sequence, can go back
# rt_tick: mono_tick but no lookahead

# use with statement to modify props from outside!

class Processor(SaveMixin, ABC):
    def __init__(self, source: dict = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = Event()
        if source is not None:
            self.from_dict(source)
        else:
            self.init_props()
        self.init_state()

    def __enter__(self):
        undoman.begin_transaction(self)
        
    def __exit__(self, exc_type, exc_value, exc_tb):
        undoman.end_transaction()
        self.event.trigger()

    @abstractmethod
    def init_props(self):
        ...

    @abstractmethod
    def init_state(self):
        ...

    @abstractmethod
    def from_dict(self, source: dict):
        ...

    @abstractmethod
    def to_dict(self) -> dict:
        ...

    @abstractmethod
    def audio_tick(self, input: list["Note"] = [], mono_tick: int = 0, seq_tick: int = 0) -> list["Note"]:
        ...

    @abstractmethod
    def visual_tick(self, rt_tick: int = 0) -> list["Note"]:
        ...