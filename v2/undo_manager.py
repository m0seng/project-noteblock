# heavily inspired by FamiStudio's undo/redo system

from savable import Savable

class Transaction:
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
        self.past: list[Transaction] = []
        self.future: list[Transaction] = []

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