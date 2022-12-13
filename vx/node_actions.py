from abc import ABC, abstractmethod
from node import Node
from node_contexts import AddChildContext, RemoveChildContext, SetPropertyContext
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
    def __init__(self, event_bus: NodeEventBus, ctx: SetPropertyContext):
        self.event_bus = event_bus
        self.ctx = ctx
        self.reversed_ctx = SetPropertyContext(
            self.ctx.node,
            self.ctx.key,
            self.ctx.new_value,
            self.ctx.old_value
        )

    def perform(self):
        self.ctx.node._set_property(self.ctx.key, self.ctx.new_value)
        self.event_bus.property_set(self.ctx)

    def undo(self):
        self.ctx.node._set_property(self.ctx.key, self.ctx.old_value)
        self.event_bus.property_set(self.reversed_ctx)