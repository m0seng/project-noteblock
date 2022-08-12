from collections.abc import MutableMapping
from typing import Any

class UndoableDict(MutableMapping):
    # see https://redux.js.org/usage/implementing-undo-history
    def __init__(self, data: dict = {}):
        self.past: dict[Any, list[Any]] = {}
        self.present: dict[Any] = {}
        self.future: dict[Any, list[Any]] = {}

        self.present.update(data)
        self.reset_history()

    def reset_history(self):
        for key in self.present.keys():
            self.past[key] = []
            self.future[key] = []

    def undo(self, key):
        self.future[key].append(self.present[key])
        self.present[key] = self.past[key].pop()

    def redo(self, key):
        self.past[key].append(self.present[key])
        self.present[key] = self.future[key].pop()

    def __getitem__(self, key):
        return self.present[key]

    def __setitem__(self, key, value):
        self.past[key].append(self.present[key])
        self.present[key] = value
        self.future[key].clear()

    def __delitem__(self, key):
        del self.past[key]
        del self.present[key]
        del self.future[key]

    def __iter__(self):
        return iter(self.present)

    def __len__(self):
        return len(self.present)

    def __repr__(self):
        return f"{type(self).__name__}({self.present})"



def main():
    test = UndoableDict({"a": 1, "b": 2})
    print(test)

if __name__ == "__main__":
    main()