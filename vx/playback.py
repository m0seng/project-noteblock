import numpy as np
from events import Listener
from model import Model
from tick_manager import TickManager
from loop_hijacker import LoopHijacker
from audio_generator import AudioGenerator

class Playback(Listener):
    def __init__(self, model: Model, window, block_size: int = 2048):
        self.model = model
        self.model.event_bus.add_listener(self)

        self.tick_manager = TickManager(model=model)
        self.loop_hijacker = LoopHijacker(
            root=window,
            callback=self.tick,
            tps=20,
            lookahead_ticks=3,
            repeat_ms=25
        )
        self.audio_generator = AudioGenerator(block_size=block_size)

        self.playback_enabled: bool = False
        self.start_bar: int = 0

    def bar_selected(self, bar: int):
        self.start_bar = bar
        if not self.playback_enabled:
            self.tick_manager.set_tick(bar_number=bar, pat_tick=0)

    def play(self):
        self.loop_hijacker.enable()
        self.playback_enabled = True

    def pause(self):
        self.loop_hijacker.disable()
        self.playback_enabled = False

    def stop(self):
        self.pause()
        self.tick_manager.set_tick(bar_number=self.start_bar, pat_tick=0)

    def tick(self):
        next_tick = self.tick_manager.next_tick()
        notes = self.model.channel_group.tick(*next_tick)
        audio_block: np.ndarray = self.audio_generator.tick(notes)