from ..basics import Processor, Note
from .channel import Channel

class ChannelGroup(Processor):
    def init_props(self):
        self.channels: list[Processor] = []

    def init_state(self):
        ...

    def from_dict(self, source: dict):
        self.channels = [Channel.create_from_dict(channel_dict) for channel_dict in source["channels"]]

    def to_dict(self) -> dict:
        return {
            "channels": [channel.to_dict() for channel in self.channels]
        }

    def audio_tick(self, notes: list[Note] = [], mono_tick: int = 0, seq_tick: int = 0) -> list[Note]:
        for channel in self.channels:
            notes += channel.audio_tick(notes=[], mono_tick=mono_tick, seq_tick=seq_tick)
        return notes

    def visual_tick(self, rt_tick: int = 0):
        ...