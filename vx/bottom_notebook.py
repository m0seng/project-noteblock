import tkinter as tk
import tkinter.ttk as ttk

from model import Model

from piano_roll import PianoRoll

class BottomNotebook(ttk.Notebook):
    def __init__(self, parent, *args, model: Model, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model

        self.piano_roll = PianoRoll(self, model=self.model)
        self.blank_frame = ttk.Frame(self)

        self.add(self.piano_roll, text="piano roll")
        self.add(self.blank_frame, text="hide")