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

    def __init__(self, parent, model: Model, channel: Channel, **kw):
        super().__init__(parent, **kw)
        self.model = model
        self.channel = channel

        self.init_ui()
        self.model.event_bus.add_listener(self)
        self.update_ui()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_property_set(self, node: Node, key, old_value, new_value):
        if node is self.channel:
            self.update_ui()

    def update_ui(self):
        self.var_name.set(self.channel.get_property("name"))
        self.var_main_instrument.set(
            self.instrument_names[self.channel.get_property("main_instrument")])
        self.var_sustain_enabled.set(
            self.channel.get_property("sustain_enabled"))
        self.var_sustain_instrument.set(
            self.instrument_names[self.channel.get_property("sustain_instrument")])
        self.var_sustain_mix.set(self.channel.get_property("sustain_mix"))
        self.opt_sustain_instrument.state(
            ["!disabled" if self.channel.get_property("sustain_enabled") else "disabled"])
        self.inp_sustain_mix.state(
            ["!disabled" if self.channel.get_property("sustain_enabled") else "disabled"])
        self.lbl_sustain_mix.state(
            ["!disabled" if self.channel.get_property("sustain_enabled") else "disabled"])

    def init_ui(self):
        # generated with pygubu
        self.inp_name = ttk.Entry(self)
        self.var_name = tk.StringVar()
        self.inp_name.configure(state="normal", textvariable=self.var_name)
        self.inp_name.grid(column=0, padx=5, pady=5, row=0, sticky="ew")
        self.lf_main = ttk.Labelframe(self)
        self.lf_main.configure(text='main instrument')
        self.var_main_instrument = tk.StringVar()
        self.opt_main_instrument = ttk.OptionMenu(
            self.lf_main, self.var_main_instrument, None, *self.instrument_names,
            command=lambda: self.model.ed.set_property(
                self.channel,
                "main_instrument",
                self.instrument_names.index(self.var_main_instrument.get())
            ))
        self.opt_main_instrument.grid(
            column=0, padx=5, pady=5, row=0, sticky="w")
        self.lf_main.grid(column=0, padx=5, pady=5, row=1, sticky="ew")
        self.lf_sustain = ttk.Labelframe(self)
        self.lf_sustain.configure(text='sustain instrument')
        self.chk_sustain_enabled = ttk.Checkbutton(self.lf_sustain)
        self.var_sustain_enabled = tk.BooleanVar()
        self.chk_sustain_enabled.configure(
            text='enabled?', variable=self.var_sustain_enabled)
        self.chk_sustain_enabled.grid(
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            row=0,
            sticky="w")
        self.chk_sustain_enabled.configure(command=lambda: self.model.ed.set_property(
            self.channel,
            "sustain_enabled",
            self.var_sustain_enabled.get()
        ))
        self.var_sustain_instrument = tk.StringVar()
        self.opt_sustain_instrument = ttk.OptionMenu(
            self.lf_sustain,
            self.var_sustain_instrument,
            None,
            *self.instrument_names,
            command=lambda: self.model.ed.set_property(
                self.channel,
                "sustain_instrument",
                self.instrument_names.index(self.var_sustain_instrument.get())
            ))
        self.opt_sustain_instrument.grid(
            column=0, columnspan=2, padx=5, pady=5, row=1, sticky="w")
        self.inp_sustain_mix = ttk.Spinbox(self.lf_sustain)
        self.var_sustain_mix = tk.DoubleVar()
        self.inp_sustain_mix.configure(
            from_=0.0,
            increment=0.1,
            textvariable=self.var_sustain_mix,
            to=1.0,
            width=5)
        self.inp_sustain_mix.grid(column=1, padx=5, pady=5, row=2, sticky="w")
        self.inp_sustain_mix.configure(command=lambda: self.model.ed.set_property(
            self.channel,
            "sustain_mix",
            self.var_sustain_mix.get()
        ))
        self.inp_sustain_mix.bind("<Enter>", lambda e: self.model.ed.set_property(
            self.channel,
            "sustain_mix",
            self.var_sustain_mix.get()
        ), add="")
        self.lbl_sustain_mix = ttk.Label(self.lf_sustain)
        self.lbl_sustain_mix.configure(text='mix:')
        self.lbl_sustain_mix.grid(column=0, padx=5, pady=5, row=2)
        self.lf_sustain.grid(column=0, padx=5, pady=5, row=2, sticky="ew")
        self.configure(padding=5)
