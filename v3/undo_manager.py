from collections import deque
from .save_mixin import SaveMixin
from .transaction import Transaction

past_length = 10
future_length = 5
past: deque[Transaction] = deque(maxlen=past_length)
future: deque[Transaction] = deque(maxlen=future_length)
trans: Transaction = None

def begin_transaction(obj: SaveMixin):
    trans = Transaction()
    trans.begin(obj)

def end_transaction():
    trans.end()
    past.append(trans)
    future.clear()

def undo():
    trans = past.pop()
    if trans is not None:
        trans.undo()
        future.append(trans)
        trans.obj.change_event.trigger()

def redo(self):
    trans = future.pop()
    if trans is not None:
        trans.redo()
        past.append(trans)
        trans.obj.change_event.trigger()