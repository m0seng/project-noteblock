from abc import ABC, abstractmethod

class Savable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        """MAKE COPIES OF MUTABLES!!!"""
        ...

    @abstractmethod
    def from_dict(self, source: dict):
        ...