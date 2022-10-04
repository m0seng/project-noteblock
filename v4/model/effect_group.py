from ..basics import Processor, Note
from .. import effects

class EffectGroup(Processor):
    def init_props(self):
        self.effects: list[Processor] = []

    def init_state(self):
        ...

    def from_dict(self, source: dict):
        effects_list = source["effects"]
        for effect_dict in effects_list:
            effect_class: Processor = getattr(effects, effect_dict["class"])
            effect = effect_class.create_from_dict(effect_dict)
            self.effects.append(effect)

    def to_dict(self) -> dict:
        effects_list = []
        for effect in self.effects:
            effect_dict = effect.to_dict()
            effects_list.append(effect_dict)
        return {
            "effects": effects_list
        }

    def audio_tick(self, notes: list[Note] = [], mono_tick: int = 0, seq_tick: int = 0) -> list[Note]:
        for effect in self.effects:
            notes = effect.audio_tick(notes=notes, mono_tick=mono_tick, seq_tick=seq_tick)
        return notes

    def visual_tick(self, rt_tick: int = 0):
        ...