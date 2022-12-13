from collections import deque
from action import Action
from node import Node
from node_contexts import AddChildContext, RemoveChildContext
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

class AddChildAction(Action):
    # assumes child does not have another parent
    def __init__(self, event_bus: NodeEventBus, ctx: AddChildContext):
        self.event_bus = event_bus
        self.ctx = ctx

    def perform(self):
        self.ctx.parent._add_child(self.ctx.child, self.ctx.id, self.ctx.index)
        self.event_bus.child_added(self.ctx)
    
    def undo(self):
        self.ctx.parent._remove_child(self.ctx.child, self.ctx.id, self.ctx.index)
        self.event_bus.child_removed(self.ctx)

class RemoveChildAction(Action):
    # assumes child does not have another parent
    def __init__(self, event_bus: NodeEventBus, ctx: RemoveChildContext):
        self.event_bus = event_bus
        self.ctx = ctx

    def perform(self):
        self.ctx.parent._remove_child(self.ctx.child, self.ctx.id, self.ctx.index)
        self.event_bus.child_removed(self.ctx)
    
    def undo(self):
        self.ctx.parent._add_child(self.ctx.child, self.ctx.id, self.ctx.index)
        self.event_bus.child_added(self.ctx)

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