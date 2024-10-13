import numpy as np
import soundfile

from model import Model
from tick_manager import TickManager
from instrument_sounds import InstrumentSounds
from audio_generator import AudioGenerator

class AudioExporter:
    """Turns a song into audio (without waiting for real-time) and writes it to a .wav file."""

    def __init__(self, model: Model, sounds: InstrumentSounds, block_size: int = 2400):
        self.model = model
        self.sounds = sounds
        self.block_size = block_size

    def export(self, filename: str):
        tick_manager = TickManager(model=self.model, ignore_loop=True)
        audio_generator = AudioGenerator(block_size=self.block_size, sounds=self.sounds)

        audio_blocks: list[np.ndarray] = []
        tick_manager.set_tick(0, 0)

        # workaround for clearing effects when exporting: just run the buffer a bit
        tick_manager.disable_sequence()
        for _ in range(32): # arbitrary number, might need to increase this
            next_tick = tick_manager.next_tick()
            self.model.channel_group.tick(*next_tick)
        tick_manager.enable_sequence()

        while tick_manager.sequence_enabled:
            next_tick = tick_manager.next_tick()
            notes = self.model.channel_group.tick(*next_tick)
            audio_block: np.ndarray = audio_generator.tick(notes)
            audio_blocks.append(audio_block)

        final_audio = np.concatenate(audio_blocks, axis=0)
        soundfile.write(filename, final_audio, samplerate=48000)