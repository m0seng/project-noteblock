from abc import ABC, abstractmethod
from .event import Event
import undo_manager as undoman

class Savable(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pre_change = Event()
        self.post_change = Event()
    
    def __enter__(self):
        self.pre_change.trigger()
        undoman.begin_transaction(self)
        
    def __exit__(self, exc_type, exc_value, exc_tb):
        undoman.end_transaction()
        self.post_change.trigger()
        
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
        return self.__class__.create_from_dict(self.to_dict())

    def altered_copy(self, **kwargs) -> "Savable":
        temp_dict = self.to_dict()
        temp_dict.update(kwargs)
        return self.__class__.create_from_dict(temp_dict)