import tkinter as tk
from model import Model
from playback import Playback

def main():
    model = Model()

    pattern_0 = model.new_pattern()
    model.ed.set_property(pattern_0, "notes",
        [8, -1, 8, -1, 20, -1, -1, -1, 15, -1, -1, -1, -1, -1, 14, -1])

    pattern_1 = model.new_pattern()
    model.ed.set_property(pattern_1, "notes",
        [-1, -1, 13, -1, -1, -1, 11, -1, -1, -1, 8, -1, 11, -1, 13, -1])

    channel = model.new_channel()
    model.ed.set_property(channel, "placements", [0, 1] + [-1] * 18)
    model.ed.set_property(channel, "main_instrument", 4)

    window = tk.Tk()
    window.title("Playback Test")

    playback = Playback(model, window)

    window.mainloop()

if __name__ == "__main__":
    main()