from note import Note
from effect import Effect
from effect_ui import EffectUI

# TODO: make this!!!

class EffectDelay(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ... # initialize properties and state here

    def process_notes(self, notes: list[Note], mono_tick: int) -> list[Note]:
        ... # do tick logic here

class EffectDelayUI(EffectUI):
    def init_ui(self):
        super().init_ui()
        ... # initialize UI components here - grid into column 0, row 1

    def update_ui(self):
        super().update_ui()
        ... # update UI components based on self.effect (which will not be None)