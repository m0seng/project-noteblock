import tkinter as tk
import tkinter.ttk as ttk

from node import Node
from node_events import NodeListener
from pattern import Pattern
from pattern_group import PatternGroup

class PianoRoll(NodeListener):
    def __init__(self, pattern_group: PatternGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pattern_group = pattern_group
        self.pattern: Pattern | None = None

    def attach_pattern(self, pattern: Pattern):
        self.pattern = pattern

    def node_property_set(self, node: Node, key, old_value, new_value):
        if node is self.pattern: self.update()

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        if parent is self.pattern_group and child is self.pattern:
            self.pattern = None
            self.update()

    def update(self):
        ...