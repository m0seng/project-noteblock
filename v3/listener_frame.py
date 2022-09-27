from abc import ABC, abstractmethod
import tkinter as tk
import tkinter.ttk as ttk
from .save_mixin import SaveMixin

class ListenerFrame(ttk.Frame, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model: SaveMixin = None
        self.block_sync = False

    @abstractmethod
    def sync(self):
        ...

    def callback(self):
        if self.model is not None and not self.block_sync:
            self.sync()

    def connect(self, model: SaveMixin):
        if self.model is not None:
            self.disconnect()
        model.change_event.add_listener(self.callback)
        self.model = model
        self.sync()

    def disconnect(self):
        if self.model is not None:
            self.model.change_event.remove_listener(self.callback)
            self.model = None

    def destroy(self, *args, **kwargs):
        self.disconnect()
        super().destroy(*args, **kwargs)