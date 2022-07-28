import random
import tkinter as tk
import tkinter.ttk as ttk


class PianoRoll(ttk.Frame):
    def __init__(self, parent, pattern: list[int], *args, **kwargs):
        self.pattern = pattern
        self.note_width = 10

        super().__init__(parent, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.init_canvas()
        self.init_scrollbar()
        self.init_controls()
        #self.init_notes()

    def init_canvas(self):
        self.canvas = tk.Canvas(
            self, width=200, height=200,
            scrollregion=(0, 0, self.target_canvas_length(), 200),
            bg="black"
        )

        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.grid(column=0, row=0, sticky="nsew")

    def init_scrollbar(self):
        self.scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.scrollbar["command"] = self.canvas.xview
        self.scrollbar.grid(column=0, row=1, sticky="ew")

    def init_controls(self):
        self.controls = ttk.Frame(self)
        self.controls.grid(column=1, row=0, sticky="ns")

        self.btn_zoom_in = ttk.Button(self.controls, text="Zoom in")
        self.btn_zoom_in.pack()

        self.btn_zoom_out = ttk.Button(self.controls, text="Zoom out")
        self.btn_zoom_out.pack()

    def init_notes(self):
        canvas_height = self.canvas.winfo_height()
        note_height = canvas_height / 25
        print(note_height)
        for index, note in enumerate(self.pattern):
            self.canvas.create_rectangle(
                index * self.note_width,
                note_height * (24 - note),
                (index + 1) * self.note_width,
                note_height * (25 - note),
                fill="red"
            )

    def on_resize(self, event):
        print(self.canvas.winfo_height(), self.canvas.winfo_width())

    def target_canvas_length(self):
        return self.note_width * len(self.pattern)


def main():
    window = tk.Tk()
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    pattern_length = 60
    pattern = [random.randint(0, 24) for _ in range(pattern_length)]

    roll = PianoRoll(window, pattern)
    roll.grid(column=0, row=0, sticky="nsew")
    
    window.after(100, roll.init_notes)
    window.mainloop()

if __name__ == "__main__":
    main()