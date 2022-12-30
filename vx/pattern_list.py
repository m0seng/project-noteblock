import tkinter as tk
import tkinter.ttk as ttk
from tkinter import dnd

from node import Node
from pattern import Pattern
from events import Listener
from model import Model

class PatternList(Listener, ttk.Frame):
    def __init__(self, parent, *args, model: Model, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.name_width: int = 20

        self.init_ui()
        self.model.event_bus.add_listener(self)
        self.update_ui()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_property_set(self, node: Node, key, old_value, new_value):
        if isinstance(node, Pattern) and key != "notes":
            self.update_ui()

    def node_child_added(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.pattern_group:
            self.update_ui()

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.pattern_group:
            self.update_ui()

    def reset_ui(self):
        self.update_ui()

    def init_ui(self):
        self.canvas = tk.Canvas(self)
        self.canvas.grid(column=0, row=0, sticky="ns")

        self.internal_frame = ttk.Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor="nw", window=self.internal_frame)

        # NOTE: this is the magic line
        # resizing canvas to frame here instead of in update_ui() avoids the
        # problem of having 1 pixel width/height at init
        self.internal_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(width=self.internal_frame.winfo_reqwidth())
        )

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar["command"] = self.canvas.yview
        self.scrollbar.grid(column=1, row=0, sticky="ns")

        self.btn_add_pattern = ttk.Button(
            self,
            text="+ add pattern",
            command=self.model.new_pattern
        )
        self.btn_add_pattern.grid(column=0, row=1)

    def update_ui(self):
        for child in self.internal_frame.winfo_children():
            child.destroy()

        # empty function that gets added to every pattern label
        def dnd_end(target, event):
            ...

        for index, pattern in enumerate(self.model.pattern_group.children_iterator()):
            pattern_name = pattern.get_property("name")
            pattern_colour = pattern.get_property("colour")
            pattern_label = ttk.Label(
                self.internal_frame,
                text=pattern_name,
                width=self.name_width,
                background=pattern_colour,
            )
            pattern_label.pattern = pattern # cheeky monkey patch
            pattern_label.dnd_end = dnd_end
            pattern_label.bind("<ButtonPress-1>", lambda e: self.model.event_bus.node_selected(pattern))
            pattern_label.bind("<ButtonPress-1>", lambda e: dnd.dnd_start(pattern_label, e), add=True)
            pattern_label.grid(column=0, row=index, ipadx=5, ipady=5, padx=2, pady=2)

        self.canvas.configure(scrollregion=(0, 0, 0, self.internal_frame.winfo_reqheight()))