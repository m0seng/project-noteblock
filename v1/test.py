import numpy as np
import soundfile
import time

from channel import Channel
from player import Player

def main():
    channels = [Channel()]
    player = Player(block_size=2205)
    sound_blocks = []

    start_time = time.perf_counter()
    for timestamp in range(100):
        notes = []
        for channel in channels:
            notes += channel.get_notes(timestamp)
        sound = player.tick(notes)
        sound_blocks.append(sound)
    elapsed_time = time.perf_counter() - start_time
    print(elapsed_time)

    final_sound = np.concatenate(sound_blocks, axis=0)
    soundfile.write("test.wav", final_sound, 44100)

if __name__ == "__main__":
    main()