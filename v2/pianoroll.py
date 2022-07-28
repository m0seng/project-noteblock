import random
import tkinter as tk
import tkinter.ttk as ttk


class PianoRoll(ttk.Frame):
    def __init__(self, parent, pattern: list[int], *args, **kwargs):
        self.black_notes = [0, 2, 4, 7, 9, 12, 14, 16, 19, 21, 24]
        self.note_width = 20
        self.canvas_height = 400
        self.note_height = self.canvas_height / 25

        self.bg_colour = "gray75"
        self.guidebar_colour = "gray70"
        self.guideline_colour = "gray65"
        self.note_colour = "red"

        self.pattern = pattern
        self.pattern_rectangles = []

        super().__init__(parent, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)

        self.init_canvas()
        self.init_scrollbar()
        self.init_controls()

    def init_canvas(self):
        self.canvas = tk.Canvas(
            self, height=self.canvas_height,
            scrollregion=(0, 0, self.target_canvas_length(), self.canvas_height),
            highlightthickness=0,
            bg=self.bg_colour
        )
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<ButtonPress-3>", self.delete_note)
        self.canvas.grid(column=0, row=0, sticky="nsew", padx=5, pady=5)

    def init_scrollbar(self):
        self.scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.scrollbar["command"] = self.canvas.xview
        self.scrollbar.grid(column=0, row=1, sticky="ew", padx=5, pady=5)

    def init_controls(self):
        self.controls = ttk.Frame(self)

        self.btn_zoom_in = ttk.Button(self.controls, text="Zoom in")
        self.btn_zoom_in.pack()

        self.btn_zoom_out = ttk.Button(self.controls, text="Zoom out")
        self.btn_zoom_out.pack()

        self.controls.grid(column=1, row=0, sticky="ns", padx=5, pady=5)

    def draw_everything(self):
        self.canvas.delete("all")
        self.draw_guide_bars()
        self.draw_guide_lines()
        self.draw_pattern_notes()

    def draw_pattern_notes(self):
        self.pattern_rectangles = []
        for tick, note in enumerate(self.pattern):
            if note is not None:
                self.pattern_rectangles.append(self.draw_note(note, tick, length=1, fill=self.note_colour))
            else:
                self.pattern_rectangles.append(None)

    def draw_guide_bars(self):
        for note in self.black_notes:
            self.draw_note(note, 0, len(self.pattern), fill=self.guidebar_colour, outline="")

    def draw_guide_lines(self):
        for index, _ in enumerate(self.pattern):
            self.canvas.create_line(
                index * self.note_width,
                0,
                index * self.note_width,
                self.canvas_height,
                fill=self.guideline_colour,
                width=0
            )

    def draw_note(self, note: int, tick: int, length: int, **kwargs):
        return self.canvas.create_rectangle(
            tick * self.note_width,
            self.note_height * (24 - note),
            (tick + length) * self.note_width,
            self.note_height * (25 - note),
            **kwargs
        )

    def get_note_at_coords(self, x: int, y: int):
        canvas_x = self.canvas.canvasx(x)
        canvas_y = self.canvas.canvasy(y)
        tick = int(canvas_x // self.note_width)
        note = int(24 - (canvas_y // self.note_height))
        return note, tick

    def delete_note(self, event: tk.Event):
        note, tick = self.get_note_at_coords(event.x, event.y)
        if self.pattern[tick] == note:
            self.canvas.delete(self.pattern_rectangles[tick])
            self.pattern[tick] = None
            self.pattern_rectangles[tick] = None

    def on_resize(self, event: tk.Event):
        print(self.canvas.winfo_height(), self.canvas.winfo_width())

    def target_canvas_length(self):
        return self.note_width * len(self.pattern)


def main():
    window = tk.Tk()
    window.title("Piano Roll")
    window.resizable(True, False)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    pattern_length = 60
    pattern = []
    pattern_note_chance = 0.5
    for _ in range(pattern_length):
        if random.random() < pattern_note_chance:
            pattern.append(random.randint(0, 24))
        else:
            pattern.append(None)

    roll = PianoRoll(window, pattern)
    roll.grid(column=0, row=0, sticky="nsew")
    
    window.after(100, roll.draw_everything)
    window.mainloop()

if __name__ == "__main__":
    main()