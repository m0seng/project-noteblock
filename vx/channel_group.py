from node import Node
from note import Note
from channel import Channel

class ChannelGroup(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tick(self, mono_tick: int, sequence_enabled: bool, bar_number: int, pat_tick: int) -> list[Note]:
        notes: list[Note] = []
        solo_active = any(child.get_property("solo") for child in self.children_iterator())
        for child in self.children_iterator():
            if isinstance(child, Channel):
                channel_notes = child.tick(mono_tick, sequence_enabled, bar_number, pat_tick)
                muted = child.get_property("mute")
                soloed = child.get_property("solo")
                if soloed or (not muted and not solo_active):
                    notes.extend(channel_notes)
        return notes