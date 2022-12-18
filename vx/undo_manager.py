from collections import deque
from node_actions import Action

# TODO: implement action groups!

class UndoManager:
    def __init__(self, past_len: int = 10, future_len: int = 10):
        self.past: deque[Action] = deque(maxlen=past_len)
        self.future: deque[Action] = deque(maxlen=future_len)

    def clear_history(self):
        self.past.clear()
        self.future.clear()

    def perform(self, new_action: Action):
        new_action.perform()
        self.past.append(new_action)
        self.future.clear()

    def can_undo(self):
        return len(self.past) > 0

    def undo(self):
        if self.can_undo():
            action = self.past.pop()
            action.undo()
            self.future.append(action)

    def can_redo(self):
        return len(self.future) > 0

    def redo(self):
        if self.can_redo():
            action = self.future.pop()
            action.perform()
            self.past.append(action)