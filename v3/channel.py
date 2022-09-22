from processor import Processor
from note import Note
from pattern import Pattern
import bisect

# effects belong to a channel so storing direct references to them is fine (I think)
# patterns DO NOT belong to a channel and storing direct references would prevent them from being deleted

class Channel(Processor):
    def __init__(self, pattern_dict: dict[int, Pattern], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pattern_dict = pattern_dict

    def init_props(self):
        self.patterns: list[Pattern] = []
        self.effects: list[Processor] = []

    def init_state(self):
        self.last_index = 0

    def to_dict(self) -> dict:
        return {
            "patterns": self.patterns.copy(),
            "effects": self.effects.copy()
        }

    def from_dict(self, source: dict):
        # TODO: creating effects from dict does not work yet
        # need to figure out how to select the right class to instantiate
        # see https://stackoverflow.com/questions/4821104/dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported-module
        self.patterns = source["patterns"].copy()
        self.effects = [Processor.create_from_dict(effect) for effect in source["effects"]]

    def audio_tick(self, input: list[Note] = [], mono_tick: int = 0, seq_tick: int = 0) -> list[Note]:
        # find the only possible pattern - the last one starting before or on the current tick
        if not self.in_pattern(self.last_index, seq_tick):
            index = bisect.bisect(self.patterns, seq_tick, key=lambda r: r[0]) - 1
            self.last_index = index

        # get note from found pattern
        start_tick, pattern_no = self.patterns[index]
        current_pattern = self.pattern_dict[pattern_no]
        notes = current_pattern.tick(seq_tick - start_tick)

        for effect in self.effects:
            notes = effect.audio_tick(notes, mono_tick, seq_tick)

        return notes

    def in_pattern(self, index: int, seq_tick: int):
        start_tick, pattern_no = self.patterns[index]
        pattern = self.pattern_dict[pattern_no]
        end_tick = start_tick + pattern.length
        return start_tick <= seq_tick < end_tick

    # TODO: add methods for adding and removing pattern placements