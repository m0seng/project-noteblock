from .savable import Savable

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