from collections import deque
from dataclasses import dataclass
from action import Action
from node import Node
from node_events import NodeEventBus

class UndoManager:
    def __init__(self, past_len: int = 10, future_len: int = 10):
        self.past: deque[Action] = deque(maxlen=past_len)
        self.future: deque[Action] = deque(maxlen=future_len)

    def perform(self, new_action: Action):
        new_action.perform()
        self.past.append(new_action)
        self.future.clear()

    def can_undo(self):
        return len(self.past) > 0

    def undo(self):
        if self.can_undo():
            action = self.past.pop()
            action.undo()
            self.future.append(action)

    def can_redo(self):
        return len(self.future) > 0

    def redo(self):
        if self.can_redo():
            action = self.future.pop()
            action.perform()
            self.past.append(action)

@dataclass
class AddChildContext:
    parent: Node
    child: Node
    id: int
    index: int
    reversed: bool = False

class AddChildAction(Action):
    # assumes child does not have another parent
    def __init__(
            self,
            event_bus: NodeEventBus,
            parent: Node,
            child: Node,
            id: int,
            index: int,
            reversed: bool = False
    ):
        self.event_bus = event_bus
        self.parent = parent
        self.child = child
        self.id = id
        self.index = index
        self.reversed = reversed

    def perform(self):
        if self.reversed:
            self._remove()
        else:
            self._add()
    
    def undo(self):
        if self.reversed:
            self._add()
        else:
            self._remove()
    
    def _add(self):
        self.parent._add_child(self.child, self.id, self.index)
        self.event_bus.child_added(self.parent, self.child, self.id, self.index)
    
    def _remove(self):
        self.parent._remove_child(self.child, self.id, self.index)
        self.event_bus.child_removed(self.parent, self.child, self.id, self.index)

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
        self.event_bus.property_set(self.node, self.key, self.new_value, self.old_value)