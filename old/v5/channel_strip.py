import tkinter as tk
import tkinter.ttk as ttk

from pattern import Pattern
from pattern_group import PatternGroup
from channel import Channel
from channel_group import ChannelGroup
from savable_frame import SavableFrame

class ChannelStrip(SavableFrame):
    def __init__(
            self,
            parent,
            model: Channel,
            channel_group: ChannelGroup,
            pattern_group: PatternGroup,
            scrollbar: ttk.Scrollbar,
            *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.columnconfigure(0, weight=1)

        self.channel_group: ChannelGroup = channel_group
        self.pattern_group: PatternGroup = pattern_group
        self.model: Channel = model
        self.scrollbar: ttk.Scrollbar = scrollbar

        self.tick_width: float = 5
        self.strip_height: int = 100
        self.snap: int = 4
        
        # colour constants
        # TODO: derive these from global theme???
        self.bg_colour: str = "gray75"
        self.guideline_colour: str = "gray65"

        self.pattern_rects: list[int] = []

    def init_canvas(self):
        self.canvas = tk.Canvas(
            self,
            height=self.strip_height,
            scrollregion=(0, 0, self.target_canvas_length(), self.strip_height),
            highlightthickness=0,
            bg=self.bg_colour
        )
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.canvas.grid(column=0, row=0, sticky="nsew", padx=5, pady=5)

    def zoom(self, zoom_factor: float):
        left_fraction = self.canvas.xview()[0]
        self.tick_width *= zoom_factor
        self.canvas.configure(scrollregion=(0, 0, self.target_canvas_length(), self.strip_height))
        self.canvas.xview_moveto(left_fraction)

    def draw_everything(self):
        self.canvas.delete("all")
        self.draw_guide_lines()
        self.draw_placements()

    def draw_guide_lines(self):
        for i in range(0, self.channel_group.song_length(), self.snap):
            self.canvas.create_line(
                i * self.tick_width,
                0,
                i * self.tick_width,
                self.strip_height,
                fill=self.guideline_colour,
                width=0
            )

    def draw_placements(self):
        self.pattern_rects = []
        for pat_id, start_tick in self.model.placements:
            pattern = self.pattern_group.data[pat_id]
            rect_id = self.draw_pattern_rect(
                start_tick,
                start_tick + pattern.length,
                pattern.colour
            )
            self.pattern_rects.append(rect_id)

    def draw_pattern_rect(self, start: int, end: int, colour: str, **kwargs) -> int:
        return self.canvas.create_rectangle(
            start * self.tick_width,
            0,
            end * self.tick_width,
            self.strip_height,
            fill=colour,
            **kwargs
        )

    def target_canvas_length(self):
        return self.tick_width * self.channel_group.song_length()