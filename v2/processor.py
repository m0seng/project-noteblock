from abc import ABC, abstractmethod
from save_mixin import SaveMixin
from note import Note
from event import Event

# props = stuff that gets saved
# state = stuff that doesn't

# mono_tick: always goes up, has lookahead
# seq_tick: tick in sequence, can go back
# rt_tick: mono_tick but no lookahead

class Processor(SaveMixin, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.props = {}
        self.state = {}
        self.reset_state()

    def from_dict(self, source: dict):
        self.props.update(source)
        # TODO: add event here

    def to_dict(self) -> dict:
        return self.props

    @abstractmethod
    def reset_state(self):
        # also init state in here
        ...

    @abstractmethod
    def tick(self, input: list[Note] = [], mono_tick: int = 0, seq_tick: int = 0) -> list[Note]:
        ...

    @abstractmethod
    def visual_tick(self, rt_tick: int = 0) -> list[Note]:
        ...