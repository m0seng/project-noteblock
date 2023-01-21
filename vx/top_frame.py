import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd

from model import Model
from song_settings import SongSettings
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
        self.btn_new_song = ttk.Button(
            self, text="☆", width=3,
            command=self.model.init_tree
        )
        self.btn_load = ttk.Button(
            self, text="📁", width=3,
            command=lambda: self.model.from_file(fd.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON project file", "*.json")]
            ))
        )
        self.btn_save = ttk.Button(
            self, text="💾", width=3,
            command=lambda: self.model.to_file(fd.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON project file", "*.json")]
            ))
        )
        self.btn_settings = ttk.Button(
            self, text="⚙", width=3,
            command=lambda: SongSettings(self, model=self.model)
        )

        self.btn_play.grid(column=0, row=0)
        self.btn_pause.grid(column=1, row=0)
        self.btn_stop.grid(column=2, row=0)
        self.btn_undo.grid(column=3, row=0)
        self.btn_redo.grid(column=4, row=0)
        self.btn_new_song.grid(column=5, row=0)
        self.btn_load.grid(column=6, row=0)
        self.btn_save.grid(column=7, row=0)
        self.btn_settings.grid(column=8, row=0)