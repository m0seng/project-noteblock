import tkinter as tk
import tkinter.ttk as ttk

from node_events import NodeEventBus
from undo_manager import UndoManager
from node_editor import NodeEditor
from coordinator import Coordinator

from pattern_group import PatternGroup
from pattern import Pattern
from piano_roll import PianoRoll

def main():
    coordinator = Coordinator()

    pattern_group = PatternGroup()
    pattern = Pattern()
    coordinator.ed.set_property(pattern, "notes", [-1 for _ in range(16)])

    coordinator.ed.add_child(pattern_group, pattern)

    window = tk.Tk()
    window.title("Piano Roll")
    window.resizable(True, False) # Only resize horizontally
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    piano_roll = PianoRoll(window, coordinator=coordinator, pattern_group=pattern_group)
    piano_roll.attach_pattern(pattern)
    piano_roll.grid(column=0, row=0, sticky="nsew")

    # test_buttons = ttk.Frame(window)
    # test_buttons.grid(column=1, row=0, sticky="ns", padx=5, pady=5)

    # evil_button = ttk.Button(test_buttons, text="evil button", command=lambda: ed.remove_child(pattern_group, pattern))
    # evil_button.grid(column=0, row=0)

    # def good_function():
    #     ed.add_child(pattern_group, pattern)
    #     piano_roll.attach_pattern(pattern)

    # good_button = ttk.Button(test_buttons, text="good button", command=good_function)
    # good_button.grid(column=0, row=1)

    undo_frame = ttk.Frame(window)
    undo_btn = ttk.Button(undo_frame, text="undo", command=lambda: coordinator.uman.undo())
    redo_btn = ttk.Button(undo_frame, text="redo", command=lambda: coordinator.uman.redo())
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    undo_frame.grid(column=1, row=0)

    window.mainloop()

if __name__ == "__main__":
    main()