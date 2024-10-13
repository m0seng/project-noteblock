import tkinter as tk
import tkinter.ttk as ttk

from effect_ui import EffectUI

class EffectDummyUI(EffectUI):
    """UI component - UI for the dummy effect."""

    effect_name = "dummy effect"
    ui_width = 200

    def init_ui(self):
        super().init_ui()
        # initialize UI components here - grid into column 0, row 1
        self.label = ttk.Label(self, text="dummy effect")
        self.label.grid(column=0, row=1, sticky="nsew", padx=5, pady=5)

    def update_ui(self):
        super().update_ui()
        ... # update UI components based on self.effect (which will not be None)