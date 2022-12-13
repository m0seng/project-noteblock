from abc import ABC, abstractmethod
from node import Node
from node_contexts import AddChildContext, RemoveChildContext, SetPropertyContext

class NodeListener(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def property_set(self, ctx: SetPropertyContext):
        ...

    @abstractmethod
    def child_added(self, ctx: AddChildContext):
        ...

    @abstractmethod
    def child_removed(self, ctx: RemoveChildContext):
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

    def property_set(self, ctx: SetPropertyContext):
        for listener in self.listeners:
            listener.property_set(ctx)

    def child_added(self, ctx: AddChildContext):
        for listener in self.listeners:
            listener.child_added(ctx)

    def child_removed(self, ctx: RemoveChildContext):
        for listener in self.listeners:
            listener.child_removed(ctx)