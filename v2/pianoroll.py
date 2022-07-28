import tkinter as tk
import tkinter.ttk as ttk


class PianoRoll(ttk.Frame):
    def __init__(self, parent, pattern: list[int], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.pattern = pattern

        self.canvas = tk.Canvas(self, width=200, height=200, bg="black")
        self.canvas.create_rectangle(10, 10, 90, 90, fill="red")
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.grid(column=0, row=0, sticky="nsew")

    def on_resize(self, event):
        print(self.canvas.winfo_height(), self.canvas.winfo_width())


def main():
    window = tk.Tk()
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    roll = PianoRoll(window, [])
    roll.grid(column=0, row=0, sticky="nsew")

    window.mainloop()

if __name__ == "__main__":
    main()