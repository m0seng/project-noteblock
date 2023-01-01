from abc import ABC, abstractmethod
import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import Listener
from model import Model
from effect import Effect

class EffectUI(Listener, ttk.Labelframe, ABC):
    effect_name: str = "base effect ui"
    ui_width: int = 200

    def __init__(self, parent, model: Model, effect: Effect, **kwargs):
        super().__init__(parent, text=self.effect_name, **kwargs)
        self.model = model
        self.effect = effect

        self.init_ui()
        self.model.event_bus.add_listener(self)
        self.update_ui()

    def destroy(self):
        self.model.event_bus.remove_listener(self)
        super().destroy()

    def node_property_set(self, node: Node, key, old_value, new_value):
        if node is self.effect:
            self.update_ui()

    @abstractmethod
    def init_ui(self):
        pad_kwargs = {"padx": 2, "pady": 2}
        self.columnconfigure(0, minsize=self.ui_width)
        self.header_frame = ttk.Frame(self)
        
        self.btn_enabled = ttk.Button(
            self.header_frame,
            text="|",
            width=3,
            command=lambda: self.model.ed.toggle_bool(self.effect, "enabled")
        )

        self.btn_move_left = ttk.Button(
            self.header_frame,
            text="◀",
            width=3,
            command=lambda: self.move_effect(-1)
        )
        self.btn_move_right = ttk.Button(
            self.header_frame,
            text="▶",
            width=3,
            command=lambda: self.move_effect(1)
        )
        self.btn_delete = ttk.Button(
            self.header_frame,
            text="🗑",
            width=3,
            command=lambda: self.model.ed.remove_child(self.effect.parent, self.effect)
        )

        self.header_frame.columnconfigure(1, weight=1)
        self.btn_enabled.grid(column=0, row=0, **pad_kwargs)
        self.btn_move_left.grid(column=2, row=0, **pad_kwargs)
        self.btn_move_right.grid(column=3, row=0, **pad_kwargs)
        self.btn_delete.grid(column=4, row=0, **pad_kwargs)
        self.header_frame.grid(column=0, row=0, sticky="ew")

    @abstractmethod
    def update_ui(self):
        self.btn_enabled.configure(text=("|" if self.effect.get_property("enabled") else "◯"))

    def move_effect(self, delta: int):
        channel = self.effect.parent
        if channel is not None:
            old_index = channel.get_index_of_child(self.effect)
            new_index = old_index + delta
            self.model.ed.move_child(channel, old_index, new_index)