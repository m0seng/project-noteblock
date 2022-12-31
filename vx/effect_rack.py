import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import Listener
from model import Model
from channel import Channel
from effect import Effect
from effect_ui_factory import EffectUIFactory

class EffectRack(Listener, ttk.Frame):
    def __init__(self, parent, model: Model, **kwargs):
        super().__init__(parent, **kwargs)
        self.model = model
        self.channel: Channel | None = None

        self.factory = EffectUIFactory(parent=self, model=self.model)

        self.model.event_bus.add_listener(self)
        self.update_ui()

    def destroy(self):
        self.model.event_bus.remove_listener(self)
        super().destroy()

    def node_child_added(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.channel:
            self.update_ui()

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.channel:
            self.update_ui()

    def node_child_moved(self, parent: Node, old_index: int, new_index: int):
        if parent is self.channel:
            self.update_ui()

    def node_selected(self, node: Node):
        if isinstance(node, Channel):
            self.channel = node
            self.update_ui()

    def reset_ui(self):
        self.channel = None
        self.update_ui()

    def update_ui(self):
        for child in self.winfo_children():
            child.destroy()

        if self.channel is not None:
            for index, effect in enumerate(self.channel.children_iterator()):
                if isinstance(effect, Effect):
                    effect_ui = self.factory.create_ui(effect)
                    effect_ui.grid(column=index, row=0, sticky="ns", padx=5, pady=5)