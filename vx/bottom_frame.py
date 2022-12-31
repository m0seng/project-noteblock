import tkinter as tk
import tkinter.ttk as ttk

from model import Model

from piano_roll import PianoRoll

# TODO: update this to use new piano roll lol

class BottomFrame(ttk.Frame):
    def __init__(self, parent, *args, model: Model, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.columnconfigure(1, weight=1)
        self.showing: bool = True

        self.btn_hide = ttk.Button(
            self,
            text="▼",
            width=3,
            command=self.toggle_show
        )

        self.notebook = ttk.Notebook(self)
        self.piano_roll = PianoRoll(self.notebook, model=self.model)
        self.notebook.add(self.piano_roll, text="piano roll")

        self.btn_hide.grid(column=0, row=0, sticky="n")
        self.notebook.grid(column=1, row=0, sticky="nsew")

    def toggle_show(self):
        if self.showing:
            self.notebook.grid_forget()
            self.btn_hide.configure(text="▲")
            self.showing = False
        else:
            self.notebook.grid(column=1, row=0, sticky="nsew")
            self.btn_hide.configure(text="▼")
            self.showing = True