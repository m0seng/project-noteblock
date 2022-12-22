import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import EventBus, Listener
from node_editor import NodeEditor
from channel import Channel

class ChannelHeader(Listener, ttk.Frame):
    def __init__(self, parent, *args, ed: NodeEditor, event_bus: EventBus, channel: Channel, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.channel = channel
        self.ed = ed
        self.event_bus = event_bus
        
        self.init_ui()
        self.event_bus.add_listener(self)
        self.update_ui()

    def destroy(self, *args, **kwargs):
        self.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_property_set(self, node: Node, key, old_value, new_value):
        if node is self.channel:
            self.update_ui()

    def node_child_added(self, parent: Node, child: Node, id: int, index: int):
        ...

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        ...

    def node_selected(self, node: Node):
        ...

    def init_ui(self):
        self.btn_mute = ttk.Button(
            self,
            text="M",
            width=3,
            command=lambda: self.ed.toggle_bool(self.channel, "mute")
        )
        self.btn_solo = ttk.Button(
            self,
            text="S",
            width=3,
            command=lambda: self.ed.toggle_bool(self.channel, "solo")
        )

        self.lbl_colour = ttk.Label(self, width=2)

        self.var_name = tk.StringVar(self)
        self.inp_name = ttk.Entry(
            self,
            width=15,
            textvariable=self.var_name,
        )
        self.inp_name.bind("<Return>", lambda e: self.ed.set_property(self.channel, "name", self.var_name.get()))

        self.lbl_volume = ttk.Label(self, text="V:")
        self.var_volume = tk.DoubleVar(self, value=1.0)
        self.inp_volume = ttk.Spinbox(
            self,
            from_=0.0,
            to=1.0,
            increment=0.1,
            width=5,
            textvariable=self.var_volume,
            command=lambda: self.ed.set_property(self.channel, "volume", self.var_volume.get())
        )
        self.inp_volume.bind("<Return>", lambda e: self.ed.set_property(self.channel, "volume", self.var_volume.get()))

        self.lbl_pan = ttk.Label(self, text="P:")
        self.var_pan = tk.DoubleVar(self, value=0.0)
        self.inp_pan = ttk.Spinbox(
            self,
            from_=-1.0,
            to=1.0,
            increment=0.1,
            width=5,
            textvariable=self.var_pan,
            command=lambda: self.ed.set_property(self.channel, "pan", self.var_pan.get())
        )
        self.inp_pan.bind("<Return>", lambda e: self.ed.set_property(self.channel, "pan", self.var_pan.get()))

        self.lbl_colour.grid(column=0, row=0)
        self.inp_name.grid(column=1, row=0, columnspan=3, sticky="w")
        self.lbl_volume.grid(column=0, row=1)
        self.inp_volume.grid(column=1, row=1)
        self.lbl_pan.grid(column=2, row=1)
        self.inp_pan.grid(column=3, row=1)
        self.btn_mute.grid(column=4, row=0)
        self.btn_solo.grid(column=4, row=1)

        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=2)

    def update_ui(self):
        self.lbl_colour.config(background=self.channel.get_property("colour"))
        self.btn_mute.state(["pressed" if self.channel.get_property("mute") else "!pressed"])
        self.btn_solo.state(["pressed" if self.channel.get_property("solo") else "!pressed"])
        self.var_name.set(self.channel.get_property("name"))
        self.var_volume.set(self.channel.get_property("volume"))
        self.var_pan.set(self.channel.get_property("pan"))