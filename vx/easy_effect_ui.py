from abc import abstractmethod
from typing import Callable
import tkinter as tk
import tkinter.ttk as ttk

from effect_ui import EffectUI

class EasyEffectUI(EffectUI):
    """UI component - provides methods to easily create simple effect UIs."""
    
    effect_name: str = "easy effect ui"
    ui_width: int = 200

    instrument_names = [
        "harp",
        "basedrum",
        "snare",
        "hat",
        "bass",
        "flute",
        "bell",
        "guitar",
        "chime",
        "xylophone",
        "iron_xylophone",
        "cow_bell",
        "didgeridoo",
        "bit",
        "banjo",
        "pling"
    ]
    grid_kwargs = {"sticky": "w", "padx": 2, "pady": 2}

    @abstractmethod    
    def init_ui(self):
        super().init_ui()
        self.next_grid_row: int = 1
        self.update_callbacks: list[Callable] = []

    @abstractmethod
    def update_ui(self):
        super().update_ui()
        for callback in self.update_callbacks:
            callback()

    def add_label(self, text: str):
        label = ttk.Label(self, text=text)
        label.grid(column=0, row=self.next_grid_row, **self.grid_kwargs)
        self.next_grid_row += 1
    
    def add_checkbox(self, name: str, key: str):
        var = tk.BooleanVar()
        set_callback = lambda e=None: self.model.ed.set_property(self.effect, key, var.get())
        get_callback = lambda: var.set(self.effect.get_property(key))
        checkbox = ttk.Checkbutton(self, text=name, command=set_callback, variable=var)
        checkbox.grid(column=0, row=self.next_grid_row, **self.grid_kwargs)
        self.next_grid_row += 1
        self.update_callbacks.append(get_callback)

    def add_spinbox(self, name: str, key: str, low: float, high: float, step: float, int_only: bool = False):
        var = (tk.IntVar() if int_only else tk.DoubleVar())
        set_callback = lambda e=None: self.model.ed.set_property(
            self.effect, key, self._clamp(var.get(), low, high))
        get_callback = lambda: var.set(self.effect.get_property(key))
        frame = ttk.Frame(self)
        label = ttk.Label(frame, text=name)
        spinbox = ttk.Spinbox(
            frame, from_=low, to=high, increment=step, width=5,
            textvariable=var,
            command=set_callback)
        spinbox.bind("<Return>", set_callback)
        label.grid(column=0, row=0)
        spinbox.grid(column=1, row=0)
        frame.grid(column=0, row=self.next_grid_row, **self.grid_kwargs)
        self.next_grid_row += 1
        self.update_callbacks.append(get_callback)

    def add_instrument_choice(self, name: str, key: str):
        var = tk.StringVar()
        set_callback = lambda e=None: self.model.ed.set_property(self.effect, key,
            self.instrument_names.index(var.get()))
        get_callback = lambda: var.set(self.instrument_names[self.effect.get_property(key)])
        frame = ttk.Frame(self)
        label = ttk.Label(frame, text=name)
        combo = ttk.OptionMenu(
            frame, var,
            self.instrument_names[0],
            *self.instrument_names,
            command=set_callback)
        label.grid(column=0, row=0)
        combo.grid(column=1, row=0)
        frame.grid(column=0, row=self.next_grid_row, **self.grid_kwargs)
        self.next_grid_row += 1
        self.update_callbacks.append(get_callback)

    def _clamp(self, value, low, high):
        return min(max(value, low), high)