from abc import ABC, abstractmethod

class Event(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listeners: list[function] = []

    def add_listener(self, listener: function):
        self.listeners.append(listener)

    def remove_listener(self, listener: function):
        self.listeners.remove(listener)

    def trigger(self):
        for listener in self.listeners:
            listener()