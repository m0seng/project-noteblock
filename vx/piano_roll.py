import tkinter as tk
import tkinter.ttk as ttk

from model import Model
from piano_roll_canvas import PianoRollCanvas
from piano_notes_canvas import PianoNotesCanvas
from pattern_settings import PatternSettings

class PianoRoll(ttk.Frame):
    """UI component - a scrollable, editable pattern display."""

    def __init__(self, parent, *args, model: Model, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model

        self.piano_roll_canvas = PianoRollCanvas(self, model=self.model)
        self.piano_notes_canvas = PianoNotesCanvas(self)
        self.pattern_settings = PatternSettings(self, model=model, canvas=self.piano_roll_canvas)
        
        self.scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.piano_roll_canvas.configure(xscrollcommand=self.scrollbar.set)
        self.scrollbar["command"] = self.piano_roll_canvas.xview

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.pattern_settings.grid(column=0, row=0, columnspan=2, sticky="ew")
        self.piano_notes_canvas.grid(column=0, row=1)
        self.piano_roll_canvas.grid(column=1, row=1, sticky="ew")
        self.scrollbar.grid(column=1, row=2, sticky="ew")