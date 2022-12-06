from action import Action
from event_manager import EventManager

# TODO: more specific child manipulation methods

class Node:
    '''
    A simplified adaptation of the ValueTree concept from JUCE.
    
    Many features have been omitted as I do not need them.
    '''
    def __init__(self, event_manager: EventManager):
        self.parent: Node | None = None
        self.properties = {}
        self.children: dict[int, Node] = {}
        self.child_order: list[int] = []
        self.event_manager = event_manager

    def get_child_by_id(self, id: int):
        return self.children[id]

    def get_child_by_index(self, index: int):
        return self.get_child_by_id(self.child_order[index])

    def add_child(self, child: "Node"):
        if child.parent is not None:
            child.parent.remove_child(child)
        next_id = max(self.children, default=0) + 1
        next_index = len(self.child_order)
        self.event_manager.perform(AddChildAction(
            parent=self,
            child=child,
            id=next_id,
            index=next_index
        ))

    def remove_child(self, child: "Node"):
        if child not in self.children.values(): return
        child_id = next(k for k, v in self.children.items() if v == child)
        child_index = self.child_order.index(child_id)
        self.event_manager.perform(AddChildAction(
            parent=self,
            child=child,
            id=child_id,
            index=child_index,
            reversed=True
        ))

    def get_property(self, key):
        return self.properties[key]

    def set_property(self, key, value):
        # NOTE: this sets the property even if it does not already exist
        # useful for testing purposes but maybe not ideal?
        old_value = self.properties.get(key, None)
        self.event_manager.perform(SetPropertyAction(
            node=self,
            key=key,
            old_value=old_value,
            new_value=value
        ))

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

def main():
    eman = EventManager()
    root = Node(eman)

    root.set_property("bruh", "real")
    print(root.properties)

    child_1 = Node(eman)
    child_2 = Node(eman)
    root.add_child(child_1)
    root.add_child(child_2)

    print(root.children)
    print(root.child_order)

if __name__ == "__main__":
    main()