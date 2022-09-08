from dataclasses import dataclass

@dataclass(slots=True)
class Instrument():
    id: int
    name: str
    path: str

harp = Instrument(0, "harp", "sounds/harp.ogg")
instruments = (harp,)