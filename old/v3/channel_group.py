from .processor import Processor
from .channel import Channel
from .note import Note

class ChannelGroup(Processor):
    def init_state(self):
        ...

    def init_props(self):
        self.channels: list[Channel] = []

    def to_dict(self) -> dict:
        return {
            "channels": [channel.to_dict() for channel in self.channels]
        }

    def from_dict(self, source: dict):
        # don't worry about the old channels here
        # the context manager event will take care of them
        self.channels = []
        for channel_dict in source:
            channel = Channel.create_from_dict(channel_dict)
            self.channels.append(channel)

    def audio_tick(self, input: list[Note] = ..., mono_tick: int = 0, seq_tick: int = 0) -> list[Note]:
        notes = []
        for channel in self.channels:
            notes.extend(channel.audio_tick(mono_tick=mono_tick, seq_tick=seq_tick))
        return notes
    
    def visual_tick(self, rt_tick: int = 0):
        ... # TODO