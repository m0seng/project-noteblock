from time import perf_counter_ns
from typing import Callable
import tkinter as tk

class LoopHijacker:
    def __init__(
            self,
            root: tk.Tk,
            callback: Callable,
            tps: int = 20,
            lookahead_ticks: int = 5,
            repeat_ms: int = 25
    ):
        self.root = root
        self.callback = callback
        self.tps = tps
        self.lookahead_ticks = lookahead_ticks
        self.repeat_ms = repeat_ms
        self.enabled: bool = False
        self.reset()

    def reset(self):
        self.start_time = self.time_ms()
        self.next_tick = 0

    def enable(self):
        if not self.enabled:
            self.enabled = True
            self.update()

    def disable(self):
        self.enabled = False

    def hijack_root(self):
        self.root.after(self.repeat_ms, self.update)

    def update(self):
        elapsed_time = self.time_ms() - self.start_time
        current_tick = self.ms_to_tick(elapsed_time) + self.lookahead_ticks
        while current_tick >= self.next_tick:
            self.callback() # TODO: add parameters here?
            self.next_tick += 1
        if self.enabled: self.hijack_root()

    def time_ms(self) -> int:
        return int(perf_counter_ns() * 0.001)

    def ms_to_tick(self, ms: int) -> int:
        return int(ms * self.tps * 0.001)