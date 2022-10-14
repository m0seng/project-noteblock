from collections import UserList
from .pattern import Pattern
from .processor import Processor
from .channel import Channel
from .note import Note

class ChannelGroup(Processor, UserList):
    def init_state(self):
        ...

    def init_props(self):
        self.data: list[Channel] = []

    def to_dict(self) -> dict:
        return {
            "channels": [channel.to_dict() for channel in self.data]
        }

    def from_dict(self, source: dict):
        # don't worry about the old channels here
        # the context manager event will take care of them
        self.data = []
        for channel_dict in source["channels"]:
            channel = Channel.create_from_dict(channel_dict)
            self.data.append(channel)

    def has_pattern(self, id: int) -> bool:
        return any(c.has_pattern(id) for c in self.data)

    def purge_pattern(self, id: int):
        for channel in self.data:
            channel.purge_pattern(id)

    def audio_tick(self, notes: list[Note] = [], mono_tick: int = 0, seq_tick: int = 0, is_next: bool = True) -> list[Note]:
        notes = []
        for channel in self.data:
            notes.extend(channel.audio_tick(mono_tick=mono_tick, seq_tick=seq_tick))
        return notes
    
    def visual_tick(self, rt_tick: int = 0):
        ...