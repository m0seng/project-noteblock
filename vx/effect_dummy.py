import tkinter as tk
import tkinter.ttk as ttk

from note import Note
from effect import Effect
from effect_ui import EffectUI

class EffectDummy(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # initialize properties and state here

    def process_notes(self, notes: list[Note], mono_tick: int) -> list[Note]:
        # do tick logic here
        return notes

class EffectDummyUI(EffectUI):
    def init_ui(self):
        super().init_ui()
        # initialize UI components here - grid into column 0, row 1
        self.columnconfigure(0, minsize=200)
        self.label = ttk.Label(self, text="dummy effect")
        self.label.grid(column=0, row=1, sticky="nsew", padx=5, pady=5)

    def update_ui(self):
        super().update_ui()
        ... # update UI components based on self.effect (which will not be None)