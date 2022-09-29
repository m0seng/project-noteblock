from .save_mixin import SaveMixin
from abc import ABC, abstractmethod
from typing import Type

class SavableGroup(SaveMixin):
    def __init__(self, subclass: Type[SaveMixin], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.savables: list[subclass] = []
        self.subclass = subclass

    def to_dict(self):
        return {
            "savables": [savable.to_dict() for savable in self.savables]
        }

    def from_dict(self, source):
        self.savables = []
        for saved_dict in source["savables"]:
            savable = self.subclass.create_from_dict(saved_dict)
            self.savables.append(savable)

    @abstractmethod
    def init_subclass(self, source) -> SaveMixin:
        ...