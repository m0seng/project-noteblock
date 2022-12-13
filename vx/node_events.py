from abc import ABC, abstractmethod
from node import Node

class NodeListener(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def property_set(self, node: Node, key):
        ...

    @abstractmethod
    def child_added(self, parent: Node, child: Node):
        ...

    @abstractmethod
    def child_removed(self, parent: Node, child: Node):
        ...

class NodeEvents:
    def __init__(self):
        self.listeners: list[NodeListener] = []

    def add_listener(self, listener: NodeListener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener: NodeListener):
        if listener in self.listeners:
            self.listeners.remove(listener)