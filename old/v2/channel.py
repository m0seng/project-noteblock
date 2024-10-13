from processor import Processor
from note import Note
from pattern import Pattern
import bisect

class Channel(Processor):
    # props.patterns: list[tuple[int, int]]
    # maps sequence ticks to patterns placed on them
    # maintain sortedness!
    # int is used instead of direct references to patterns so they can be deleted...?
    # something like that
    # pattern_dict is the dictionary of all patterns by id

    default_props = {
        "patterns": [],
        "effects": [],
    }
    default_state = {
        "last_index": 0,
    }
    
    def __init__(self, pattern_dict: dict[int, Pattern], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pattern_dict = pattern_dict

    def audio_tick(self, input: list[Note] = [], mono_tick: int = 0, seq_tick: int = 0) -> list[Note]:
        # find the only possible pattern - the last one starting before or on the current tick
        if not self.in_pattern(self.state["last_index"], seq_tick):
            index = bisect.bisect(self.props["patterns"], seq_tick, key=lambda r: r[0]) - 1
            self.state["last_index"] = index

        # get note from found pattern
        start_tick, pattern_no = self.pattern_info(index)
        current_pattern = self.pattern_dict[pattern_no]
        current_note = current_pattern.tick(seq_tick - start_tick)
        note_list = [current_note,]

        for effect in self.props["effects"]:
            note_list = effect.audio_tick(note_list, mono_tick, seq_tick)

    def pattern_info(self, index: int):
        return self.props["patterns"][index]

    def in_pattern(self, index: int, seq_tick: int):
        start_tick, pattern_no = self.pattern_info(index)
        pattern = self.pattern_dict[pattern_no]
        end_tick = start_tick + pattern.length
        return start_tick <= seq_tick < end_tick