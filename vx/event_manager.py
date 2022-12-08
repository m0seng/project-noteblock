from action import Action
from node import Node, AddChildAction, SetPropertyAction
from undo_manager import UndoManager

class EventManager:
    def __init__(self):
        self.undo_manager = UndoManager()

    def perform(self, action: Action):
        self.undo_manager.perform(action) # TODO: elaborate

    def node_add_child(self, parent: Node, child: Node):
        if child.parent is not None:
            self.node_remove_child(parent, child)
        next_id = max(parent.children, default=-1) + 1
        next_index = len(parent.child_order)
        self.perform(AddChildAction(
            parent=self,
            child=child,
            id=next_id,
            index=next_index
        ))

    def node_remove_child(self, parent: Node, child: Node):
        if child not in parent.children.values(): return
        child_id = next(k for k, v in parent.children.items() if v == child)
        child_index = parent.child_order.index(child_id)
        self.perform(AddChildAction(
            parent=self,
            child=child,
            id=child_id,
            index=child_index,
            reversed=True
        ))

    def node_set_property(self, node: Node, key, value):
        # NOTE: this sets the property even if it does not already exist
        # useful for testing purposes but maybe not ideal?
        old_value = node.properties.get(key, None)
        self.perform(SetPropertyAction(
            node=self,
            key=key,
            old_value=old_value,
            new_value=value
        ))

    # TODO: handle object CREATION here
    # avoid circular imports !!!