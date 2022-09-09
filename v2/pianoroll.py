import math
import random
import tkinter as tk
import tkinter.ttk as ttk

from pattern import Pattern

class PianoRoll(ttk.Frame):
    """UI for editing patterns. Subclassed from ttk.Frame."""

    def __init__(self, parent, pattern: Pattern, *args, **kwargs):
        """Constructs the piano roll UI. kwargs are passed to ttk.Frame."""
        # drawing constants
        self.note_width: float = 20
        self.canvas_height: int = 400
        self.pitch_count: int = 25
        self.note_height: float = self.canvas_height / self.pitch_count

        # colour constants
        # TODO: derive these from global state and pattern colour
        self.bg_colour: str = "gray75"
        self.guidebar_colour: str = "gray70"
        self.guideline_colour: str = "gray65"
        self.note_colour: str = "red"

        self.pattern: Pattern = pattern
        self.notes: list[int] = pattern.notes # list of note numbers (or None) in pattern
        self.note_rectangles: list[int] = [] # contains ids of corresponding rectangles

        # create the frame
        super().__init__(parent, *args, **kwargs)
        self.columnconfigure(0, weight=1)

        self.init_canvas()
        self.init_scrollbar()
        self.init_controls()
        self.draw_everything()

    def init_canvas(self):
        """Initializes and grids the canvas with click bindings."""
        self.canvas = tk.Canvas(
            self, height=self.canvas_height,
            scrollregion=(0, 0, self.target_canvas_length(), self.canvas_height),
            highlightthickness=0,
            bg=self.bg_colour
        )
        self.canvas.bind("<ButtonPress-1>", self.set_note) # left click sets note
        self.canvas.bind("<ButtonPress-3>", self.delete_note) # right click deletes note
        self.canvas.grid(column=0, row=0, sticky="nsew", padx=5, pady=5)

    def init_scrollbar(self):
        """Initializes and grids the canvas scroll bar."""
        self.scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.scrollbar["command"] = self.canvas.xview
        self.scrollbar.grid(column=0, row=1, sticky="ew", padx=5, pady=5)

    def init_controls(self):
        """Initializes and grids control buttons."""
        self.controls = ttk.Frame(self)

        self.btn_zoom_in = ttk.Button(self.controls, text="Zoom in", command=lambda: self.zoom(1.25))
        self.btn_zoom_in.pack()

        self.btn_zoom_out = ttk.Button(self.controls, text="Zoom out", command=lambda: self.zoom(0.8))
        self.btn_zoom_out.pack()

        self.controls.grid(column=1, row=0, sticky="ns", padx=5, pady=5)

    def zoom(self, zoom_factor: float):
        """Stretches the piano roll horizontally by the given factor."""
        left_fraction = self.canvas.xview()[0]
        self.note_width *= zoom_factor
        self.canvas.configure(scrollregion=(0, 0, self.target_canvas_length(), self.canvas_height))
        self.canvas.xview_moveto(left_fraction)
        self.draw_everything()

    def draw_everything(self):
        """Clears and redraws the canvas."""
        self.canvas.delete("all")
        self.draw_guide_bars()
        self.draw_guide_lines()
        self.draw_pattern_notes()

    def draw_pattern_notes(self):
        """Draws all notes in the pattern and adds the corresponding rectangle ids to pattern_rectangles."""
        self.note_rectangles = []
        for tick, note in enumerate(self.notes):
            if note is not None:
                self.note_rectangles.append(self.draw_note(note, tick, length=1, fill=self.note_colour))
            else:
                self.note_rectangles.append(None)

    def draw_guide_bars(self):
        """Draws the horizontal guide bars."""
        for note in self.black_notes(self.pitch_count):
            self.draw_note(note, 0, length=len(self.notes), fill=self.guidebar_colour, outline="")

    def draw_guide_lines(self):
        """Draws the vertical guide lines. TODO: make this snap smart."""
        for index, _ in enumerate(self.notes):
            self.canvas.create_line(
                index * self.note_width,
                0,
                index * self.note_width,
                self.canvas_height,
                fill=self.guideline_colour,
                width=0
            )

    def draw_note(self, note: int, tick: int, length: int, **kwargs) -> int:
        """Draws a note on the canvas. Returns id of rectangle drawn. kwargs are passed to create_rectangle."""
        return self.canvas.create_rectangle(
            tick * self.note_width,
            self.note_height * (self.pitch_count - 1 - note),
            (tick + length) * self.note_width,
            self.note_height * (self.pitch_count - note),
            **kwargs
        )

    def get_note_at_coords(self, x: int, y: int) -> tuple[int, int]:
        """Translates widget-relative coordinates to the corresponding note and tick."""
        canvas_x = self.canvas.canvasx(x)
        canvas_y = self.canvas.canvasy(y)
        tick = int(canvas_x // self.note_width)
        note = int(self.pitch_count - 1 - (canvas_y // self.note_height))
        return note, tick

    def delete_note(self, event: tk.Event):
        """Deletes a note at the given event coordinates."""
        note, tick = self.get_note_at_coords(event.x, event.y)
        if self.notes[tick] == note:
            self.canvas.delete(self.note_rectangles[tick])
            self.notes[tick] = None
            self.note_rectangles[tick] = None

    def set_note(self, event: tk.Event):
        """Sets a note at the given event coordinates. If a note is already at that tick it is replaced."""
        note, tick = self.get_note_at_coords(event.x, event.y)
        self.notes[tick] = note
        self.canvas.delete(self.note_rectangles[tick])
        self.note_rectangles[tick] = self.draw_note(note, tick, length=1, fill=self.note_colour)

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
        return self.note_width * len(self.notes)


def main():
    """Bare bones testing code for the piano roll. (obsolete)"""
    # Make and configure the window
    window = tk.Tk()
    window.title("Piano Roll")
    window.resizable(True, False) # Only resize horizontally
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    # Randomly generate a pattern
    pattern_length = 60
    pattern_note_chance = 0.5
    notes = []
    for _ in range(pattern_length):
        if random.random() < pattern_note_chance:
            notes.append(random.randint(0, 24))
        else:
            notes.append(None)

    pattern = Pattern(notes=notes)

    # Create the piano roll
    roll = PianoRoll(window, pattern)
    roll.grid(column=0, row=0, sticky="nsew")

    # Start the event loop
    window.mainloop()

# duh
if __name__ == "__main__":
    main()