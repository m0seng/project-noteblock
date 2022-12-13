from typing import Any
from dataclasses import dataclass
from node import Node

# NOTE: might subclass these from a common ancestor?

@dataclass
class AddChildContext:
    parent: Node
    child: Node
    id: int
    index: int

@dataclass
class RemoveChildContext:
    parent: Node
    child: Node
    id: int
    index: int

@dataclass
class SetPropertyContext:
    node: Node
    key: Any
    old_value: Any
    new_value: Any