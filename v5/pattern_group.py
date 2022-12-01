from collections import UserDict
from savable import Savable
from pattern import Pattern

class PatternGroup(Savable, UserDict):
    def init_state(self):
        ...

    def init_props(self):
        self.data: dict[int, Pattern] = {}

    def to_dict(self) -> dict:
        return {
            k: v.to_dict() for k, v in self.data.items()
        }

    def from_dict(self, source: dict):
        # don't worry about the old channels here
        # the context manager event will take care of them
        self.data = {}
        for k, v in source.items():
            pattern = Pattern.create_from_dict(v)
            self.data[int(k)] = pattern # TODO: catch errors here