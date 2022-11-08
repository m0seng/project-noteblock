# GOALS OF THE VALUE TREE:
# - flexible, nestable data structure
# - serialization to and from a JSON-compatible dictionary
# - support for an undo manager
# - listener notification system

# see https://docs.juce.com/master/tutorial_value_tree.html for the basis of this system

from undo_manager import UndoManager
from undoable_action import UndoableAction
from value_tree_listener import ValueTreeListener

class ValueTree:
    def __init__(self):
        self.parent: ValueTree | None = None
        self.properties: dict = {}
        self.children: list[ValueTree] = []
        self.listeners: list[ValueTreeListener] = []

    def add_listener(self, listener: ValueTreeListener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener: ValueTreeListener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def set_property(self, key: str, value, uman: UndoManager | None):
        if uman is None:
            self.properties[key] = value
            for listener in self.listeners: listener.vt_property_changed(self, key)
        else:
            if key in self.properties:
                uman.perform(SetPropertyAction(self, key, new_val=value, old_val=self.properties[key]))
            else:
                uman.perform(SetPropertyAction(self, key, new_val=value, is_adding=True))

    def remove_property(self, key: str, uman: UndoManager | None):
        if uman is None:
            del self.properties[key]
            for listener in self.listeners: listener.vt_property_changed(self, key)
        else:
            if key in self.properties:
                uman.perform(SetPropertyAction(self, key, old_val=self.properties[key], is_deleting=True))

    def add_child(self, child: "ValueTree", index: int, uman: UndoManager | None):
        if (child.parent is not self) and (child is not self) and (self.parent is not child):
            if child.parent is not None:
                child.parent.remove_child(child.parent.children.index(child), uman)
            if uman is None:
                self.children.insert(index, child)
                child.parent = self
                for listener in self.listeners: listener.vt_child_added(self, child)
                for listener in child.listeners: listener.vt_parent_changed(child)
            else:
                uman.perform(AddOrRemoveChildAction(self, child, index))

    def remove_child(self, index: int, uman: UndoManager | None):
        try:
            child = self.children[index]
        except IndexError:
            return
        if uman is None:
            del self.children[index]
            child.parent = None
            for listener in self.listeners: listener.vt_child_removed(self, child, index)
            for listener in child.listeners: listener.vt_parent_changed(child)
        else:
            uman.perform(AddOrRemoveChildAction(self, child, index, is_deleting=True))

    def move_child(self, old_index: int, new_index: int, uman: UndoManager | None):
        if old_index != new_index and 0 <= old_index < len(self.children) and 0 <= new_index < len(self.children):
            if uman is None:
                child = self.children.pop(old_index)
                self.children.insert(new_index, child)
                for listener in self.listeners: listener.vt_child_order_changed(self, old_index, new_index)
            else:
                uman.perform(MoveChildAction(self, old_index, new_index))
    
    def to_dict(self) -> dict:
        output = {}
        output.update(self.properties)
        child_list = [child.to_dict() for child in self.children]
        output["children"] = child_list
        output["type"] = self.__class__.__name__ # use a class mapping here?
        return output

    @classmethod
    def from_dict(cls, source: dict, class_mapping: dict):
        obj = cls()
        for k, v in source.items():
            if k == "children":
                for child_dict in v:
                    child_type = class_mapping.get(child_dict["type"], ValueTree)
                    obj.children.append(child_type.from_dict(child_dict, class_mapping))
            elif k == "type":
                pass
            else:
                obj.properties[k] = v


class SetPropertyAction(UndoableAction):
    def __init__(self, tree: ValueTree, key: str, new_val = None, old_val = None, is_adding: bool = False, is_deleting: bool = False):
        self.tree = tree
        self.key = key
        self.new_val = new_val
        self.old_val = old_val
        self.is_adding = is_adding
        self.is_deleting = is_deleting

    def perform(self):
        if self.is_deleting:
            self.tree.remove_property(self.key, None)
        else:
            self.tree.set_property(self.key, self.new_val, None)

    def undo(self):
        if self.is_adding:
            self.tree.remove_property(self.key, None)
        else:
            self.tree.set_property(self.key, self.old_val, None)

class AddOrRemoveChildAction(UndoableAction):
    def __init__(self, tree: ValueTree, child: ValueTree, index: int, is_deleting: bool = False):
        self.tree = tree
        self.child = child
        self.index = index
        self.is_deleting = is_deleting

    def perform(self):
        if self.is_deleting:
            self.tree.remove_child(self.index, None)
        else:
            self.tree.add_child(self.child, self.index, None)

    def undo(self):
        if self.is_deleting:
            self.tree.add_child(self.child, self.index, None)
        else:
            self.tree.remove_child(self.index, None)

class MoveChildAction(UndoableAction):
    def __init__(self, tree: ValueTree, old_index: int, new_index: int):
        self.tree = tree
        self.old_index = old_index
        self.new_index = new_index

    def perform(self):
        self.tree.move_child(self.old_index, self.new_index, None)

    def undo(self):
        self.tree.move_child(self.new_index, self.old_index, None)