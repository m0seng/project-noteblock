import tkinter as tk
import tkinter.ttk as ttk

from model import Model

from pattern_list import PatternList
from sequencer import Sequencer
from bottom_notebook import BottomNotebook

def test_sequencer():
    model = Model()
    model.new_channel()
    model.new_pattern()

    window = tk.Tk()
    window.title("humu humu")
    window.columnconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    main_frame = ttk.Frame(window)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(0, weight=1)

    pattern_list = PatternList(main_frame, model=model)
    pattern_list.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    sequencer = Sequencer(main_frame, model=model)
    sequencer.grid(column=1, row=0, padx=5, pady=5, sticky="nsew")

    stuff_frame = ttk.Frame(main_frame)
    undo_btn = ttk.Button(stuff_frame, text="undo", command=lambda: model.uman.undo())
    redo_btn = ttk.Button(stuff_frame, text="redo", command=lambda: model.uman.redo())
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    stuff_frame.grid(column=2, row=0)

    main_frame.grid(column=0, row=1, sticky="nsew")

    bottom_notebook = BottomNotebook(window, model=model)
    bottom_notebook.grid(column=0, row=2, sticky="nsew")

    window.mainloop()

if __name__ == "__main__":
    test_sequencer()