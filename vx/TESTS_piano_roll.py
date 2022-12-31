import tkinter as tk
import tkinter.ttk as ttk
from model import Model
from old_piano_roll import PianoRoll

def main():
    model = Model()

    pattern = model.new_pattern()
    model.ed.set_property(pattern, "notes", [-1 for _ in range(16)])

    window = tk.Tk()
    window.title("Piano Roll")
    window.resizable(True, False) # Only resize horizontally
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    piano_roll = PianoRoll(window, model=model)
    piano_roll.attach_pattern(pattern)
    piano_roll.grid(column=0, row=0, sticky="nsew")
    
    undo_frame = ttk.Frame(window)
    undo_btn = ttk.Button(undo_frame, text="undo", command=lambda: model.uman.undo())
    redo_btn = ttk.Button(undo_frame, text="redo", command=lambda: model.uman.redo())
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    undo_frame.grid(column=1, row=0)

    window.mainloop()

if __name__ == "__main__":
    main()