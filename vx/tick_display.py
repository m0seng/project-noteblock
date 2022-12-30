import tkinter as tk
import tkinter.ttk as ttk

from events import Listener
from model import Model

# NOTE: obsolete

class TickDisplay(Listener, ttk.Frame):
    def __init__(self, parent, *args, model: Model, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model = model

        self.init_ui()
        self.model.event_bus.add_listener(self)
    
    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def tick_processed(self, mono_tick: int, sequence_enabled: bool, bar_number: int, pat_tick: int):
        self.var_tick.set(f"{bar_number}.{pat_tick}")

    def init_ui(self):
        self.var_tick = tk.StringVar()
        self.lbl_tick = ttk.Label(
            self,
            width=10,
            justify=tk.CENTER,
            textvariable=self.var_tick
        )
        self.lbl_tick.grid(column=0, row=0)