import tkinter as tk
import tkinter.ttk as ttk

from events import EventBus
from undo_manager import UndoManager
from node_editor import NodeEditor
from model import Model

from pattern import Pattern
from pattern_group import PatternGroup
from channel import Channel
from channel_group import ChannelGroup
from channel_header import ChannelHeader
from channel_header_canvas import ChannelHeaderCanvas
from placement_display import PlacementDisplay
from sequencer import Sequencer
from instrument_editor import InstrumentEditor

def test_header():
    model = Model()
    channel = model.new_channel()

    window = tk.Tk()
    window.title("Channel Header")
    window.resizable(False, False)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    header = ChannelHeader(window, model=model, channel=channel)
    header.grid(column=0, row=0, padx=5, pady=5)
    window.rowconfigure(0, minsize=100)

    undo_frame = ttk.Frame(window)
    undo_btn = ttk.Button(undo_frame, text="undo", command=lambda: model.uman.undo())
    redo_btn = ttk.Button(undo_frame, text="redo", command=lambda: model.uman.redo())
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    undo_frame.grid(column=1, row=0)

    window.mainloop()

def test_header_canvas():
    model = Model()
    model.new_channel()
    model.new_channel()
    model.new_channel()

    window = tk.Tk()
    window.title("Channel Headers")
    # window.resizable(False, False)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    header = ChannelHeaderCanvas(window, model=model)
    header.grid(column=0, row=0, padx=5, pady=5)

    stuff_frame = ttk.Frame(window)
    undo_btn = ttk.Button(stuff_frame, text="undo", command=lambda: model.uman.undo())
    redo_btn = ttk.Button(stuff_frame, text="redo", command=lambda: model.uman.redo())
    add_channel_btn = ttk.Button(stuff_frame, text="add button", command=model.new_channel)
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    add_channel_btn.grid(column=0, row=2)
    stuff_frame.grid(column=1, row=0)

    window.mainloop()

def test_instrument_editor():
    model = Model()
    channel = model.new_channel()

    window = tk.Tk()
    window.title("Instrument Editor")
    window.resizable(False, False)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    editor = InstrumentEditor(window, model=model, channel=channel)
    editor.grid(column=0, row=0, padx=5, pady=5)

    undo_frame = ttk.Frame(window)
    undo_btn = ttk.Button(undo_frame, text="undo", command=lambda: model.uman.undo())
    redo_btn = ttk.Button(undo_frame, text="redo", command=lambda: model.uman.redo())
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    undo_frame.grid(column=1, row=0)

    window.mainloop()

def test_placement_display():
    model = Model()
    pattern = model.new_pattern()
    channel = model.new_channel()
    model.ed.set_property(channel, "placements", [-1, 0, 0, -1])

    window = tk.Tk()
    window.title("Sequencer")
    window.resizable(False, False)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    placement_display = PlacementDisplay(
        window,
        model=model,
        height=500,
        width=500
    )
    placement_display.grid(column=0, row=0, padx=5, pady=5)

    undo_frame = ttk.Frame(window)
    undo_btn = ttk.Button(undo_frame, text="undo", command=lambda: model.uman.undo())
    redo_btn = ttk.Button(undo_frame, text="redo", command=lambda: model.uman.redo())
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    undo_frame.grid(column=1, row=0)

    window.mainloop()

def test_sequencer():
    model = Model()
    pattern = model.new_pattern()
    channel = model.new_channel()
    model.ed.set_property(channel, "placements", [-1, 0, 0, -1] + [-1] * 16)

    model.new_channel()
    model.new_channel()

    window = tk.Tk()
    window.title("Sequencer")
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    sequencer = Sequencer(window, model=model)
    sequencer.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    stuff_frame = ttk.Frame(window)
    undo_btn = ttk.Button(stuff_frame, text="undo", command=lambda: model.uman.undo())
    redo_btn = ttk.Button(stuff_frame, text="redo", command=lambda: model.uman.redo())
    add_channel_btn = ttk.Button(stuff_frame, text="add channel", command=model.new_channel)
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    add_channel_btn.grid(column=0, row=2)
    stuff_frame.grid(column=1, row=0)

    window.mainloop()

if __name__ == "__main__":
    test_sequencer()