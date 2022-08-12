from abc import ABC, abstractmethod

class Savable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        ...

    @abstractmethod
    def from_dict(self, source: dict):
        ...