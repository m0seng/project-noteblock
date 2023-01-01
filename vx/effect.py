from abc import ABC, abstractmethod
from node import Node
from note import Note

class Effect(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_property("enabled", True)

    def tick(self, notes: list[Note], mono_tick: int) -> list[Note]:
        # NOTE: this is for internal use with the "enabled" property
        if self.get_property("enabled"):
            return self.process_notes(notes, mono_tick)
        else:
            return notes

    @abstractmethod
    def process_notes(self, notes: list[Note], mono_tick: int) -> list[Note]:
        ...