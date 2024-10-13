import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import Listener
from model import Model

from channel import Channel

from effect_dummy import EffectDummy
from effect_delay import EffectDelay

class EffectAddFrame(Listener, ttk.Frame):
    """UI component - used to add effects to a channel's effect rack."""

    effects = {
        "dummy": EffectDummy,
        "delay": EffectDelay,
    }
    effect_names = list(effects.keys())

    def __init__(self, parent, model: Model, **kwargs):
        super().__init__(parent, **kwargs)
        self.model = model
        self.channel: Channel | None = None

        self.init_ui()
        self.model.event_bus.add_listener(self)
        self.update_ui()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

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
        self.var_effect = tk.StringVar(self)
        self.cmb_effect = ttk.OptionMenu(
            self,
            self.var_effect,
            self.effect_names[0],
            *self.effect_names
        )
        self.btn_add_effect = ttk.Button(
            self,
            text="+ add effect",
            command=lambda: self.add_effect(self.var_effect.get())
        )

        self.cmb_effect.grid(column=0, row=0, sticky="ew")
        self.btn_add_effect.grid(column=0, row=1, sticky="ew")

    def add_effect(self, name: str):
        effect_class = self.effects[name]
        effect_node = effect_class()
        self.model.ed.add_child(self.channel, effect_node)

    def update_ui(self):
        if self.channel is None:
            self.set_all_states(["disabled"])
        else:
            self.set_all_states(["!disabled"])

    def set_all_states(self, statespec: list[str]):
        for component in (self.cmb_effect, self.btn_add_effect):
            component.state(statespec)