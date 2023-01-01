import tkinter as tk
import tkinter.ttk as ttk

from model import Model

class SongSettings(tk.Toplevel):
    def __init__(self, parent, model: Model, **kwargs):
        super().__init__(parent, **kwargs)
        self.model = model
        self.title("song settings")

        self.lbl_song_name = ttk.Label(self, text="song name:")
        self.lbl_pattern_length = ttk.Label(self, text="pattern length:")
        self.lbl_sequence_length = ttk.Label(self, text="sequence length:")

        self.var_song_name = tk.StringVar(self, value=self.model.song_config.get_property("name"))
        self.var_pattern_length = tk.IntVar(self, value=self.model.song_config.get_property("pattern_length"))
        self.var_sequence_length = tk.IntVar(self, value=self.model.song_config.get_property("sequence_length"))

        self.inp_song_name = ttk.Entry(self, textvariable=self.var_song_name, width=25)
        self.inp_pattern_length = ttk.Spinbox(self, textvariable=self.var_pattern_length, width=10)
        self.inp_sequence_length = ttk.Spinbox(self, textvariable=self.var_sequence_length, width=10)

        self.btn_ok = ttk.Button(self, text="ok", command=self.save_settings)
        self.btn_cancel = ttk.Button(self, text="cancel", command=self.destroy)

        self.lbl_song_name.grid(column=0, row=0, sticky="e")
        self.lbl_pattern_length.grid(column=0, row=1, sticky="e")
        self.lbl_sequence_length.grid(column=0, row=2, sticky="e")
        self.inp_song_name.grid(column=1, row=0, sticky="w")
        self.inp_pattern_length.grid(column=1, row=1, sticky="w")
        self.inp_sequence_length.grid(column=1, row=2, sticky="w")
        self.btn_cancel.grid(column=0, row=3)
        self.btn_ok.grid(column=1, row=3)

        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=2)

    def save_settings(self):
        self.model.uman.start_group()
        self.model.ed.set_property(self.model.song_config, "name", self.var_song_name.get())
        self.model.change_pattern_length(self.var_pattern_length.get())
        self.model.change_sequence_length(self.var_sequence_length.get())
        self.model.uman.end_group()
        self.destroy()