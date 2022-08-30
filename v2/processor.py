from abc import ABC, abstractmethod
from savable import Savable

class Processor(Savable, ABC):
    def __init__(self):
        ...

    