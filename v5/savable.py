from abc import ABC, abstractmethod
from . import events
from .undo_manager import uman

class Savable(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __enter__(self):
        uman.begin_transaction(self)
        
    def __exit__(self, exc_type, exc_value, exc_tb):
        uman.end_transaction()
        events.edit.trigger(sender=self)
        
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