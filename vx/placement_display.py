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
    """
    UI component - the main renderer of the sequencer.
    Shows pattern placements on their respective channels.
    """

    def __init__(self, parent, *args, model: Model, **kwargs):
        self.model = model
        self.selected_bar: int = 0
        self.playing_bar: int = -1

        # actual config
        self.pattern_width: float = 60
        self.pattern_height: float = 60

        # internal variables that get recalculated
        self.channel_count: int = 0
        self.placement_count: int = 0
        self.canvas_height: float = 0
        self.canvas_width: float = 0

        self.bg_colour: str = "gray75"
        self.guidebar_colour: str = "gray70"
        self.guideline_colour: str = "gray65"
        self.selected_bar_colour: str = "red"
        self.playing_bar_colour: str = "green"

        super().__init__(
            parent,
            *args,
            scrollregion=(0, 0, 0, 0),
            highlightthickness=0,
            bg=self.bg_colour,
            **kwargs
        )
        self.bind("<ButtonPress-1>", self.select_things)
        self.bind("<ButtonPress-3>", self.delete_placement)

        self.model.event_bus.add_listener(self)
        self.draw_everything()

    def destroy(self, *args, **kwargs):
        self.model.event_bus.remove_listener(self)
        super().destroy(*args, **kwargs)

    def node_property_set(self, node: Node, key, old_value, new_value):
        if isinstance(node, Pattern) and key == "colour":
            self.draw_placements()
        elif isinstance(node, Channel) and key == "placements":
            self.draw_placements()
        elif node is self.model.song_config and key == "sequence_length":
            self.draw_everything()

    def node_child_added(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.channel_group:
            self.draw_everything()

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.model.channel_group:
            self.draw_everything()

    def node_child_moved(self, parent: Node, old_index: int, new_index: int):
        if parent is self.model.channel_group:
            self.draw_everything()

    def bar_selected(self, bar: int):
        self.selected_bar = bar
        self.draw_selected_bar_line()

    def bar_playing(self, bar: int):
        self.playing_bar = bar
        self.draw_playing_bar_line()

    def reset_ui(self):
        self.draw_everything()

    # NOTE: apparently all of the following are needed to use Tkinter's drag and drop library
    # maybe I should have written my own...

    def dnd_accept(self, source, event):
        return self

    def dnd_enter(self, source, event):
        ...

    def dnd_motion(self, source, event):
        ...

    def dnd_leave(self, source, event):
        ...

    def dnd_commit(self, source, event: tk.Event):
        pattern = getattr(source, "pattern", None)
        if isinstance(pattern, Pattern):
            pattern_id = self.model.pattern_group.get_id_of_child(pattern)
            bar, channel, _ = self.get_everything_at_coords(
                event.x_root - self.winfo_rootx(),
                event.y_root - self.winfo_rooty()
            )
            if channel is not None:
                placements_copy = channel.get_property("placements")[:]
                placements_copy[bar] = pattern_id
                self.model.ed.set_property(channel, "placements", placements_copy)

    def draw_everything(self):
        self.recalculate_dimensions()
        self.configure_canvas()
        self.draw_placements()
        self.draw_selected_bar_line()
        self.draw_playing_bar_line()

    def recalculate_dimensions(self):
        self.channel_count = self.model.channel_group.children_count()
        self.placement_count = self.model.song_config.get_property("sequence_length")
        self.canvas_height = self.channel_count * self.pattern_height
        self.canvas_width = self.placement_count * self.pattern_width

    def configure_canvas(self):
        self.delete("all")
        self.configure(scrollregion=(0, 0, self.canvas_width, self.canvas_height))

        # guide bars
        for channel_number in range(0, self.channel_count, 2):
            self.draw_pattern(
                channel=channel_number,
                bar=0,
                length=self.placement_count,
                fill=self.guidebar_colour,
                outline=""
            )

        # guide lines
        for bar in range(self.placement_count):
            self.create_line(
                bar * self.pattern_width,
                0,
                bar * self.pattern_width,
                self.canvas_height,
                fill=self.guideline_colour,
                width=0
            )

    def draw_selected_bar_line(self):
        # selected bar line
        self.delete("selected_bar_line")
        if 0 <= self.selected_bar < self.placement_count:
            self.create_line(
                self.selected_bar * self.pattern_width,
                0,
                self.selected_bar * self.pattern_width,
                self.canvas_height,
                fill=self.selected_bar_colour,
                width=0,
                tags="selected_bar_line"
            )

    def draw_playing_bar_line(self):
        # playing bar line
        self.delete("playing_bar_line")
        if 0 <= self.playing_bar < self.placement_count:
            self.create_line(
                self.playing_bar * self.pattern_width,
                0,
                self.playing_bar * self.pattern_width,
                self.canvas_height,
                fill=self.playing_bar_colour,
                width=0,
                tags="playing_bar_line"
            )

    def draw_placements(self):
        self.delete("placements")
        for channel_number, channel in enumerate(self.model.channel_group.children_iterator()):
            for bar, pattern_id in enumerate(channel.get_property("placements")):
                if pattern_id == -1: continue # no placement here
                pattern = self.model.pattern_group.get_child_by_id(pattern_id)
                if pattern is None: continue
                pattern_colour = pattern.get_property("colour")
                self.draw_pattern(channel=channel_number, bar=bar, length=1, fill=pattern_colour, tags="placements")
        self.tag_raise("selected_bar_line")
        self.tag_raise("playing_bar_line")

    def draw_pattern(self, channel: int, bar: int, length: int, **kwargs) -> int:
        """Draws a note on the canvas."""
        self.create_rectangle(
            self.pattern_width * bar,
            self.pattern_height * channel,
            self.pattern_width * (bar + length),
            self.pattern_height * (channel + 1),
            **kwargs
        )

    def select_things(self, event: tk.Event):
        bar, channel, pattern = self.get_everything_at_coords(event.x, event.y)
        if channel is not None: self.model.event_bus.node_selected(channel)
        if pattern is not None: self.model.event_bus.node_selected(pattern)

    def delete_placement(self, event: tk.Event):
        bar, channel, pattern = self.get_everything_at_coords(event.x, event.y)
        if pattern is not None:
            placements_copy = channel.get_property("placements")[:]
            placements_copy[bar] = -1
            self.model.ed.set_property(channel, "placements", placements_copy)

    def get_bar_at_coords(self, x: int, y: int) -> tuple[int, int]:
        canvas_x = self.canvasx(x)
        canvas_y = self.canvasy(y)
        bar = int(canvas_x // self.pattern_width)
        channel_index = int(canvas_y // self.pattern_height)
        return channel_index, bar

    def get_everything_at_coords(self, x: int, y: int):
        channel_index, bar = self.get_bar_at_coords(x, y)
        channel = self.model.channel_group.get_child_at_index(channel_index)
        if channel is None: return (bar, channel, None)
        pattern_id = channel.get_property("placements")[bar]
        pattern = self.model.pattern_group.get_child_by_id(pattern_id)
        return (bar, channel, pattern)