from abc import ABC, abstractmethod

class Savable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        """MAKE COPIES OF MUTABLES!!!"""
        ...

    @abstractmethod
    def from_dict(self, source: dict):
        ...

    @classmethod
    def create_from_dict(cls, source: dict):
        obj = cls()
        obj.from_dict(source)
        return obj

    def copy(self) -> "Savable":
        return self.__class__.create_from_dict(self.to_dict)