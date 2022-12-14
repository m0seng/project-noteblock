from abc import ABC, abstractmethod
from node import Node
from node_events import NodeEventBus

class Action(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def perform(self):
        ...

    @abstractmethod
    def undo(self):
        ...

class SetPropertyAction(Action):
    def __init__(self, event_bus: NodeEventBus, node: Node, key, old_value, new_value):
        self.event_bus = event_bus
        self.node = node
        self.key = key
        self.old_value = old_value
        self.new_value = new_value

    def perform(self):
        self.node._set_property(self.key, self.new_value)
        self.event_bus.property_set(self.node, self.key, self.old_value, self.new_value)

    def undo(self):
        self.node._set_property(self.key, self.old_value)
        self.event_bus.property_set(self.node, self.key, self.old_value, self.new_value)

class AddChildAction(Action):
    # assumes child does not have another parent
    def __init__(self, event_bus: NodeEventBus, parent: Node, child: Node, id: int, index: int):
        self.event_bus = event_bus
        self.parent = parent
        self.child = child
        self.id = id
        self.index = index

    def perform(self):
        self.parent._add_child(self.child, self.id, self.index)
        self.event_bus.child_added(self.parent, self.child, self.id, self.index)
    
    def undo(self):
        self.parent._remove_child(self.child, self.id, self.index)
        self.event_bus.child_removed(self.parent, self.child, self.id, self.index)

class RemoveChildAction(Action):
    def __init__(self, event_bus: NodeEventBus, parent: Node, child: Node, id: int, index: int):
        self.event_bus = event_bus
        self.parent = parent
        self.child = child
        self.id = id
        self.index = index

    def perform(self):
        self.parent._remove_child(self.child, self.id, self.index)
        self.event_bus.child_removed(self.parent, self.child, self.id, self.index)
    
    def undo(self):
        self.parent._add_child(self.child, self.id, self.index)
        self.event_bus.child_added(self.parent, self.child, self.id, self.index)