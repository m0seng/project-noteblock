from node import Node
from events import Listener
from model import Model
from note import Note

class Playback(Listener):
    def __init__(self, model: Model):
        self.model = model
        self.mono_tick: int = 0
        self.sequence_enabled: bool = False
        self.bar_number: int = 0
        self.pat_tick: int = 0

    def tick(self):
        notes = self.model.channel_group.tick(
            mono_tick=self.mono_tick,
            sequence_enabled=self.sequence_enabled,
            bar_number=self.bar_number,
            pat_tick=self.pat_tick)
        self.increment_tick()

    def increment_tick(self):
        # increment tick
        self.mono_tick += 1
        if self.sequence_enabled: # normal pattern playback
            self.pat_tick += 1
            if self.pat_tick >= self.model.song_config.get_property("pattern_length"):
                self.pat_tick = 0
                self.bar_number += 1
                if self.bar_number >= self.model.song_config.get_property("sequence_length"):
                    self.sequence_enabled = False