from .processor import Processor
from .pattern import Pattern
from .pattern_group import PatternGroup
from .note import Note

class Channel(Processor):
    def __init__(self, pattern_group: PatternGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pattern_group = pattern_group

    def init_props(self):
        self.name = "default channel name"
        self.colour = "red"
        self.volume = 1.0
        self.pan = 0.0
        self.placements: list[tuple[int, int]] = [] # pattern id, start tick
    
    def init_state(self):
        self.last_index: int = 0

    def from_dict(self, source: dict):
        self.name = source["name"]
        self.colour = source["colour"]
        self.volume = source["volume"]
        self.pan = source["pan"]
        self.placements = [tuple(placement) for placement in source["placements"]]

    def to_dict(self) -> dict:
        channel_dict = {
            "name": self.name,
            "colour": self.colour,
            "volume": self.volume,
            "pan": self.pan,
            "placements": self.placements.copy()
        }
        return channel_dict

    def channel_length(self) -> int:
        last_pattern, last_start = self.placements[-1]
        return last_start + self.pattern_group.data[last_pattern].length

    def has_pattern(self, id: int) -> bool:
        return any(p == id for p, _ in self.placements)

    def purge_pattern(self, id: int):
        self.placements = [pm for pm in self.placements if pm[0] != id]

    def index_of_tick(self, tick: int):
        # TODO: convert this to a binary search - algorithm!
        return next(
            (index for index, item in enumerate(self.placements) if item[1] > tick),
            len(self.placements - 1) # default
        )

    def in_index(self, tick: int, index: int):
        pattern, start = self.placements[index]
        return start <= tick < (start + self.pattern_group.data[pattern].length)

    def add_placement(self, tick: int, pat_id: int):
        index = self.index_of_tick(tick)
        if tick == self.placements[index][1]:
            self.placements.pop(index) # remove existing pattern if same start tick!
        self.placements.insert(index, (pat_id, tick))

    def remove_placement(self, index: int):
        self.placements.pop(index)

    def audio_tick(self, notes: list[Note] = [], mono_tick: int = 0, seq_tick: int = 0, is_next: bool = True) -> list[Note]:
        if not is_next or not self.in_index(seq_tick, self.last_index):
            self.last_index = self.index_of_tick(seq_tick) - 1
        if self.in_index(seq_tick, self.last_index):
            pattern, start = self.placements[self.last_index]
            return self.pattern_group.data[pattern].tick(seq_tick - start)
        else:
            return []

    def visual_tick(self, rt_tick: int = 0):
        ...