from time import perf_counter_ns
import tkinter as tk
import tkinter.ttk as ttk
from event import Event

class LoopHijack:
    def __init__(self, root: tk.Tk, event: Event):
        self.root = root
        self.event = event

        self.tps = 20
        self.tick_ms = 1000 / self.tps

        self.lookahead_ticks = 5
        self.repeat_ms = 25
        self.reset()

    def reset(self):
        self.start_time = self.time_ms()
        self.next_tick = 0

    def time_ms(self) -> int:
        return int(perf_counter_ns() * 0.001)

    def ms_to_tick(self, ms: int) -> int:
        return ms // self.tick_ms

    def hijack_root(self):
        self.root.after(self.repeat_ms, self.tick)

    def tick(self):
        elapsed_time = self.time_ms() - self.start_time
        current_tick = self.ms_to_tick(elapsed_time) + self.lookahead_ticks
        while current_tick >= self.next_tick:
            self.event.trigger(tick=self.next_tick)
            self.next_tick += 1
        self.hijack_root()