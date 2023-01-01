from easy_effect_ui import EasyEffectUI

class EffectDelayUI(EasyEffectUI):
    effect_name: str = "delay"
    ui_width: int = 200

    def init_ui(self):
        super().init_ui()
        self.add_spinbox("delay_ticks", 1, 32, 1)
        self.add_spinbox("dry_mix", 0.0, 1.0, 0.1)
        self.add_spinbox("wet_mix", 0.0, 1.0, 0.1)
        self.add_spinbox("wet_pan", -1.0, 1.0, 0.1)

    def update_ui(self):
        super().update_ui()