from abc import ABC, abstractmethod

class SaveMixin(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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