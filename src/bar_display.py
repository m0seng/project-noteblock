import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import EventBus, Listener
from node_editor import NodeEditor
from model import Model

class BarDisplay(Listener, tk.Canvas):
    """UI component - displays bar numbers and playback start/loop points above the sequencer."""

    def __init__(self, parent, *args, model: Model, **kwargs):
        self.model = model
        self.selected_bar: int = 0

        self.strip_height: int = 20
        self.bar_width: int = 60

        self.bg_colour: str = "gray75"
        self.guideline_colour: str = "gray50"
        self.selected_bar_colour: str = "red"

        super().__init__(
            parent,
            *args,
            height=self.strip_height,
            scrollregion=(0, 0, 0, 0),
            highlightthickness=0,
            bg=self.bg_colour,
            **kwargs
        )
        self.bind("<ButtonPress-1>", self.select_bar)
        self.bind("<ButtonPress-3>", self.set_loop_start)
        self.bind("<ButtonRelease-3>", self.set_loop_end)

        self.model.event_bus.add_listener(self)
        self.draw_everything()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_property_set(self, node: Node, key, old_value, new_value):
        if node is self.model.song_config:
            if key == "sequence_length":
                self.draw_everything()
            elif key == "loop_start" or key == "loop_end":
                self.draw_loop_markers()

    def bar_selected(self, bar: int):
        self.selected_bar = bar
        self.draw_start_marker()

    def reset_ui(self):
        self.draw_everything()

    def draw_everything(self):
        self.delete("all")
        self.draw_background()
        self.draw_start_marker()
        self.draw_loop_markers()

    def draw_background(self):
        sequence_length = self.model.song_config.get_property("sequence_length")
        self.configure(scrollregion=(0, 0, sequence_length * self.bar_width, 0))
        for bar_number in range(sequence_length):
            self.create_line(
                bar_number * self.bar_width,
                0,
                bar_number * self.bar_width,
                self.strip_height,
                fill=self.guideline_colour,
                width=0
            )
            self.create_text(
                (bar_number * self.bar_width) + 3,
                0,
                text=bar_number,
                anchor="nw",
                fill=self.guideline_colour
            )

    def draw_start_marker(self):
        self.delete("start_marker")
        self.create_polygon(
            (self.selected_bar * self.bar_width) - 5,
            0,
            (self.selected_bar * self.bar_width) + 5,
            0,
            (self.selected_bar * self.bar_width) + 5,
            self.strip_height - 5,
            (self.selected_bar * self.bar_width),
            self.strip_height,
            (self.selected_bar * self.bar_width) - 5,
            self.strip_height - 5,
            fill=self.selected_bar_colour,
            tags="start_marker"
        )

    def draw_loop_markers(self):
        self.delete("loop_marker")
        self.create_rectangle(
            self.model.song_config.get_property("loop_start") * self.bar_width,
            0,
            self.model.song_config.get_property("loop_end") * self.bar_width,
            self.strip_height,
            fill="purple",
            stipple="gray50",
            tags="loop_marker"
        )
        self.tag_raise("start_marker", "loop_marker")

    def select_bar(self, event: tk.Event):
        bar = self.get_bar_at_coords(event.x)
        self.model.event_bus.bar_selected(bar)

    def set_loop_start(self, event: tk.Event):
        bar = self.get_bar_at_coords(event.x)
        self.model.ed.set_property(self.model.song_config, "loop_start", bar)

    def set_loop_end(self, event: tk.Event):
        bar = self.get_bar_at_coords(event.x)
        self.model.ed.set_property(self.model.song_config, "loop_end", bar)

    def get_bar_at_coords(self, x: int) -> int:
        canvas_x = self.canvasx(x)
        bar = int(canvas_x // self.bar_width)
        return bar