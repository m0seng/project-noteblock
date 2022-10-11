from .savable import Savable
from .pattern import Pattern
from .note import Note

class PatternGroup(Savable):
    def init_state(self):
        ...

    def init_props(self):
        self.patterns: list[Pattern] = []

    def to_dict(self) -> dict:
        return {
            "patterns": [pattern.to_dict() for pattern in self.patterns]
        }

    def from_dict(self, source: dict):
        # don't worry about the old channels here
        # the context manager event will take care of them
        self.patterns = []
        for pattern_dict in source["patterns"]:
            channel = Pattern.create_from_dict(pattern_dict)
            self.patterns.append(channel)