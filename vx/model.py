from node import Node
from events import EventBus
from undo_manager import UndoManager
from node_editor import NodeEditor
from node_factory import NodeFactory

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
        self.pattern_group = PatternGroup()
        self.channel_group = ChannelGroup()
        self.root._add_child(self.pattern_group, 0, 0)
        self.root._add_child(self.channel_group, 1, 1)

    def from_dict(self, source: dict):
        self.root = self.factory.create_node(source)
        self.pattern_group = self.root.get_child_by_class(PatternGroup)
        self.channel_group = self.root.get_child_by_class(ChannelGroup)

    def to_dict(self) -> dict:
        return self.root.to_dict()

    def new_pattern(self) -> Pattern:
        pattern = Pattern()
        self.ed.add_child(self.pattern_group, pattern)
        return pattern

    def new_channel(self) -> Channel:
        channel = Channel()
        self.ed.add_child(self.channel_group, channel)
        return channel