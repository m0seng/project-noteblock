from typing import Callable

class Event:
    def __init__(self):
        self.listeners: list[Callable] = []

    def add_listener(self, listener: Callable):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener: Callable):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def trigger(self, **kwargs):
        for listener in self.listeners:
            listener(**kwargs)

# TODO: instantiate custom events here!
# pass sender as argument

edit = Event()