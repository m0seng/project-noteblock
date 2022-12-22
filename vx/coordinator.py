import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from undo_manager import UndoManager
from node_events import NodeEventBus, NodeListener
from general_events import GeneralEventBus, GeneralListener
from node_editor import NodeEditor

from pattern import Pattern
from pattern_group import PatternGroup
from channel import Channel
from channel_group import ChannelGroup

from sequencer import Sequencer

class Coordinator:
    def __init__(self):
        self.uman = UndoManager()
        self.node_event_bus = NodeEventBus()
        self.general_event_bus = GeneralEventBus()
        self.ed = NodeEditor(self.uman, self.node_event_bus)

        self.window = tk.Tk()
        self.window.title("PROJECT NOTEBLOCK")
        self.window.resizable(False, False) # Only resize horizontally
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.test_sequencer()
        self.window.mainloop()

    def test_sequencer(self):
        self.pattern_group = PatternGroup()
        self.channel_group = ChannelGroup()

        self.pattern = Pattern()
        self.ed.add_child(self.pattern_group, self.pattern)

        self.channel = Channel(pattern_group=self.pattern_group)
        self.ed.add_child(self.channel_group, self.channel)
        self.ed.set_property(self.channel, "placements", [-1, 0, 0, -1])

        self.sequencer = Sequencer(
            self.window,
            ed=self.ed,
            event_bus=self.node_event_bus,
            pattern_group=self.pattern_group,
            channel_group=self.channel_group,
            height=500,
            width=500
        )
        self.sequencer.grid(column=0, row=0, padx=5, pady=5)

    def add_listener(self, listener):
        if isinstance(listener, NodeListener):
            self.node_event_bus.add_listener(listener)
        if isinstance(listener, GeneralListener):
            self.general_event_bus.add_listener(listener)

    def remove_listener(self, listener):
        if isinstance(listener, NodeListener):
            self.node_event_bus.remove_listener(listener)
        if isinstance(listener, GeneralListener):
            self.general_event_bus.remove_listener(listener)

def main():
    coordinator = Coordinator()

if __name__ == "__main__":
    main()