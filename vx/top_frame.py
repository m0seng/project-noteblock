import tkinter as tk
import tkinter.ttk as ttk

from model import Model

from playback import Playback

class TopFrame(ttk.Frame):
    def __init__(self, parent, *args, model: Model, playback: Playback, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.playback = playback

        self.btn_play = ttk.Button(
            self, text="⏵", width=3,
            command=self.playback.play
        )
        self.btn_pause = ttk.Button(
            self, text="⏸", width=3,
            command=self.playback.pause
        )
        self.btn_stop = ttk.Button(
            self, text="⏹", width=3,
            command=self.playback.stop
        )
        self.btn_undo = ttk.Button(
            self, text="↶", width=3,
            command=self.model.uman.undo
        )
        self.btn_redo = ttk.Button(
            self, text="↺", width=3,
            command=self.model.uman.redo
        )

        self.btn_play.grid(column=0, row=0)
        self.btn_pause.grid(column=1, row=0)
        self.btn_stop.grid(column=2, row=0)
        self.btn_undo.grid(column=3, row=0)
        self.btn_redo.grid(column=4, row=0)