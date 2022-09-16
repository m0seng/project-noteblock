from processor import Processor
from note import Note
import bisect

class Channel(Processor):
    # props.patterns: list[tuple[int, int]]
    # maps sequence ticks to patterns placed on them
    # maintain sortedness!
    # int is used instead of direct references to patterns so they can be deleted...?
    # something like that

    default_props = {
        "patterns": [],
    }
    default_state = {}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def audio_tick(self, input: list[Note] = ..., mono_tick: int = 0, seq_tick: int = 0) -> list[Note]:
        # find the only possible pattern - the last one starting before or on the current tick
        index = bisect.bisect(self.props["patterns"], seq_tick, key=lambda r: r[0]) - 1