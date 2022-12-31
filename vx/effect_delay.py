from note import Note
from effect import Effect
from effect_ui import EffectUI

class EffectDelay(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ... # initialize properties and state here

    def tick(self, mono_tick: int, sequence_enabled: bool, bar_number: int, pat_tick: int) -> list[Note]:
        ... # do tick logic here

class EffectDelayUI(EffectUI):
    def init_ui(self):
        super().init_ui()
        ... # initialize UI components here - grid into column 0, row 1

    def update_ui(self):
        super().update_ui()
        ... # update UI components based on self.effect (which will not be None)