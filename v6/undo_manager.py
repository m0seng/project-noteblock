# obviously not complete

from undoable_action import UndoableAction

class UndoManager:
    def __init__(self):
        ...

    def perform(self, new_action: UndoableAction):
        ...

    def undo(self):
        ...

    def redo(self):
        ...