import tkinter as tk
import tkinter.ttk as ttk

from events import EventBus
from undo_manager import UndoManager
from node_editor import NodeEditor

from pattern import Pattern
from pattern_group import PatternGroup
from channel import Channel
from channel_group import ChannelGroup
from channel_header import ChannelHeader
from sequencer import Sequencer

def test_header():
    uman = UndoManager()
    event_bus = EventBus()
    ed = NodeEditor(uman, event_bus)

    pattern_group = PatternGroup()
    channel = Channel(pattern_group=pattern_group)

    window = tk.Tk()
    window.title("Channel Header")
    window.resizable(False, False)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    header = ChannelHeader(window, channel=channel, ed=ed, event_bus=event_bus)
    header.grid(column=0, row=0, padx=5, pady=5)
    window.rowconfigure(0, minsize=100)

    undo_frame = ttk.Frame(window)
    undo_btn = ttk.Button(undo_frame, text="undo", command=lambda: uman.undo())
    redo_btn = ttk.Button(undo_frame, text="redo", command=lambda: uman.redo())
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    undo_frame.grid(column=1, row=0)

    window.mainloop()

def test_sequencer():
    uman = UndoManager()
    event_bus = EventBus()
    ed = NodeEditor(uman, event_bus)

    pattern_group = PatternGroup()
    channel_group = ChannelGroup()

    pattern = Pattern()
    ed.add_child(pattern_group, pattern)

    channel = Channel(pattern_group=pattern_group)
    ed.add_child(channel_group, channel)
    ed.set_property(channel, "placements", [-1, 0, 0, -1])

    window = tk.Tk()
    window.title("Sequencer")
    window.resizable(False, False)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    sequencer = Sequencer(
        window,
        ed=ed,
        event_bus=event_bus,
        pattern_group=pattern_group,
        channel_group=channel_group,
        height=500,
        width=500
    )
    sequencer.grid(column=0, row=0, padx=5, pady=5)

    undo_frame = ttk.Frame(window)
    undo_btn = ttk.Button(undo_frame, text="undo", command=lambda: uman.undo())
    redo_btn = ttk.Button(undo_frame, text="redo", command=lambda: uman.redo())
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    undo_frame.grid(column=1, row=0)

    window.mainloop()

if __name__ == "__main__":
    test_header()