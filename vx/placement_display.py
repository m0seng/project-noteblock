import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from events import EventBus, Listener
from node_editor import NodeEditor
from model import Model

from pattern import Pattern
from pattern_group import PatternGroup
from channel import Channel
from channel_group import ChannelGroup

class PlacementDisplay(Listener, tk.Canvas):
    def __init__(self, parent, *args, model: Model, **kwargs):
        self.model = model

        self.pattern_width: float = 60
        self.pattern_height: float = 60

        self.bg_colour: str = "gray75"
        self.guidebar_colour: str = "gray70"
        self.guideline_colour: str = "gray65"

        super().__init__(
            parent,
            *args,
            scrollregion=(0, 0, 0, 0),
            highlightthickness=0,
            bg=self.bg_colour,
            **kwargs
        )

        self.model.event_bus.add_listener(self)
        self.draw_everything()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_property_set(self, node: Node, key, old_value, new_value):
        if isinstance(node, Pattern) and key == "colour":
            self.draw_everything()
        elif isinstance(node, Channel) and key == "placements":
            self.draw_everything()

    def node_child_added(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.channel_group or parent is self.model.pattern_group:
            self.draw_everything()

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.channel_group or parent is self.model.pattern_group:
            self.draw_everything()

    def draw_everything(self):
        self.configure_canvas()
        self.draw_placements()

    def configure_canvas(self):
        self.delete("all")

        channel_count = self.model.channel_group.children_count()
        # if channel_count == 0:
        #     placement_count = 0
        # else:
        #     first_channel = self.model.channel_group.get_child_at_index(0)
        #     placement_count = len(first_channel.get_property("placements"))
        placement_count = self.model.song_config.get_property("sequence_length")

        canvas_height = channel_count * self.pattern_height
        canvas_width = placement_count * self.pattern_width
        self.configure(scrollregion=(0, 0, canvas_width, canvas_height))

        # guide bars
        for channel_number in range(0, channel_count, 2):
            self.draw_pattern(
                channel=channel_number,
                bar=0,
                length=placement_count,
                fill=self.guidebar_colour,
                outline=""
            )

        # guide lines
        for bar in range(placement_count):
            self.create_line(
                bar * self.pattern_width,
                0,
                bar * self.pattern_width,
                canvas_height,
                fill=self.guideline_colour,
                width=0
            )

    def draw_placements(self):
        for channel_number, channel in enumerate(self.model.channel_group.children_iterator()):
            for bar, pattern_id in enumerate(channel.get_property("placements")):
                if pattern_id == -1: continue # no placement here
                pattern = self.model.pattern_group.get_child_by_id(pattern_id)
                if pattern is None: continue
                pattern_colour = pattern.get_property("colour")
                self.draw_pattern(channel=channel_number, bar=bar, length=1, fill=pattern_colour)

    def draw_pattern(self, channel: int, bar: int, length: int, **kwargs) -> int:
        """Draws a note on the canvas."""
        self.create_rectangle(
            self.pattern_width * bar,
            self.pattern_height * channel,
            self.pattern_width * (bar + length),
            self.pattern_height * (channel + 1),
            **kwargs
        )

    def get_bar_at_coords(self, x: int, y: int) -> tuple[int, int]:
        canvas_x = self.canvasx(x)
        canvas_y = self.canvasy(y)
        bar = int(canvas_x // self.pattern_width)
        channel = int(canvas_y // self.pattern_height)
        return channel, bar