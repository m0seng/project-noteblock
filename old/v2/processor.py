from abc import ABC, abstractmethod
import copy
from save_mixin import SaveMixin
from note import Note
from event import Event

# props = stuff that gets saved
# state = stuff that doesn't

# mono_tick: always goes up, has lookahead
# seq_tick: tick in sequence, can go back
# rt_tick: mono_tick but no lookahead

class Processor(SaveMixin, ABC):
    default_props = {}
    default_state = {}

    def __init__(self, source: dict = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if source is not None:
            self.from_dict(source)
        else:
            self.init_props()
        self.init_state()

    def from_dict(self, source: dict):
        self.props = copy.deepcopy(source)
        # TODO: add event here

    def to_dict(self) -> dict:
        return copy.deepcopy(self.props)

    def init_props(self):
        self.props = copy.deepcopy(self.__class__.default_props)

    def init_state(self):
        self.state = copy.deepcopy(self.__class__.default_state)

    @abstractmethod
    def audio_tick(self, input: list[Note] = [], mono_tick: int = 0, seq_tick: int = 0) -> list[Note]:
        ...

    @abstractmethod
    def visual_tick(self, rt_tick: int = 0) -> list[Note]:
        ...