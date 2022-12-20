import tkinter as tk
import tkinter.ttk as ttk

from node_events import NodeEventBus
from undo_manager import UndoManager
from node_editor import NodeEditor

from pattern_group import PatternGroup
from channel import Channel
from channel_header import ChannelHeader

def main():
    uman = UndoManager()
    event_bus = NodeEventBus()
    ed = NodeEditor(uman, event_bus)

    pattern_group = PatternGroup()
    channel = Channel(pattern_group=pattern_group)

    window = tk.Tk()
    window.title("Channel Header")
    window.resizable(False, False)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    header = ChannelHeader(window, channel, ed, event_bus)
    header.grid(column=0, row=0)

    undo_frame = ttk.Frame(window)
    undo_btn = ttk.Button(undo_frame, text="undo", command=lambda: uman.undo())
    redo_btn = ttk.Button(undo_frame, text="redo", command=lambda: uman.redo())
    undo_btn.grid(column=0, row=0)
    redo_btn.grid(column=0, row=1)
    undo_frame.grid(column=1, row=0)

    window.mainloop()

if __name__ == "__main__":
    main()