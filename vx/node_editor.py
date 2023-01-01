from node import Node
from events import EventBus
from node_actions import AddChildAction, RemoveChildAction, MoveChildAction, SetPropertyAction
from undo_manager import UndoManager

# This is where I stick methods to make editing nodes MUCH easier
# passing an undo manager for now but it might make its own
# also partially facades undo manager, for example when making action groups

class NodeEditor:
    def __init__(self, uman: UndoManager, event_bus: EventBus):
        self.uman = uman
        self.event_bus = event_bus

    def set_property(self, node: Node, key, value):
        old_value = node.get_property(key)
        self.uman.perform(SetPropertyAction(
            self.event_bus,
            node,
            key,
            old_value,
            value
        ))
    
    def toggle_bool(self, node: Node, key):
        old_value = node.get_property(key)
        if not isinstance(old_value, bool):
            return
        new_value = False if old_value else True
        self.uman.perform(SetPropertyAction(
            self.event_bus,
            node,
            key,
            old_value,
            new_value
        ))

    def remove_child(self, parent: Node, child: Node):
        if child.parent is not parent: return
        child_id = parent.get_id_of_child(child)
        child_index = parent.get_index_of_child(child)
        if child_id is None or child_index is None: return
        self.uman.perform(RemoveChildAction(
            self.event_bus,
            parent,
            child,
            child_id,
            child_index
        ))

    def remove_child_with_id(self, parent: Node, child_id: int):
        child = parent.get_child_by_id(child_id)
        child_index = parent.get_index_of_child(child)
        if child is None or child_index is None: return
        self.uman.perform(RemoveChildAction(
            self.event_bus,
            parent,
            child,
            child_id,
            child_index
        ))

    def remove_child_at_index(self, parent: Node, child_index: int):
        child = parent.get_child_at_index(child_index)
        child_id = parent.get_id_of_child(child)
        if child is None or child_id is None: return
        self.uman.perform(RemoveChildAction(
            self.event_bus,
            parent,
            child,
            child_id,
            child_index
        ))

    def add_child(self, parent: Node, child: Node):
        if child.parent is not None: self.remove_child(parent, child)
        child_id = parent.next_available_id()
        child_index = len(parent.child_order)
        self.uman.perform(AddChildAction(
            self.event_bus,
            parent,
            child,
            child_id,
            child_index
        ))

    def add_child_with_id(self, parent: Node, child: Node, child_id: int):
        if child_id in parent.children.keys(): return
        if child.parent is not None: self.remove_child(parent, child)
        child_index = len(parent.child_order)
        self.uman.perform(AddChildAction(
            self.event_bus,
            parent,
            child,
            child_id,
            child_index
        ))

    def add_child_at_index(self, parent: Node, child: Node, child_index: int):
        if child.parent is not None: self.remove_child(parent, child)
        child_id = parent.next_available_id()
        self.uman.perform(AddChildAction(
            self.event_bus,
            parent,
            child,
            child_id,
            child_index
        ))

    def move_child(self, parent: Node, old_index: int, new_index: int):
        children_count = parent.children_count()
        if 0 <= old_index < children_count and 0 <= new_index < children_count:
            self.uman.perform(MoveChildAction(
                self.event_bus,
                parent,
                old_index,
                new_index
            ))