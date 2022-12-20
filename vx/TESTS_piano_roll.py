import tkinter as tk
import tkinter.ttk as ttk

from node_events import NodeEventBus
from undo_manager import UndoManager
from node_editor import NodeEditor

from pattern_group import PatternGroup
from pattern import Pattern

from piano_roll import PianoRoll

def main():
    uman = UndoManager()
    event_bus = NodeEventBus()
    ed = NodeEditor(uman, event_bus)

    pattern_group = PatternGroup()
    pattern = Pattern()
    ed.set_property(pattern, "notes", [1,2,3,4,5,6,7,8,-2])

    ed.add_child(pattern_group, pattern)

    window = tk.Tk()
    window.title("Piano Roll")
    window.resizable(True, False) # Only resize horizontally
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    piano_roll = PianoRoll(window, ed, event_bus, pattern_group)
    piano_roll.attach_pattern(pattern)
    piano_roll.grid(column=0, row=0, sticky="nsew")

    test_buttons = ttk.Frame(window)
    test_buttons.grid(column=1, row=0, sticky="ns", padx=5, pady=5)

    evil_button = ttk.Button(test_buttons, text="evil button", command=lambda: ed.remove_child(pattern_group, pattern))
    evil_button.grid(column=0, row=0)

    def good_function():
        ed.add_child(pattern_group, pattern)
        piano_roll.attach_pattern(pattern)

    good_button = ttk.Button(test_buttons, text="good button", command=good_function)
    good_button.grid(column=0, row=1)

    window.mainloop()

if __name__ == "__main__":
    main()