import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import Listener
from model import Model
from channel import Channel
from effect import Effect
from effect_ui_factory import EffectUIFactory
from instrument_settings import InstrumentSettings

class EffectRack(Listener, ttk.Frame):
    def __init__(self, parent, model: Model, **kwargs):
        super().__init__(parent, **kwargs)
        self.model = model
        self.channel: Channel | None = None

        self.init_ui()
        self.factory = EffectUIFactory(parent=self.internal_frame, model=self.model)

        self.model.event_bus.add_listener(self)
        self.update_ui()

    def destroy(self):
        self.model.event_bus.remove_listener(self)
        super().destroy()

    def node_child_added(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.channel:
            self.update_ui()

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.channel or child is self.channel:
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

    def init_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self)
        self.canvas.grid(column=1, row=0, sticky="nsew")

        self.internal_frame = ttk.Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor="nw", window=self.internal_frame)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.scrollbar["command"] = self.canvas.xview
        self.scrollbar.grid(column=1, row=1, sticky="ew")

    def update_ui(self):
        for child in self.internal_frame.winfo_children():
            child.destroy()

        if self.channel is not None:
            instrument_settings = InstrumentSettings(self, model=self.model, channel=self.channel)
            instrument_settings.grid(column=0, row=0, sticky="nsew", padx=5, pady=5)
            for index, effect in enumerate(self.channel.children_iterator()):
                if isinstance(effect, Effect):
                    effect_ui = self.factory.create_ui(effect)
                    effect_ui.grid(column=index, row=0, sticky="ns", padx=5, pady=5)

        self.canvas.configure(
            height=self.internal_frame.winfo_reqheight(),
            scrollregion=(0, 0, self.internal_frame.winfo_reqwidth(), 0)
        )