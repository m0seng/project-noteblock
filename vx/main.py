import tkinter as tk
import tkinter.ttk as ttk

from model import Model
from playback import Playback

from pattern_list import PatternList
from sequencer import Sequencer
from top_frame import TopFrame
from bottom_frame import BottomFrame
 
def main():
    model = Model()

    window = tk.Tk()
    window.title("project noteblock")
    window.columnconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    playback = Playback(model=model, window=window)

    top_frame = TopFrame(window, model=model, playback=playback)

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