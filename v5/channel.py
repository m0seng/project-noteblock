from .processor import Processor
from .pattern import Pattern
from .note import Note

class Channel(Processor):
    def init_props(self):
        self.name = "default channel name"
        self.colour = "red"
        self.volume = 1.0
        self.pan = 0.0
        self.placements: list[tuple[Pattern, int]] = []
    
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

    def has_pattern(self, pattern: Pattern) -> bool:
        return any(p == pattern for p, _ in self.placements)

    def purge_pattern(self, pattern: Pattern):
        new_placements = []
        for placement in self.placements:
            if placement[0] != pattern:
                new_placements.append(placement)
        self.placements = new_placements

    def index_of_tick(self, tick: int):
        # TODO: convert this to a binary search - algorithm!
        for index, item in enumerate(self.placements):
            if item[1] > tick:
                return index - 1
        return len(self.placements) - 1

    def in_index(self, tick: int, index: int):
        pattern, start = self.placements[index]
        return start <= tick < (start + pattern.length)

    def audio_tick(self, notes, mono_tick, seq_tick, is_next) -> list[Note]:
        if not is_next or not self.in_index(seq_tick, self.last_index):
            self.last_index = self.index_of_tick(seq_tick)
        if self.in_index(seq_tick, self.last_index):
            pattern, start = self.placements[self.last_index]
            return pattern.tick(seq_tick - start)
        else:
            return []

    def visual_tick(self, rt_tick: int = 0):
        ...