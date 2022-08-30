# heavily inspired by FamiStudio's undo/redo system
from collections import deque
from savable import Savable

class Transaction:
    # TODO: make this __slots__ for speed?
    def begin(self, obj: Savable):
        self.obj = obj
        self.before = self.obj.to_dict()

    def end(self):
        self.after = self.obj.to_dict()

    def undo(self):
        self.obj.from_dict(self.before)

    def redo(self):
        self.obj.from_dict(self.after)

class UndoManager:
    def __init__(self):
        self.past_length = 10
        self.future_length = 5
        self.past: deque[Transaction] = deque(maxlen=self.past_length)
        self.future: deque[Transaction] = deque(maxlen=self.future_length)

    def begin_transaction(self, obj: Savable):
        self.trans = Transaction()
        self.trans.begin(obj)

    def end_transaction(self):
        self.trans.end()
        self.past.append(self.trans)
        self.future.clear()

    def undo(self):
        trans = self.past.pop()
        trans.undo()
        self.future.append(trans)

    def redo(self):
        trans = self.future.pop()
        trans.redo()
        self.past.append(trans)