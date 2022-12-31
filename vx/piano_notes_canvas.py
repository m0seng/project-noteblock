import math
import tkinter as tk

class PianoNotesCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        self.canvas_height: int = 300
        self.note_width: int = 20

        # drawing constants
        self.non_neg_pitch_count: int = 25
        self.negative_pitch_count: int = 2
        self.pitch_count: int = self.non_neg_pitch_count + self.negative_pitch_count
        self.draw_no_note: bool = False # for debugging idk
        self.note_height: float = self.canvas_height / self.pitch_count

        # colour constants
        # TODO: derive these from global theme???
        self.bg_colour: str = "white"
        self.guidebar_colour: str = "black"
        self.no_note_bar_colour: str = "gray50"

        super().__init__(
            parent, *args,
            height=self.canvas_height,
            width=self.note_width,
            highlightthickness=0,
            bg=self.bg_colour,
            **kwargs
        )
        
        for note in self.black_notes(self.pitch_count):
            self.draw_note(note, 0, length=1, fill=self.guidebar_colour, outline="")
        self.draw_note(-1, 0, length=1, fill=self.no_note_bar_colour, outline="")

    def draw_note(self, note: int, tick: int, length: int, **kwargs) -> int:
        """Draws a note on the canvas."""
        self.create_rectangle(
            tick * self.note_width,
            self.note_height * (self.non_neg_pitch_count - 1 - note),
            (tick + length) * self.note_width,
            self.note_height * (self.non_neg_pitch_count - note),
            **kwargs
        )

    def black_notes(self, pitch_count: int) -> list[int]:
        """Helper function which returns a list of black notes within the given pitch range."""
        result = []
        octave_black_notes = [0, 2, 4, 7, 9]
        octave_count = math.ceil(pitch_count / 12)
        for octave in range(octave_count):
            result.extend(n + 12*octave for n in octave_black_notes)
        result = filter(lambda n: n < pitch_count, result)
        return result