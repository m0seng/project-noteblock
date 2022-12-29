import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import Listener
from model import Model

from channel_header_canvas import ChannelHeaderCanvas
from placement_display import PlacementDisplay

class Sequencer(ttk.Frame):
    def __init__(self, parent, *args, model: Model, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.model = model

        self.placement_display = PlacementDisplay(self, model=self.model)
        self.channel_header_canvas = ChannelHeaderCanvas(self, model=self.model)

        self.horizontal_scroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.placement_display.configure(xscrollcommand=self.horizontal_scroll.set)
        self.horizontal_scroll["command"] = self.placement_display.xview

        def yview_both_canvases(*args):
            self.placement_display.yview(*args)
            self.channel_header_canvas.yview(*args)

        self.vertical_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.placement_display.configure(yscrollcommand=self.vertical_scroll.set)
        self.vertical_scroll["command"] = yview_both_canvases

        self.placement_display.grid(column=0, row=0, sticky="nsew")
        self.channel_header_canvas.grid(column=1, row=0, sticky="ns")
        self.horizontal_scroll.grid(column=0, row=1, sticky="ew")
        self.vertical_scroll.grid(column=2, row=0, sticky="ns")