from dataclasses import dataclass

@dataclass(slots=True)
class Instrument():
    name: str
    path: str

instruments = {
    0: Instrument("harp", "sounds/harp.ogg")
}