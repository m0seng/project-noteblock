import json

from node import Node
from events import EventBus
from undo_manager import UndoManager
from node_editor import NodeEditor
from node_factory import NodeFactory

from song_config import SongConfig
from pattern import Pattern
from pattern_group import PatternGroup
from channel import Channel
from channel_group import ChannelGroup

class Model:
    def __init__(self):
        self.init_components()
        self.init_tree()

    def init_components(self):
        self.uman = UndoManager()
        self.event_bus = EventBus()
        self.ed = NodeEditor(self.uman, self.event_bus)
        self.factory = NodeFactory()

    def init_tree(self):
        self.root = Node()
        self.song_config = SongConfig()
        self.pattern_group = PatternGroup()
        self.channel_group = ChannelGroup()
        self.root._add_child(self.song_config, 0, 0)
        self.root._add_child(self.pattern_group, 1, 1)
        self.root._add_child(self.channel_group, 2, 2)
        self.new_pattern()
        self.new_channel()
        self.event_bus.reset_ui()

    def from_dict(self, source: dict):
        # NOTE: if only it was this simple...
        # self.root = self.factory.create_node(source)
        # self.song_config = self.root.get_child_by_class(SongConfig)
        # self.pattern_group = self.root.get_child_by_class(PatternGroup)
        # self.channel_group = self.root.get_child_by_class(ChannelGroup)

        self.song_config = self.factory.create_node(source["children"]["0"])
        self.pattern_group = self.factory.create_node(source["children"]["1"])
        self.channel_group = self.factory.create_node(source["children"]["2"],
            pattern_group=self.pattern_group)
        self.root = Node()
        self.root._add_child(self.song_config, 0, 0)
        self.root._add_child(self.pattern_group, 1, 1)
        self.root._add_child(self.channel_group, 2, 2)
        self.event_bus.reset_ui() # TODO: does this have to be somewhere else?

    def to_dict(self) -> dict:
        return self.root.to_dict()

    def from_file(self, filename: str):
        with open(filename, "r", encoding="utf-8") as file:
            self.from_dict(json.load(file))

    def to_file(self, filename: str):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file)

    def new_pattern(self) -> Pattern:
        pattern_length = self.song_config.get_property("pattern_length")
        pattern = Pattern(pattern_length=pattern_length)
        self.ed.add_child(self.pattern_group, pattern)
        return pattern

    def new_channel(self) -> Channel:
        sequence_length = self.song_config.get_property("sequence_length")
        channel = Channel(pattern_group=self.pattern_group, sequence_length=sequence_length)
        self.ed.add_child(self.channel_group, channel)
        return channel

    def change_pattern_length(self, new_length: int):
        # TODO: note priority logic?
        self.uman.start_group()
        old_length: int = self.song_config.get_property("pattern_length")
        for pattern in self.pattern_group.children_iterator():
            old_notes = pattern.get_property("notes")
            new_notes = [-1] * new_length
            ratio = new_length / old_length
            for old_tick, note in reversed(enumerate(old_notes)):
                if note != -1:
                    new_tick = int(old_tick * ratio)
                    new_notes[new_tick] = note
            self.ed.set_property(pattern, "notes", new_notes)
        self.ed.set_property(self.song_config, "pattern_length", new_length)
        self.uman.end_group()

    def change_sequence_length(self, new_length: int):
        self.uman.start_group()
        old_length = self.song_config.get_property("sequence_length")
        for channel in self.channel_group.children_iterator():
            old_placements = channel.get_property("placements")
            if new_length > old_length:
                difference = new_length - old_length
                new_placements = old_placements + ([-1] * difference)
            else:
                new_placements = old_placements[:new_length]
            self.ed.set_property(channel, "placements", new_placements)
        self.ed.set_property(self.song_config, "sequence_length", new_length)
        self.uman.end_group()

    def remove_pattern(self, pattern: Pattern):
        self.uman.start_group()
        pattern_id = self.pattern_group.get_id_of_child(pattern)
        if pattern_id is None: return
        for channel in self.channel_group.children_iterator():
            old_placements = channel.get_property("placements")
            new_placements = [id for id in old_placements if id != pattern_id]
            self.ed.set_property(channel, "placements", new_placements)
        self.ed.remove_child(self.pattern_group, pattern)
        self.uman.end_group()