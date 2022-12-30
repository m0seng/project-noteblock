import tkinter as tk
import tkinter.ttk as ttk

from model import Model

from pattern_list import PatternList

def test_sequencer():
    model = Model()
    model.new_pattern()

    window = tk.Tk()
    window.title("Pattern List")
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    pattern_list = PatternList(window, model=model)
    pattern_list.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    stuff_frame = ttk.Frame(window)
    undo_btn = ttk.Button(stuff_frame, text="undo", command=lambda: model.uman.undo())
    redo_btn = ttk.Button(stuff_frame, text="redo", command=lambda: model.uman.redo())
    add_pattern_btn = ttk.Button(stuff_frame, text="add channel", command=model.new_pattern)
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    add_pattern_btn.grid(column=0, row=2)
    stuff_frame.grid(column=1, row=0)

    window.mainloop()

if __name__ == "__main__":
    test_sequencer()