import tkinter as tk
import tkinter.ttk as ttk
from tkinter import colorchooser

from node import Node
from events import Listener
from model import Model

from pattern import Pattern
from piano_roll_canvas import PianoRollCanvas

class PatternSettings(Listener, ttk.Frame):
    """UI component - shows a pattern's settings above the piano roll."""

    padding = {"padx": 2, "pady": 2}

    def __init__(self, parent, *args, model: Model, canvas: PianoRollCanvas, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.canvas = canvas
        self.pattern: Pattern | None = None

        self.init_ui()
        self.model.event_bus.add_listener(self)
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

    def choose_colour(self, event: tk.Event):
        if self.pattern is not None:
            colour = colorchooser.askcolor()[1]
            if colour is not None: self.model.ed.set_property(self.pattern, "colour", colour)

    def init_ui(self):
        self.lbl_colour = ttk.Label(self, width=3)
        self.lbl_colour.bind(
            "<ButtonPress-1>",
            self.choose_colour
        )

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

        self.btn_zoom_in = ttk.Button(
            self,
            text="+",
            width=3,
            command=lambda: self.canvas.zoom(1.25)
        )
        self.btn_zoom_out = ttk.Button(
            self,
            text="-",
            width=3,
            command=lambda: self.canvas.zoom(0.8)
        )

        self.btn_delete = ttk.Button(
            self,
            text="🗑",
            width=3,
            command=lambda: self.model.remove_pattern(self.pattern)
        )
        
        self.lbl_colour.grid(column=0, row=0, **self.padding)
        self.inp_name.grid(column=1, row=0, **self.padding)
        self.btn_zoom_in.grid(column=2, row=0, **self.padding)
        self.btn_zoom_out.grid(column=3, row=0, **self.padding)
        self.btn_delete.grid(column=5, row=0, sticky="e", **self.padding)

    def update_ui(self):
        if self.pattern is None:
            self.set_all_states(["disabled"])
        else:
            self.set_all_states(["!disabled"])
            self.lbl_colour.config(background=self.pattern.get_property("colour"))
            self.var_name.set(self.pattern.get_property("name"))

    def set_all_states(self, statespec: list[str]):
        for component in (self.inp_name, self.btn_zoom_in, self.btn_zoom_out, self.btn_delete):
            component.state(statespec)