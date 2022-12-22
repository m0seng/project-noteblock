from collections import deque
from node_actions import Action

class UndoManager:
    def __init__(self, past_len: int = 10, future_len: int = 10):
        self.past: deque[Action | list[Action]] = deque(maxlen=past_len)
        self.future: deque[Action | list[Action]] = deque(maxlen=future_len)
        self.current_group: list[Action] = []
        self.making_group: bool = False

    def reset(self):
        self.past.clear()
        self.future.clear()
        self.current_group = []
        self.making_group = False

    def perform_without_undo(self, new_action: Action):
        new_action.perform()

    def perform(self, new_action: Action):
        new_action.perform()
        if self.making_group:
            self.current_group.append(new_action)
        else:
            self.past.append(new_action)
        self.future.clear()
    
    def start_group(self):
        if not self.making_group:
            self.current_group = []
            self.making_group = True

    def end_group(self):
        if self.making_group:
            self.past.append(self.current_group)
            self.current_group = []
            self.making_group = False

    def can_undo(self):
        return len(self.past) > 0

    def undo(self):
        if self.can_undo() and not self.making_group:
            action = self.past.pop()
            if isinstance(action, list):
                for act in reversed(action): act.undo()
            else:
                action.undo()
            self.future.append(action)

    def can_redo(self):
        return len(self.future) > 0

    def redo(self):
        if self.can_redo() and not self.making_group:
            action = self.future.pop()
            if isinstance(action, list):
                for act in action: act.perform()
            else:
                action.perform()
            self.past.append(action)