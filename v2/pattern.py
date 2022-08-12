from savable import Savable

class Pattern(Savable):
    def __init__(self, id: int = None):
        self.id: int = id
        self.name: str = "pattern bruh"
        self.colour: str = "red"
        self.notes: list[int] = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "colour": self.colour,
            "notes": self.notes,
        }

    def from_dict(self, source: dict):
        self.id = source["id"]
        self.name = source["name"]
        self.colour = source["colour"]
        self.notes = source["notes"]