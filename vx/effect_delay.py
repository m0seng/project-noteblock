from note import Note
from effect import Effect

# TODO: make this!!!

class EffectDelay(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_property("delay_ticks", 4)
        self._set_property("dry_mix", 1.0)
        self._set_property("wet_mix", 0.5)
        self._set_property("wet_pan", 0.0)
        self.notes_buffer: list[list[Note]] = [[]]
        self.buffer_index: int = 0

    def process_notes(self, notes: list[Note], mono_tick: int) -> list[Note]:
        # the ol' buffer switcheroo
        delayed_notes = self.notes_buffer[self.buffer_index]
        self.notes_buffer[self.buffer_index] = notes
        
        # mix things
        dry_notes = [note.apply_volume_and_pan(
            volume=self.get_property("dry_mix")
        ) for note in notes]
        wet_notes = [note.apply_volume_and_pan(
            volume=self.get_property("wet_mix"),
            pan=self.get_property("wet_pan")
        ) for note in delayed_notes]

        # advance buffer index
        self.buffer_index += 1
        if self.buffer_index >= self.get_property("delay_ticks"): # loop back round
            self.buffer_index = 0
        elif self.buffer_index >= len(self.notes_buffer): # extend buffer
            self.notes_buffer.append([])

        # output
        return dry_notes + wet_notes