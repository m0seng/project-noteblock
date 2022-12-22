from abc import ABC, abstractmethod
from node import Node

class GeneralListener(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def node_selected(self, node: Node):
        ...

class GeneralEventBus:
    def __init__(self):
        self.listeners: list[GeneralListener] = []

    def add_listener(self, listener: GeneralListener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener: GeneralListener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def node_selected(self, node: Node):
        for listener in self.listeners:
            listener.node_selected(node)