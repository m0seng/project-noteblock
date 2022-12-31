from abc import ABC, abstractmethod
import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import Listener
from model import Model
from effect import Effect

class EffectUI(Listener, ttk.Frame, ABC):
    def __init__(self, parent, model: Model, effect: Effect, **kwargs):
        super().__init__(parent, **kwargs)
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
        ... # TODO: write code for effect header here

    @abstractmethod
    def update_ui(self):
        ...