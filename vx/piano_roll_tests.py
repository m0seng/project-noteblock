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

    piano_roll = PianoRoll(window, ed, pattern_group)
    event_bus.add_listener(piano_roll)
    piano_roll.attach_pattern(pattern)
    piano_roll.grid(column=0, row=0, sticky="nsew")

    window.mainloop()

if __name__ == "__main__":
    main()