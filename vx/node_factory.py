from copy import deepcopy
from typing import Type

from node import Node
from pattern import Pattern
from pattern_group import PatternGroup
from channel import Channel
from channel_group import ChannelGroup
# TODO: import Node subclasses here

class NodeFactory:
    node_classes: dict[str, Type[Node]] = {
        "Node": Node,
        "Pattern": Pattern,
        "PatternGroup": PatternGroup,
        "Channel": Channel,
        "ChannelGroup": ChannelGroup,
        # TODO: add entries for Node subclasses here
    }

    def create_node(self, source: dict):
        node_class = self.node_classes.get(source["class"], None)
        if node_class is None: return None
        node = node_class()
        node.properties = deepcopy(source["properties"])
        node.child_order = deepcopy(source["child_order"])
        for k, v in source["children"].items():
            child = self.create_node(v)
            node._add_child(child, id=int(k), index=None)
        return node