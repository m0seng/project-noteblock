import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import Listener
from model import Model

from pattern import Pattern

class PatternSettings(Listener, ttk.Frame):
    padding = {"padx": 5, "pady": 5}

    def __init__(self, parent, *args, model: Model, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.pattern: Pattern | None = None

        self.columnconfigure(0, weight=1)

        self.init_ui()
        self.model.event_bus.add_listener(self)
        self.update_ui()

    def attach_pattern(self, pattern: Pattern | None):
        # NOTE: this is made obsolete by the node_selected event
        self.pattern = pattern
        self.update_ui()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_property_set(self, node: Node, key, old_value, new_value):
        if node is self.pattern and key != "notes":
            self.update_ui()

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.pattern_group and child is self.pattern:
            self.pattern = None
            self.update_ui()

    def node_selected(self, node: Node):
        if isinstance(node, Pattern):
            self.pattern = node
            self.update_ui()

    def reset_ui(self):
        self.pattern = None
        self.update_ui()

    def init_ui(self):
        self.var_name = tk.StringVar(self)
        self.inp_name = ttk.Entry(
            self,
            width=20,
            textvariable=self.var_name,
        )
        self.inp_name.bind(
            "<Return>",
            lambda e: self.model.ed.set_property(self.pattern, "name", self.var_name.get())
        )

    def update_ui(self):
        if self.pattern is None:
            self.state(["disabled"])
        else:
            self.state(["!disabled"])
            self.var_name.set(self.pattern.get_property("name"))