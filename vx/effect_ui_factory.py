from typing import Type

from model import Model
from effect import Effect
from effect_ui import EffectUI

from effect_dummy_ui import EffectDummyUI
# TODO: import EffectUI subclasses here

class EffectUIFactory:
    ui_classes: dict[str, Type[EffectUI]] = {
        "EffectDummy": EffectDummyUI,
        # TODO: add entries for EffectUI subclasses here
    }

    def __init__(self, parent, model: Model):
        self.parent = parent
        self.model = model

    def create_ui(self, effect: Effect, **kwargs):
        ui_class = self.ui_classes.get(effect.__class__.__name__, None)
        if ui_class is None: return None
        ui_object = ui_class(self.parent, model=self.model, effect=effect, **kwargs)
        return ui_object