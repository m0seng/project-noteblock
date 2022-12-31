from abc import ABC
from node import Node

class Listener(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def node_property_set(self, node: Node, key, old_value, new_value):
        ...

    def node_child_added(self, parent: Node, child: Node, id: int, index: int):
        ...

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        ...

    def node_child_moved(self, parent: Node, old_index: int, new_index: int):
        ...

    def node_selected(self, node: Node):
        ...

    def bar_selected(self, bar: int):
        ...

    def bar_playing(self, bar: int):
        ...

    def reset_ui(self):
        # Used when a project is loaded from file
        # All links to old Nodes need to be broken
        ...

class EventBus:
    def __init__(self):
        self.listeners: list[Listener] = []

    def add_listener(self, listener: Listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener: Listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def clear_listeners(self):
        self.listeners = []

    def node_property_set(self, node: Node, key, old_value, new_value):
        for listener in self.listeners:
            listener.node_property_set(node, key, old_value, new_value)

    def node_child_added(self, parent: Node, child: Node, id: int, index: int):
        for listener in self.listeners:
            listener.node_child_added(parent, child, id, index)

    def node_child_removed(self, parent: Node, child: Node, id: int, index: int):
        for listener in self.listeners:
            listener.node_child_removed(parent, child, id, index)

    def node_child_moved(self, parent: Node, old_index: int, new_index: int):
        for listener in self.listeners:
            listener.node_child_moved(parent, old_index, new_index)

    def node_selected(self, node: Node):
        print(f"node {node} selected") # TODO: remove this
        for listener in self.listeners:
            listener.node_selected(node)

    def bar_selected(self, bar: int):
        for listener in self.listeners:
            listener.bar_selected(bar)

    def bar_playing(self, bar: int):
        for listener in self.listeners:
            listener.bar_playing(bar)

    def reset_ui(self):
        for listener in self.listeners:
            listener.reset_ui()