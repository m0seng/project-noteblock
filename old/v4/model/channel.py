from ..basics import Processor, Note
from .effect_group import EffectGroup

class Channel(Processor):
    def init_props(self):
        self.name = "default channel name"
        self.colour = "red"
        self.volume = 1.0
        self.pan = 0.0
        self.placements = []
        self.effects: EffectGroup = EffectGroup()
    
    def init_state(self):
        ...

    def from_dict(self, source: dict):
        self.name = source["name"]
        self.colour = source["colour"]
        self.volume = source["volume"]
        self.pan = source["pan"]
        self.placements = [tuple(placement) for placement in source["placements"]]
        self.effects.from_dict(source)

    def to_dict(self) -> dict:
        channel_dict = {
            "name": self.name,
            "colour": self.colour,
            "volume": self.volume,
            "pan": self.pan,
            "placements": self.placements.copy()
        }
        channel_dict.update(self.effects.to_dict)
        return channel_dict

    def audio_tick(self, notes: list[Note] = [], mono_tick: int = 0, seq_tick: int = 0) -> list[Note]:
        ...

    def visual_tick(self, rt_tick: int = 0):
        ...