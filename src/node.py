from copy import copy, deepcopy

class Node:
    """Base class of all song objects."""

    def __init__(self, *args, **kwargs):
        self.parent: Node | None = None
        self.properties = {}
        self.children: dict[int, Node] = {}
        self.child_order: list[int] = []

    def to_dict(self):
        return {
            "class": self.__class__.__name__,
            "properties": deepcopy(self.properties),
            "child_order": deepcopy(self.child_order),
            "children": {str(k): v.to_dict() for k, v in self.children.items()}
        }
    
    def get_property(self, key):
        # shouldn't need deepcopy here - nested data should be separated into nodes
        return copy(self.properties.get(key, None))

    def get_child_by_id(self, id: int):
        return self.children.get(id, None)

    def get_child_at_index(self, index: int):
        if 0 <= index < len(self.child_order):
            return self.get_child_by_id(self.child_order[index])
        return None

    def get_child_by_class(self, _class):
        for child in self.children.values():
            if isinstance(child, _class): return child

    def get_index_of_child(self, child: "Node"):
        child_id = self.get_id_of_child(child)
        if child_id is not None:
            return self.child_order.index(child_id)
        return None

    def get_id_of_child(self, child: "Node"):
        for k, v in self.children.items():
            if v == child:
                return k
        return None

    def is_root(self):
        return True if self.parent is None else False

    def next_available_id(self):
        return max(self.children.keys(), default=-1) + 1

    def children_iterator(self):
        for child_id in self.child_order:
            yield self.get_child_by_id(child_id)

    def children_count(self):
        return len(self.children)

    def _set_property(self, key, value):
        self.properties[key] = value

    def _add_child(self, child: "Node", id: int, index: int):
        self.children[id] = child
        if index is not None: self.child_order.insert(index, id) # allows no index insertion for factory
        child.parent = self

    def _remove_child(self, child: "Node", id: int, index: int):
        del self.children[id]
        del self.child_order[index]
        child.parent = None

    def _move_child(self, old_index: int, new_index: int):
        child_id = self.child_order.pop(old_index)
        self.child_order.insert(new_index, child_id)