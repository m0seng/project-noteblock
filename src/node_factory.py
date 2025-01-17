from copy import deepcopy
from typing import Type

from node import Node
from song_config import SongConfig
from pattern import Pattern
from pattern_group import PatternGroup
from channel import Channel
from channel_group import ChannelGroup

from effect_dummy import EffectDummy
from effect_delay import EffectDelay
# TODO: import Node subclasses here

class NodeFactory:
    """
    Creates a song object from its class name and attributes.
    Used to reproduce a song object from a dictionary.
    """

    node_classes: dict[str, Type[Node]] = {
        "Node": Node,
        "SongConfig": SongConfig,
        "Pattern": Pattern,
        "PatternGroup": PatternGroup,
        "Channel": Channel,
        "ChannelGroup": ChannelGroup,
        "EffectDummy": EffectDummy,
        "EffectDelay": EffectDelay,
        # TODO: add entries for Node subclasses here
    }

    def create_node(self, source: dict, **kwargs):
        node_class = self.node_classes.get(source["class"], None)
        if node_class is None: return None
        node = node_class(**kwargs)
        node.properties = deepcopy(source["properties"])
        node.child_order = deepcopy(source["child_order"])
        for k, v in source["children"].items():
            child = self.create_node(v, **kwargs)
            node._add_child(child, id=int(k), index=None)
        return node