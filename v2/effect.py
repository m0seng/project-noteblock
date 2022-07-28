from abc import ABC, abstractmethod
from dataclasses import dataclass
import tkinter as tk
import tkinter.ttk as ttk


@dataclass(slots=True)
class ParameterMeta:
    display_name: str = "placeholder"
    value_format: str = "{value:.2f}"
    min_value: float = 0.0
    max_value: float = 1.0
    init_value: float = 0.5
    quantize: bool = True
    quantize_step: float = 0.1


class Effect(ABC):
    def __init__(self):
        self.define_metadata()
        self.build_parameters()
        self.reset()

    @abstractmethod
    def define_metadata(self):
        """Override this method to define parameter metadata."""
        self.parameters_meta: dict[str, ParameterMeta] = {
            "test": ParameterMeta()
        }

    def build_parameters(self):
        """Builds the parameter dictionary from metadata."""
        self.parameters: dict[str, float] = {}
        for key, meta in self.parameters_meta.items():
            self.parameters[key] = meta.init_value

    @abstractmethod
    def reset(self):
        """Override this method to define/reset internal values such as buffers."""
        pass

    @abstractmethod
    def process_notes(self, tick: int, notes: list["Note"]):
        """Override this method to define how notes are processed."""
        return notes

    @classmethod
    def from_dict(cls, params: dict[str, float]) -> "Effect":
        """Creates Effect from dictionary of parameters."""
        new_effect = Effect()
        new_effect.parameters.update(params)
        return new_effect

    def to_dict(self) -> dict[str, float]:
        """Returns dictionary of parameters."""
        return self.parameters


class EffectUI(tk.Frame):
    def __init__(self, effect: Effect, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in effect.parameters_meta:
            slider = Slider(effect.parameters, effect.parameters_meta, key, master=self)
            slider.pack()


class Slider(tk.Frame):
    def __init__(
        self,
        parameters: dict[str, float],
        parameters_meta: dict[str, ParameterMeta],
        key: str,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.meta = parameters_meta[key]
        self.parameters = parameters
        self.key = key

        self.lbl_title = ttk.Label(self, text=self.meta.display_name)
        self.var_value = tk.DoubleVar(self, value=self.parameters[self.key])
        self.sld_value = ttk.Scale(
            self,
            from_=self.meta.min_value,
            to=self.meta.max_value,
            orient="horizontal",
            variable=self.var_value,
            command=self.slider_changed
        )
        self.lbl_value = ttk.Label(self, text=self.label_format(self.var_value.get(), self.meta.value_format))

        self.lbl_title.pack()
        self.sld_value.pack()
        self.lbl_value.pack()

    def slider_changed(self, event):
        value = self.var_value.get()
        if self.meta.quantize:
            step_number = (value - self.meta.min_value) / self.meta.quantize_step
            step_number = round(step_number)
            value = (step_number * self.meta.quantize_step) + self.meta.min_value
        self.var_value.set(value)
        self.parameters[self.key] = value
        self.lbl_value.configure(text=self.label_format(self.var_value.get(), self.meta.value_format))

    def label_format(self, value: float, format_string: str):
        return format_string.format(value=value)


# def main():
#     effect = Effect()

#     window = tk.Tk()
#     slider = Slider(effect.parameters, effect.parameters_meta, "test")
#     slider.pack()

#     tk.mainloop()

# if __name__ == "__main__":
#     main()