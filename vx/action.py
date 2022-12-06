from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def perform(self):
        ...

    @abstractmethod
    def undo(self):
        ...