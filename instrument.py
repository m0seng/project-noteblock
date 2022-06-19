from dataclasses import dataclass
from enum import Enum

@dataclass(slots=True)
class Instrument():
    id: int
    name: str
    path: str

harp = Instrument(0, "harp", "sounds/harp.ogg")
instruments = (harp,)