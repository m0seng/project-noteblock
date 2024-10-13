# GOALS OF THE VALUE TREE:
# - flexible, nestable data structure
# - serialization to and from a JSON-compatible dictionary
# - support for an undo manager
# - listener notification system

# see https://docs.juce.com/master/tutorial_value_tree.html for the basis of this system

# magic methods are not used as they create conflicts with state/properties
# implement in subclasses where appropriate
# TODO: still make copies in dict methods?

from .undo_manager import UndoManager
from .undoable_action import UndoableAction
from .value_tree_listener import ValueTreeListener

class ValueTree:
    def __init__(self, uman: UndoManager):
        self.parent: ValueTree | None = None
        self.properties: dict = {}
        self.children: list[ValueTree] = []
        self.listeners: list[ValueTreeListener] = []
        self.uman = uman

    # def __getattr__(self, name):
    #     if name in self.properties:
    #         return self.get_property(name)

    # def __setattr__(self, name, value):
    #     if name in self.properties:
    #         self.set_property(name, value, self.uman)
    #     else:
    #         super().__setattr__(name, value)

    # def __delattr__(self, name):
    #     if name in self.properties:
    #         self.remove_property(name, self.uman)
    #     else:
    #         super().__delattr__(name)

    def add_listener(self, listener: ValueTreeListener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener: ValueTreeListener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def get_property(self, key: str):
        return self.properties[key]

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

    def get_child(self, index: int):
        return self.children[index]

    def get_child_of_type(self, t: type):
        for child in self.children:
            if isinstance(child, t):
                return child

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
        output["properties"] = self.properties
        output["children"] = [child.to_dict() for child in self.children]
        output["type"] = self.__class__.__name__ # use a class mapping here?
        return output

    @classmethod
    def from_dict(cls, source: dict, class_mapping: dict):
        obj = cls()
        obj.properties = source["properties"]
        for child_dict in source["children"]:
            child_class = class_mapping.get(child_dict["type"], ValueTree)
            obj.children.append(child_class.from_dict(child_dict, class_mapping))
        return obj


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
