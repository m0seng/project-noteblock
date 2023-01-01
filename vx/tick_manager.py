from model import Model

class TickManager:
    def __init__(self, model: Model, ignore_loop: bool = False):
        self.model = model
        self.ignore_loop = ignore_loop
        self.mono_tick: int = 0
        self.sequence_enabled: bool = False
        self.bar_number: int = 0
        self.pat_tick: int = 0

    def next_tick(self):
        result = (
            self.mono_tick,
            self.sequence_enabled,
            self.bar_number,
            self.pat_tick
        )
        self._increment_tick()
        return result

    def set_tick(self, bar_number: int, pat_tick: int):
        self.bar_number = bar_number
        self.pat_tick = pat_tick

    def _increment_tick(self):
        # increment tick
        self.mono_tick += 1
        if self.sequence_enabled: # normal pattern playback
            self.pat_tick += 1
            self._justify_tick()

    def _justify_tick(self):
        if self.pat_tick >= self.model.song_config.get_property("pattern_length"):
            self.pat_tick = 0
            self.bar_number += 1
            if ((self.bar_number == self.model.song_config.get_property("loop_end"))
                    and self.model.song_config.get_property("loop_enabled")
                    and not self.ignore_loop):
                self.bar_number = self.model.song_config.get_property("loop_start")
            if self.bar_number >= self.model.song_config.get_property("sequence_length"):
                self.sequence_enabled = False