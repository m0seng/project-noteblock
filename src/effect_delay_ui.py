from easy_effect_ui import EasyEffectUI

class EffectDelayUI(EasyEffectUI):
    """UI component - controls for the delay effect."""

    effect_name: str = "delay"
    ui_width: int = 150

    def init_ui(self):
        super().init_ui()
        self.add_spinbox("delay (ticks):", "delay_ticks", 1, 32, 1, int_only=True)
        self.add_spinbox("dry mix:", "dry_mix", 0.0, 1.0, 0.1)
        self.add_spinbox("wet mix:", "wet_mix", 0.0, 1.0, 0.1)
        self.add_spinbox("wet pan:", "wet_pan", -1.0, 1.0, 0.1)

    def update_ui(self):
        super().update_ui()