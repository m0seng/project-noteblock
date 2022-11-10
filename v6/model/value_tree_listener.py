from abc import ABC, abstractmethod
from value_tree import ValueTree

class ValueTreeListener(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
       ...

    @abstractmethod
    def vt_property_changed(self, tree: ValueTree, key: str):
        ...

    @abstractmethod
    def vt_child_added(self, tree: ValueTree, child: ValueTree):
        ...

    @abstractmethod
    def vt_child_removed(self, tree: ValueTree, child: ValueTree, index: int):
        ...

    @abstractmethod
    def vt_child_order_changed(self, tree: ValueTree, old_index: int, new_index: int):
        ...

    @abstractmethod
    def vt_parent_changed(self, tree: ValueTree):
        ...