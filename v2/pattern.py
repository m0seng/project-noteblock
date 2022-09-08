from save_mixin import SaveMixin

class Pattern(SaveMixin):
    def __init__(self, id: int = None):
        self.id: int = id
        self.name: str = "pattern bruh"
        self.colour: str = "red"
        self.notes: list[int] = []

    def tick(self, pat_tick: int) -> int:
        return self.notes[pat_tick]

    @property
    def length(self):
        return len(self.notes)

    @length.setter
    def length(self, value):
        if self.length < value:
            self.notes.extend(None for _ in range(value - self.length))
        elif self.length > value:
            self.notes = self.notes[:value]
        else:
            pass
        # TODO: add event here

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
        self.notes = source["notes"]
        # TODO: add event here