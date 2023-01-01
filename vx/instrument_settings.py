import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import Listener
from model import Model

from channel import Channel

class InstrumentSettings(Listener, ttk.Frame):
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

    padding = {"padx": 5, "pady": 5}

    def __init__(self, parent, model: Model, **kwargs):
        super().__init__(parent, **kwargs)
        self.model = model
        self.channel: Channel | None = None

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

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        if child is self.channel:
            self.channel = None
            self.update_ui()

    def node_selected(self, node: Node):
        if isinstance(node, Channel):
            self.channel = node
            self.update_ui()

    def reset_ui(self):
        self.channel = None
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

        self.lbl_sustain_mix = ttk.Label(self.lf_sustain, text="mix:")
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

        self.cmb_main_instrument.grid(column=0, row=0, sticky="w", **self.padding)
        self.chk_sustain_enabled.grid(column=0, row=0, columnspan=2, **self.padding)
        self.cmb_sustain_instrument.grid(column=0, row=1, columnspan=2, sticky="w", **self.padding)
        self.lbl_sustain_mix.grid(column=0, row=2, **self.padding)
        self.inp_sustain_mix.grid(column=1, row=2, **self.padding)
        self.inp_name.grid(column=0, row=0, sticky="ew", **self.padding)
        self.lf_main.grid(column=0, row=1, sticky="ew", **self.padding)
        self.lf_sustain.grid(column=0, row=2, sticky="ew", **self.padding)

    def update_ui(self):
        if self.channel is None:
            self.set_all_states(["disabled"])
        else:
            self.set_all_states(["!disabled"])
            self.var_name.set(self.channel.get_property("name"))
            self.var_main_instrument.set(self.instrument_names[self.channel.get_property("main_instrument")])
            self.var_sustain_enabled.set(self.channel.get_property("sustain_enabled"))
            self.var_sustain_instrument.set(self.instrument_names[self.channel.get_property("sustain_instrument")])
            self.var_sustain_mix.set(self.channel.get_property("sustain_mix"))
            for component in (self.cmb_sustain_instrument, self.inp_sustain_mix, self.lbl_sustain_mix):
                component.state(["!disabled" if self.channel.get_property("sustain_enabled") else "disabled"])

    def set_all_states(self, statespec: list[str]):
        for component in (self.inp_name, self.cmb_main_instrument, self.chk_sustain_enabled,
                self.cmb_sustain_instrument, self.lbl_sustain_mix, self.inp_sustain_mix):
            component.state(statespec)