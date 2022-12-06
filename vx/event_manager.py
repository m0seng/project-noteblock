from undoable_action import UndoableAction

class EventManager:
    def perform(self, action: UndoableAction):
        action.perform() # TODO: replace with the undo management