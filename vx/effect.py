from abc import ABC, abstractmethod
from node import Node
from note import Note

class Effect(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def tick(self, mono_tick: int, sequence_enabled: bool, bar_number: int, pat_tick: int) -> list[Note]:
        ...