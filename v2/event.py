from abc import ABC, abstractmethod

class Event(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listeners: list = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener(self, listener):
        self.listeners.remove(listener)

    def trigger(self):
        for listener in self.listeners:
            listener()