from node import Node
from note import Note
from pattern import Pattern
from pattern_group import PatternGroup

class Channel(Node):
    def __init__(self, *args, pattern_group: PatternGroup, sequence_length: int = 20, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_property("name", "channel name")
        self._set_property("colour", "blue")
        self._set_property("main_instrument", 0)
        self._set_property("sustain_enabled", False)
        self._set_property("sustain_instrument", 0)
        self._set_property("sustain_mix", 0.5)
        self._set_property("volume", 1.0)
        self._set_property("pan", 0.0)
        self._set_property("mute", False)
        self._set_property("solo", False)
        self._set_property("placements", [-1] * sequence_length)
        self.pattern_group = pattern_group
        self.sustained_note = None

    def tick(self, mono_tick: int, sequence_enabled: bool, bar_number: int, pat_tick: int) -> list[Note]:
        if not sequence_enabled: # NO-PATTERN TICK!
            note_numbers = []
        else:
            # get note numbers from pattern
            pattern_id = self.get_property("placements")[bar_number]
            if pattern_id == -1: # no pattern
                note_numbers = []
            else:
                pattern: Pattern = self.pattern_group.get_child_by_id(pattern_id)
                note_numbers = pattern.get_notes(pat_tick)

        # convert to Note objects
        notes: list[Note] = self.convert_numbers_to_notes(note_numbers)

        # apply effects in sequence
        for effect in self.children_iterator():
            notes = effect.tick(notes, mono_tick)

        # apply volume and pan
        notes = [note.apply_volume_and_pan(
            volume=self.get_property("volume"),
            pan=self.get_property("pan")
        ) for note in notes]

        return notes


    def convert_numbers_to_notes(self, note_numbers: list[int]) -> list[Note]:
        notes = []
        sustain_enabled = self.get_property("sustain_enabled")
        for note_number in note_numbers:
            if 0 <= note_number <= 24: # normal note
                notes.append(Note(
                    instrument=self.get_property("main_instrument"),
                    pitch=note_number
                ))
                self.sustained_note = note_number
            elif note_number == -1: # no note
                if sustain_enabled and self.sustained_note is not None:
                    notes.append(Note(
                        instrument=self.get_property("sustain_instrument"),
                        pitch=self.sustained_note,
                        volume=self.get_property("sustain_mix")
                    ))
            elif note_number == -2: # SUSTAIN OFF!
                self.sustained_note = None
        return notes