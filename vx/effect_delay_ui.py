import tkinter as tk
import tkinter.ttk as ttk

from effect_ui import EffectUI

# TODO: make this!

class EffectDummyUI(EffectUI):
    effect_name = "delay"
    ui_width = 200

    def init_ui(self):
        super().init_ui()
        # initialize UI components here - grid into column 0, row 1
        self.var_delay_ticks = tk.IntVar()
        self.var_dry_mix = tk.DoubleVar()
        self.var_wet_mix = tk.DoubleVar()
        self.var_wet_pan = tk.DoubleVar()

        self.inp_delay_ticks = ttk.Spinbox(
            self, from_=1, to=32, increment=1, width=5,
            textvariable=self.var_delay_ticks,
            command=lambda: self.model.ed.set_property(self.effect, "delay_ticks", self.var_delay_ticks.get())
        )
        self.inp_dry_mix = ttk.Spinbox(
            self, from_=0.0, to=1.0, increment=0.1, width=5,
            textvariable=self.var_dry_mix,
            command=lambda: self.model.ed.set_property(self.effect, "dry_mix", self.var_dry_mix.get())
        )
        self.inp_wet_mix = ttk.Spinbox(
            self, from_=0.0, to=1.0, increment=0.1, width=5,
            textvariable=self.var_wet_mix,
            command=lambda: self.model.ed.set_property(self.effect, "wet_mix", self.var_wet_mix.get())
        )
        self.inp_wet_pan = ttk.Spinbox(
            self, from_=1, to=32, increment=1, width=5,
            textvariable=self.var_wet_pan,
            command=lambda: self.model.ed.set_property(self.effect, "wet_pan", self.var_wet_pan.get())
        )

        self.inp_delay_ticks.bind("<Return>",
            lambda e: self.model.ed.set_property(self.effect, "delay_ticks", self.var_delay_ticks.get()))
        self.inp_dry_mix.bind("<Return>",
            lambda e: self.model.ed.set_property(self.effect, "dry_mix", self.var_dry_mix.get()))
        self.inp_wet_mix.bind("<Return>",
            lambda e: self.model.ed.set_property(self.effect, "wet_mix", self.var_wet_mix.get()))
        self.inp_wet_pan.bind("<Return>",
            lambda e: self.model.ed.set_property(self.effect, "wet_pan", self.var_wet_pan.get()))

    def update_ui(self):
        super().update_ui()
        # update UI components based on self.effect (which will not be None)
        self.var_delay_ticks.set(self.effect.get_property("delay_ticks"))
        self.var_dry_mix.set(self.effect.get_property("var_dry_mix"))
        self.var_wet_mix.set(self.effect.get_property("var_wet_mix"))
        self.var_wet_pan.set(self.effect.get_property("var_wet_pan"))