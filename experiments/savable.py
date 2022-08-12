from abc import ABC, abstractmethod

class Savable(ABC):
    @abstractmethod
    def to_dict(self):
        ...

    @abstractmethod
    def from_dict(self, source: dict):
        ...

    @classmethod
    def create_from_dict(cls, source: dict):
        obj = cls()
        obj.from_dict(source)
        return obj