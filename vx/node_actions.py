from abc import ABC, abstractmethod
from node import Node
from events import EventBus

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
    def __init__(self, event_bus: EventBus, node: Node, key, old_value, new_value):
        self.event_bus = event_bus
        self.node = node
        self.key = key
        self.old_value = old_value
        self.new_value = new_value

    def perform(self):
        self.node._set_property(self.key, self.new_value)
        self.event_bus.node_property_set(self.node, self.key, self.old_value, self.new_value)

    def undo(self):
        self.node._set_property(self.key, self.old_value)
        self.event_bus.node_property_set(self.node, self.key, self.new_value, self.old_value)

class AddChildAction(Action):
    # assumes child does not have another parent
    def __init__(self, event_bus: EventBus, parent: Node, child: Node, id: int, index: int):
        self.event_bus = event_bus
        self.parent = parent
        self.child = child
        self.id = id
        self.index = index

    def perform(self):
        self.parent._add_child(self.child, self.id, self.index)
        self.event_bus.node_child_added(self.parent, self.child, self.id, self.index)
    
    def undo(self):
        self.parent._remove_child(self.child, self.id, self.index)
        self.event_bus.node_child_removed(self.parent, self.child, self.id, self.index)

class RemoveChildAction(Action):
    def __init__(self, event_bus: EventBus, parent: Node, child: Node, id: int, index: int):
        self.event_bus = event_bus
        self.parent = parent
        self.child = child
        self.id = id
        self.index = index

    def perform(self):
        self.parent._remove_child(self.child, self.id, self.index)
        self.event_bus.node_child_removed(self.parent, self.child, self.id, self.index)
    
    def undo(self):
        self.parent._add_child(self.child, self.id, self.index)
        self.event_bus.node_child_added(self.parent, self.child, self.id, self.index)

class MoveChildAction(Action):
    def __init__(self, event_bus: EventBus, parent: Node, old_index: int, new_index: int):
        self.event_bus = event_bus
        self.parent = parent
        self.old_index = old_index
        self.new_index = new_index

    def perform(self):
        self.parent._move_child(self.old_index, self.new_index)
        self.event_bus.node_child_moved(self.parent, self.old_index, self.new_index)
    
    def undo(self):
        self.parent._move_child(self.new_index, self.old_index)
        self.event_bus.node_child_moved(self.parent, self.new_index, self.old_index)