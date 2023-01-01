import tkinter as tk
from easy_effect_ui import EasyEffectUI

class EffectDelayUI(EasyEffectUI):
    effect_name: str = "delay"
    ui_width: int = 200

    def init_ui(self):
        super().init_ui()
        self.add_spinbox("delay (ticks):", "delay_ticks", tk.IntVar(), 1, 32, 1)
        self.add_spinbox("dry mix:", "dry_mix", tk.DoubleVar(), 0.0, 1.0, 0.1)
        self.add_spinbox("wet mix:", "wet_mix", tk.DoubleVar(), 0.0, 1.0, 0.1)
        self.add_spinbox("wet pan:", "wet_pan", tk.DoubleVar(), -1.0, 1.0, 0.1)

    def update_ui(self):
        super().update_ui()