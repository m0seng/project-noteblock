from abc import ABC, abstractmethod

class CallbacksMixin(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callbacks: list[function] = []

    def add_callback(self, callback: function):
        self.callbacks.append(callback)

    def remove_callback(self, callback: function):
        self.callbacks.remove(callback)

    def run_callbacks(self):
        for callback in self.callbacks:
            callback()