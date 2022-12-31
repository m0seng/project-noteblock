import math
import tkinter as tk

from node import Node
from events import Listener
from model import Model

from pattern import Pattern

class PianoRollCanvas(Listener, tk.Canvas):
    def __init__(self, parent, *args, model: Model, **kwargs):
        self.canvas_height: int = 300
        self.note_width: float = 20
        self.model = model
        self.pattern: Pattern | None = None

        # drawing constants
        self.non_neg_pitch_count: int = 25
        self.negative_pitch_count: int = 2
        self.pitch_count: int = self.non_neg_pitch_count + self.negative_pitch_count
        self.draw_no_note: bool = False # for debugging idk
        self.note_height: float = self.canvas_height / self.pitch_count

        # colour constants
        # TODO: derive these from global theme???
        self.bg_colour: str = "gray75"
        self.guidebar_colour: str = "gray70"
        self.guideline_colour: str = "gray65"
        self.no_note_bar_colour: str = "gray65"

        super().__init__(
            parent, *args,
            height=self.canvas_height,
            scrollregion=(0, 0, self.target_canvas_length(), self.canvas_height),
            highlightthickness=0,
            bg=self.bg_colour,
            **kwargs
        )
        
        self.model.event_bus.add_listener(self)
        self.bind("<ButtonPress-1>", self.set_note) # left click sets note
        self.bind("<ButtonPress-3>", self.delete_note) # right click deletes note
        
        self.draw_everything()

    def attach_pattern(self, pattern: Pattern | None):
        # NOTE: this is made obsolete by the node_selected event
        self.pattern = pattern
        self.draw_everything()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_property_set(self, node: Node, key, old_value, new_value):
        if node is self.pattern:
            self.draw_everything()

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.pattern_group and child is self.pattern:
            self.pattern = None
            self.draw_everything()

    def node_selected(self, node: Node):
        if isinstance(node, Pattern):
            self.pattern = node
            self.draw_everything()

    def reset_ui(self):
        self.pattern = None
        self.draw_everything()

    def zoom(self, zoom_factor: float):
        """Stretches the piano roll horizontally by the given factor."""
        left_fraction = self.xview()[0]
        self.note_width *= zoom_factor
        self.configure(scrollregion=(0, 0, self.target_canvas_length(), self.canvas_height))
        self.xview_moveto(left_fraction)
        self.draw_everything()

    def draw_everything(self):
        """Clears and redraws the canvas."""
        self.delete("all")
        # make sure the canvas is the right length if pattern length has changed!
        self.configure(scrollregion=(0, 0, self.target_canvas_length(), self.canvas_height))
        self.draw_guide_bars()
        self.draw_guide_lines()
        self.draw_pattern_notes()

    def draw_guide_bars(self):
        """Draws the horizontal guide bars."""
        length = self.pattern_length()
        for note in self.black_notes(self.pitch_count):
            self.draw_note(note, 0, length=length, fill=self.guidebar_colour, outline="")
        self.draw_note(-1, 0, length=length, fill=self.no_note_bar_colour, outline="")

    def draw_guide_lines(self):
        """Draws the vertical guide lines."""
        for i in range(self.pattern_length()):
            self.create_line(
                i * self.note_width,
                0,
                i * self.note_width,
                self.canvas_height,
                fill=self.guideline_colour,
                width=0
            )

    def draw_pattern_notes(self):
        """Draws all notes in the pattern."""
        if self.pattern is not None:
            for tick, note in enumerate(self.pattern.get_property("notes")):
                if note != -1 or self.draw_no_note:
                    self.draw_note(note, tick, length=1, fill=self.pattern.get_property("colour"))

    def draw_note(self, note: int, tick: int, length: int, **kwargs) -> int:
        """Draws a note on the canvas."""
        self.create_rectangle(
            tick * self.note_width,
            self.note_height * (self.non_neg_pitch_count - 1 - note),
            (tick + length) * self.note_width,
            self.note_height * (self.non_neg_pitch_count - note),
            **kwargs
        )

    def get_note_at_coords(self, x: int, y: int) -> tuple[int, int]:
        """Translates widget-relative coordinates to the corresponding note and tick."""
        canvas_x = self.canvasx(x)
        canvas_y = self.canvasy(y)
        tick = int(canvas_x // self.note_width)
        note = int(self.non_neg_pitch_count - 1 - (canvas_y // self.note_height))
        return note, tick

    def delete_note(self, event: tk.Event):
        """Deletes a note at the given event coordinates."""
        if self.pattern is not None:
            note, tick = self.get_note_at_coords(event.x, event.y)
            if tick < self.pattern_length() and self.pattern.get_property("notes")[tick] == note:
                notes = self.pattern.get_property("notes")
                notes[tick] = -1
                self.model.ed.set_property(self.pattern, "notes", notes)

    def set_note(self, event: tk.Event):
        """Sets a note at the given event coordinates. If a note is already at that tick it is replaced."""
        if self.pattern is not None:
            note, tick = self.get_note_at_coords(event.x, event.y)
            if tick < self.pattern_length():
                notes = self.pattern.get_property("notes")
                notes[tick] = note
                self.model.ed.set_property(self.pattern, "notes", notes)

    def black_notes(self, pitch_count: int) -> list[int]:
        """Helper function which returns a list of black notes within the given pitch range."""
        result = []
        octave_black_notes = [0, 2, 4, 7, 9]
        octave_count = math.ceil(pitch_count / 12)
        for octave in range(octave_count):
            result.extend(n + 12*octave for n in octave_black_notes)
        result = filter(lambda n: n < pitch_count, result)
        return result

    def target_canvas_length(self) -> int:
        """Helper function to calculate how long the canvas should be."""
        return self.note_width * self.pattern_length()

    def pattern_length(self):
        if self.pattern is not None:
            return len(self.pattern.get_property("notes"))
        else:
            return 0