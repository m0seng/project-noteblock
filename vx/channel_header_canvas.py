import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import Listener
from model import Model

from channel_header import ChannelHeader

class OldChannelHeaderCanvas(Listener, tk.Canvas):
    def __init__(self, parent, *args, model: Model, **kwargs):
        self.model = model
        self.bg_colour: str = "gray75"
        self.headers: list[ChannelHeader] = []
        self.header_width: int = 250
        self.header_height: int = 60

        super().__init__(
            parent,
            *args,
            width=self.header_width,
            highlightthickness=0,
            bg=self.bg_colour,
            **kwargs
        )

        self.model.event_bus.add_listener(self)
        self.update_ui()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_child_added(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.channel_group:
            self.update_ui()

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.channel_group:
            self.update_ui()

    def update_ui(self):
        for header in self.headers:
            header.destroy()
        self.headers = []

        channel_count = self.model.channel_group.children_count()
        self.configure(scrollregion=(0, 0, 0, self.header_height*channel_count))

        for index, channel in enumerate(self.model.channel_group.children_iterator()):
            header = ChannelHeader(self, model=self.model, channel=channel)
            self.create_window(0, index*self.header_height, anchor="nw", window=header)
            self.headers.append(header)


class ChannelHeaderCanvas(Listener, tk.Canvas):
    def __init__(self, parent, *args, model: Model, **kwargs):
        self.model = model
        self.bg_colour: str = "gray75"
        self.header_width: int = 220
        self.header_height: int = 60

        super().__init__(
            parent,
            *args,
            width=self.header_width,
            scrollregion=(0, 0, 0, 0),
            highlightthickness=0,
            bg=self.bg_colour,
            **kwargs
        )

        self.internal_frame = ttk.Frame(self)
        self.create_window(0, 0, anchor="nw", window=self.internal_frame)

        self.model.event_bus.add_listener(self)
        self.update_ui()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_child_added(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.channel_group:
            self.update_ui()

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.channel_group:
            self.update_ui()

    def update_ui(self):
        for header in self.internal_frame.winfo_children():
            header.destroy()

        channel_count = self.model.channel_group.children_count()
        self.configure(scrollregion=(0, 0, 0, self.header_height * channel_count))

        self.internal_frame.columnconfigure(0, minsize=self.header_width)

        for index, channel in enumerate(self.model.channel_group.children_iterator()):
            header = ChannelHeader(self.internal_frame, model=self.model, channel=channel)
            header.grid(column=0, row=index, sticky="nsew")
            self.internal_frame.rowconfigure(index, minsize=self.header_height)