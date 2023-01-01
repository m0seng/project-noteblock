from note import Note
from effect import Effect

class EffectDummy(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # initialize properties and state here

    def process_notes(self, notes: list[Note], mono_tick: int) -> list[Note]:
        # do tick logic here
        return notes