import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import EventBus, Listener
from node_editor import NodeEditor
from model import Model

from channel import Channel

class InstrumentEditor(Listener, ttk.Frame):
    instrument_names = [
        "harp",
        "basedrum",
        "snare",
        "hat",
        "bass",
        "flute",
        "bell",
        "guitar",
        "chime",
        "xylophone",
        "iron_xylophone",
        "cow_bell",
        "didgeridoo",
        "bit",
        "banjo",
        "pling",
    ]

    def __init__(self, parent, *args, model: Model, channel: Channel, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model
        self.channel = channel

        self.columnconfigure(0, weight=1)

        self.init_ui()
        self.model.event_bus.add_listener(self)
        self.update_ui()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_property_set(self, node: Node, key, old_value, new_value):
        if node is self.channel:
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
            lambda e: self.model.ed.set_property(self.channel, "name", self.var_name.get())
        )

        self.lf_main = ttk.Labelframe(self, text="main instrument")

        self.var_main_instrument = tk.StringVar(self.lf_main)
        self.cmb_main_instrument = ttk.OptionMenu(
            self.lf_main,
            self.var_main_instrument,
            self.instrument_names[0],
            *self.instrument_names,
            command=lambda e: self.model.ed.set_property(
                self.channel,
                "main_instrument",
                self.instrument_names.index(self.var_main_instrument.get()))
        )

        self.lf_sustain = ttk.Labelframe(self, text="sustain instrument")

        self.var_sustain_enabled = tk.BooleanVar(self.lf_sustain)
        self.chk_sustain_enabled = ttk.Checkbutton(
            self.lf_sustain,
            text="enabled?",
            variable=self.var_sustain_enabled,
            command=lambda: self.model.ed.set_property(
                self.channel,
                "sustain_enabled",
                self.var_sustain_enabled.get()
            )
        )

        self.var_sustain_instrument = tk.StringVar(self.lf_sustain)
        self.cmb_sustain_instrument = ttk.OptionMenu(
            self.lf_sustain,
            self.var_sustain_instrument,
            self.instrument_names[0],
            *self.instrument_names,
            command=lambda e: self.model.ed.set_property(
                self.channel,
                "sustain_instrument",
                self.instrument_names.index(self.var_sustain_instrument.get()))
        )

        self.var_sustain_mix = tk.DoubleVar(self.lf_sustain)
        self.inp_sustain_mix = ttk.Spinbox(
            self.lf_sustain,
            from_=0.0, to=1.0, increment=0.1,
            width=5,
            textvariable=self.var_sustain_mix,
            command=lambda: self.model.ed.set_property(self.channel, "sustain_mix", self.var_sustain_mix.get())
        )
        self.inp_sustain_mix.bind(
            "<Return>",
            lambda e: self.model.ed.set_property(self.channel, "volume", self.var_sustain_mix.get())
        )

        self.cmb_main_instrument.grid(column=0, row=0)
        self.chk_sustain_enabled.grid(column=0, row=0)
        self.cmb_sustain_instrument.grid(column=0, row=1)
        self.inp_sustain_mix.grid(column=0, row=2)
        self.inp_name.grid(column=0, row=0)
        self.lf_main.grid(column=0, row=1)
        self.lf_sustain.grid(column=0, row=2)

    def update_ui(self):
        self.var_name.set(self.channel.get_property("name"))
        self.var_main_instrument.set(self.instrument_names[self.channel.get_property("main_instrument")])
        self.var_sustain_enabled.set(self.channel.get_property("sustain_enabled"))
        self.var_sustain_instrument.set(self.instrument_names[self.channel.get_property("sustain_instrument")])
        self.var_sustain_mix.set(self.channel.get_property("sustain_mix"))