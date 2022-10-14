from .savable import Savable
from .note import Note

class Pattern(Savable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id: int = None
        self.name: str = "pattern name"
        self.colour: str = "red"
        self.notes: list[int] = []

    def tick(self, pat_tick: int) -> list[Note]:
        # TODO: handle index error just in case
        note = self.notes[pat_tick]
        if note is not None:
            return [Note(pitch=self.notes[pat_tick]),]
        else:
            return []

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