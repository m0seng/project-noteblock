from note import Note
from pattern import Pattern, DummyPattern
from effect import Effect, SimpleSlapbackEffect

class Channel():
    def __init__(self):
        self.patterns: list[Pattern] = []
        self.dummy_pattern = DummyPattern(ticks_per_note=1) # temporary
        self.effects: list[Effect] = [SimpleSlapbackEffect()] # temporary added effect

    def get_notes(self, timestamp: int):
        # TODO: get notes from pattern!
        notes = self.dummy_pattern.get_notes(timestamp) # temporary

        for effect in self.effects:
            notes = effect.tick(notes)
        return notes