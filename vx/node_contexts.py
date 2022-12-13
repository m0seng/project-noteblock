from dataclasses import dataclass
from node import Node

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