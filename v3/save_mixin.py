from abc import ABC, abstractmethod
from .event import Event
import undo_manager as undoman

class SaveMixin(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.change_event = Event()
    
    def __enter__(self):
        undoman.begin_transaction(self)
        
    def __exit__(self, exc_type, exc_value, exc_tb):
        undoman.end_transaction()
        self.change_event.trigger()
        
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

    def copy(self) -> "SaveMixin":
        return self.__class__.create_from_dict(self.to_dict())

    def altered_copy(self, **kwargs) -> "SaveMixin":
        temp_dict = self.to_dict()
        temp_dict.update(kwargs)
        return self.__class__.create_from_dict(temp_dict)