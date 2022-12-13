from abc import ABC, abstractmethod
from node import Node
from node_contexts import AddChildContext

class NodeListener(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def property_set(self, node: Node, key, old_value, new_value):
        ...

    @abstractmethod
    def child_added(self, parent: Node, child: Node, id: int, index: int):
        ...

    @abstractmethod
    def child_removed(self, parent: Node, child: Node, id: int, index: int):
        ...

class NodeEventBus:
    def __init__(self):
        self.listeners: list[NodeListener] = []

    def add_listener(self, listener: NodeListener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener: NodeListener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def property_set(self, node: Node, key, old_value, new_value):
        for listener in self.listeners:
            listener.property_set(node, key, old_value, new_value)

    def child_added(self, parent: Node, child: Node, id: int, index: int):
        for listener in self.listeners:
            listener.child_added(parent, child, id, index)

    def child_removed(self, parent: Node, child: Node, id: int, index: int):
        for listener in self.listeners:
            listener.child_removed(parent, child, id, index)