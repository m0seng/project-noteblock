from node import Node
from node_contexts import AddChildContext, RemoveChildContext, SetPropertyContext
from node_actions import AddChildAction, RemoveChildAction, SetPropertyAction
from undo_manager import UndoManager

# This is where I stick methods to make editing nodes MUCH easier
# passing an undo manager for now but it might make its own
# also partially facades undo manager, for example when making action groups

class NodeEditor:
    def __init__(self, uman: UndoManager):
        self.uman = uman