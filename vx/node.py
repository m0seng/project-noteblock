class Node:
    '''
    A simplified adaptation of the ValueTree concept from JUCE.
    
    Many features have been omitted as I do not need them.
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

    def get_index_of_child(self, child: "Node"):
        child_id = self.get_id_of_child(child)
        if child_id is not None:
            return self.child_order.index(child_id)
        return None # maybe return -1?

    def get_id_of_child(self, child: "Node"):
        for k, v in self.children.items():
            if v == child:
                return k
        return None # maybe return -1?

    def _set_property(self, key, value):
        self.properties[key] = value

    def _add_child(self, child: "Node", id: int, index: int):
        self.children[id] = child
        self.parent.child_order.insert(index, id)
        child.parent = self

    def _remove_child(self, child: "Node", id: int, index: int):
        del self.children[id]
        del self.child_order[index]
        child.parent = None