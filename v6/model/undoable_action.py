from abc import ABC, abstractmethod

class UndoableAction(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def perform(self):
        pass

    @abstractmethod
    def undo(self):
        pass