import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import EventBus, Listener
from node_editor import NodeEditor
from model import Model

from channel import Channel

class ChannelHeader(Listener, ttk.Frame):
    def __init__(self, parent, *args, model: Model, channel: Channel, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.channel = channel
        
        self.init_ui()
        self.model.event_bus.add_listener(self)
        self.bind("<ButtonPress-1>", lambda e: self.model.event_bus.node_selected(self.channel))
        self.update_ui()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_property_set(self, node: Node, key, old_value, new_value):
        if node is self.channel:
            self.update_ui()

    padding = {"padx": 2, "pady": 2}

    def init_ui(self):
        self.top_frame = ttk.Frame(self)

        self.lbl_colour = ttk.Label(self.top_frame, width=3)

        self.var_name = tk.StringVar(self)
        self.inp_name = ttk.Entry(
            self.top_frame,
            width=15,
            textvariable=self.var_name,
        )
        self.inp_name.bind(
            "<Return>",
            lambda e: self.model.ed.set_property(self.channel, "name", self.var_name.get())
        )

        self.btn_delete = ttk.Button(
            self.top_frame,
            text="🗑",
            width=3,
            command=lambda: self.model.ed.remove_child(self.model.channel_group, self.channel)
        )

        self.bottom_frame = ttk.Frame(self)

        self.lbl_volume = ttk.Label(self.bottom_frame, text="V:")
        self.var_volume = tk.DoubleVar(self, value=1.0)
        self.inp_volume = ttk.Spinbox(
            self.bottom_frame,
            from_=0.0, to=1.0, increment=0.1,
            width=5,
            textvariable=self.var_volume,
            command=lambda: self.model.ed.set_property(self.channel, "volume", self.var_volume.get())
        )
        self.inp_volume.bind(
            "<Return>",
            lambda e: self.model.ed.set_property(self.channel, "volume", self.var_volume.get())
        )

        self.lbl_pan = ttk.Label(self.bottom_frame, text="P:")
        self.var_pan = tk.DoubleVar(self, value=0.0)
        self.inp_pan = ttk.Spinbox(
            self.bottom_frame,
            from_=-1.0, to=1.0, increment=0.1,
            width=5,
            textvariable=self.var_pan,
            command=lambda: self.model.ed.set_property(self.channel, "pan", self.var_pan.get())
        )
        self.inp_pan.bind(
            "<Return>",
            lambda e: self.model.ed.set_property(self.channel, "pan", self.var_pan.get())
        )

        self.btn_mute = ttk.Button(
            self,
            text="M",
            width=3,
            command=lambda: self.model.ed.toggle_bool(self.channel, "mute")
        )
        self.btn_solo = ttk.Button(
            self,
            text="S",
            width=3,
            command=lambda: self.model.ed.toggle_bool(self.channel, "solo")
        )

        self.btn_move_up = ttk.Button(
            self,
            text="▲",
            width=2,
            command=lambda: self.move_channel(-1)
        )
        self.btn_move_down = ttk.Button(
            self,
            text="▼",
            width=2,
            command=lambda: self.move_channel(1)
        )

        self.lbl_colour.grid(column=0, row=0, **self.padding)
        self.inp_name.grid(column=1, row=0, **self.padding)
        self.btn_delete.grid(column=2, row=0, **self.padding)
        self.top_frame.grid(column=0, row=0, sticky="w")

        self.lbl_volume.grid(column=0, row=0, **self.padding)
        self.inp_volume.grid(column=1, row=0, **self.padding)
        self.lbl_pan.grid(column=2, row=0, **self.padding)
        self.inp_pan.grid(column=3, row=0, **self.padding)
        self.bottom_frame.grid(column=0, row=1, sticky="w")

        self.btn_mute.grid(column=1, row=0, **self.padding)
        self.btn_solo.grid(column=1, row=1, **self.padding)
        self.btn_move_up.grid(column=2, row=0, **self.padding)
        self.btn_move_down.grid(column=2, row=1, **self.padding)

    def update_ui(self):
        self.lbl_colour.config(background=self.channel.get_property("colour"))
        self.btn_mute.state(["pressed" if self.channel.get_property("mute") else "!pressed"])
        self.btn_solo.state(["pressed" if self.channel.get_property("solo") else "!pressed"])
        self.var_name.set(self.channel.get_property("name"))
        self.var_volume.set(self.channel.get_property("volume"))
        self.var_pan.set(self.channel.get_property("pan"))

    def move_channel(self, delta: int):
        self.model.uman.start_group()
        old_index = self.model.channel_group.get_index_of_child(self.channel)
        new_index = old_index + delta
        self.model.ed.remove_child(self.model.channel_group, self.channel)
        self.model.ed.add_child_at_index(self.model.channel_group, self.channel, new_index)
        self.model.uman.end_group()