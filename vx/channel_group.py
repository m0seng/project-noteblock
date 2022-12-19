from node import Node
from note import Note
from channel import Channel

class ChannelGroup(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tick(self, mono_tick: int, bar_number: int, pat_tick: int) -> list[Note]:
        notes = []
        for child in self.children_iterator():
            if isinstance(child, Channel):
                notes.append(child.tick(mono_tick, bar_number, pat_tick))