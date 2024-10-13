from collections import deque
import events

class Transaction:
    def begin(self, obj):
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
        self.trans: Transaction = None

    def begin_transaction(self, obj):
        self.trans = Transaction()
        self.trans.begin(obj)

    def end_transaction(self):
        self.trans.end()
        self.past.append(self.trans)
        self.future.clear()

    # manually triggering events
    # as the context manager calls the undo manager

    def undo(self):
        trans = self.past.pop()
        if trans is not None:
            trans.undo()
            events.edit.trigger(sender=trans.obj)
            self.future.append(trans)

    def redo(self):
        trans = self.future.pop()
        if trans is not None:
            trans.redo()
            events.edit.trigger(sender=trans.obj)
            self.past.append(trans)

uman = UndoManager()