from time import perf_counter_ns
import tkinter as tk
import tkinter.ttk as ttk
from . import events

class LoopHijack:
    def __init__(
            self,
            root: tk.Tk,
            event: events.Event,
            tps: int = 20,
            lookahead_ticks: int = 5,
            repeat_ms: int = 25
    ):
        self.root = root
        self.event = event
        self.tps = tps
        self.lookahead_ticks = lookahead_ticks
        self.repeat_ms = repeat_ms

        self.reset()
        self.tick()

    def reset(self):
        self.start_time = self.time_ms()
        self.next_tick = 0

    def time_ms(self) -> int:
        return int(perf_counter_ns() * 0.001)

    def ms_to_tick(self, ms: int) -> int:
        return ms * self.tps * 0.001

    def hijack_root(self):
        self.root.after(self.repeat_ms, self.tick)

    def tick(self):
        elapsed_time = self.time_ms() - self.start_time
        current_tick = self.ms_to_tick(elapsed_time) + self.lookahead_ticks
        while current_tick >= self.next_tick:
            self.event.trigger(time=elapsed_time, tick=self.next_tick)
            self.next_tick += 1
        self.hijack_root()