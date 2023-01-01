from abc import ABC, abstractmethod
from typing import Callable
import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import Listener
from model import Model
from effect import Effect
from effect_ui import EffectUI

class EasyEffectUI(EffectUI):
    effect_name: str = "easy effect ui"
    ui_width: int = 200

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

    def add_spinbox(self, key: str, low: float, high: float, step: float):
        set_callback = lambda e=None: self.model.ed.set_property(self.effect, key, var.get())
        get_callback = lambda: var.set(self.effect.get_property(key))
        var = tk.DoubleVar()
        spinbox = ttk.Spinbox(
            self, from_=low, to=high, increment=step, width=5,
            textvariable=var,
            command=set_callback)
        spinbox.bind("<Return>", set_callback)
        spinbox.grid(column=0, row=self.next_grid_row)
        self.next_grid_row += 1
        self.update_callbacks.append(get_callback)