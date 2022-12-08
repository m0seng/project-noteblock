from action import Action

# TODO: more specific child manipulation methods

class Node:
    '''
    A simplified adaptation of the ValueTree concept from JUCE.
    
    Many features have been omitted as I do not need them.

    No editing methods are found here - they are all in the event manager
    '''
    def __init__(self):
        self.parent: Node | None = None
        self.properties = {}
        self.children: dict[int, Node] = {}
        self.child_order: list[int] = []
    
    def get_property(self, key):
        return self.properties[key]

    def get_child_by_id(self, id: int):
        return self.children[id]

    def get_child_by_index(self, index: int):
        return self.get_child_by_id(self.child_order[index])

class AddChildAction(Action):
    # assumes child does not have another parent
    def __init__(self, parent: Node, child: Node, id: int, index: int, reversed: bool = False):
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
        self.parent.children[self.id] = self.child
        self.parent.child_order.insert(self.index, self.id)
        self.child.parent = self.parent
    
    def _remove(self):
        del self.parent.children[self.id]
        del self.parent.child_order[self.index]
        self.child.parent = None

class SetPropertyAction(Action):
    def __init__(self, node: Node, key, old_value, new_value):
        self.node = node
        self.key = key
        self.old_value = old_value
        self.new_value = new_value

    def perform(self):
        self.node.properties[self.key] = self.new_value

    def undo(self):
        self.node.properties[self.key] = self.old_value