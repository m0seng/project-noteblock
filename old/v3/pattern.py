from dataclasses import dataclass, field
from .save_mixin import SaveMixin
from .note import Note

@dataclass
class Pattern(SaveMixin):
    id: int = None
    name: str = "pattern bruh"
    colour: str = "red"
    notes: list[int] = field(default_factory=lambda: [None for _ in range(16)])

    def tick(self, pat_tick: int) -> list[Note]:
        # TODO: handle index error just in case
        return [Note(pitch=self.notes[pat_tick]),]

    @property
    def length(self):
        return len(self.notes)

    @length.setter
    def length(self, value):
        if self.length < value:
            self.notes.extend(None for _ in range(value - self.length))
        else:
            self.notes = self.notes[:value]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "colour": self.colour,
            "notes": self.notes.copy(),
        }

    def from_dict(self, source: dict):
        self.id = source["id"]
        self.name = source["name"]
        self.colour = source["colour"]
        self.notes = source["notes"].copy()