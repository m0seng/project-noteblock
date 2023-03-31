import queue
import numpy as np
from events import Listener
from model import Model
from tick_manager import TickManager
from loop_hijacker import LoopHijacker
from instrument_sounds import InstrumentSounds
from audio_generator import AudioGenerator
from audio_player import AudioPlayer

class Playback(Listener):
    """Coordinates real-time playback of a song."""

    def __init__(self, model: Model, window, sounds: InstrumentSounds, block_size: int = 2400):
        self.model = model
        self.model.event_bus.add_listener(self)
        self.start_bar: int = 0

        self.tick_manager = TickManager(model=model)
        self.loop_hijacker = LoopHijacker(
            root=window,
            callback=self.tick,
            tps=20,
            lookahead_ticks=3,
            repeat_ms=50
        )
        
        self.audio_generator = AudioGenerator(block_size=block_size, sounds=sounds)
        self.audio_queue = queue.Queue(maxsize=10) # a bit arbitrary

        self.audio_player = AudioPlayer(self.audio_queue)
        self.loop_hijacker.enable()

    def bar_selected(self, bar: int):
        self.start_bar = bar
        if not self.tick_manager.sequence_enabled:
            self.tick_manager.set_tick(bar_number=bar, pat_tick=0)

    def play(self):
        self.tick_manager.enable_sequence()

    def pause(self):
        self.tick_manager.disable_sequence()

    def stop(self):
        self.pause()
        self.tick_manager.set_tick(bar_number=self.start_bar, pat_tick=0)

    def tick(self):
        next_tick = self.tick_manager.next_tick()
        notes = self.model.channel_group.tick(*next_tick)
        audio_block: np.ndarray = self.audio_generator.tick(notes)
        self.audio_queue.put(audio_block)