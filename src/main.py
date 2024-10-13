import tkinter as tk
import tkinter.ttk as ttk

from model import Model
from instrument_sounds import InstrumentSounds
from playback import Playback
from audio_exporter import AudioExporter

from pattern_list import PatternList
from sequencer import Sequencer
from top_frame import TopFrame
from bottom_frame import BottomFrame
 
def main():
    """Program flow starts here. Everything else is initialized from here."""

    model = Model()

    window = tk.Tk()
    window.title("project noteblock - new song")
    window.columnconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    block_size = 2400
    sounds = InstrumentSounds(block_size=block_size)
    playback = Playback(model=model, window=window, sounds=sounds, block_size=block_size)
    audio_exporter = AudioExporter(model=model, sounds=sounds, block_size=block_size)

    top_frame = TopFrame(window, model=model, playback=playback, audio_exporter=audio_exporter)

    main_frame = ttk.Frame(window)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(0, weight=1)

    pattern_list = PatternList(main_frame, model=model)
    pattern_list.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    sequencer = Sequencer(main_frame, model=model)
    sequencer.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    bottom_frame = BottomFrame(window, model=model)

    top_frame.grid(column=0, row=0, sticky="ew")
    main_frame.grid(column=0, row=1, sticky="nsew")
    bottom_frame.grid(column=0, row=2, sticky="nsew")

    window.mainloop()

if __name__ == "__main__":
    main()