from abc import ABC, abstractmethod
import tkinter as tk
import tkinter.ttk as ttk
from .save_mixin import SaveMixin
from .event import Event

class SavableFrame(ttk.Frame, ABC):
    def __init__(self, aux_events: list[Event], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model: SaveMixin = None
        self.aux_events = aux_events
        self.suppress_sync = False # use when this Frame is making the edits

    @abstractmethod
    def sync(self):
        ...

    def update(self):
        if self.model is not None and not self.suppress_sync:
            self.sync()

    def connect(self, model: SaveMixin):
        if self.model is not None:
            self.disconnect()
        self.model = model
        self.model.change_event.add_listener(self.update)
        self.sync()

    def disconnect(self):
        if self.model is not None:
            self.model.change_event.remove_listener(self.update)
            self.model = None

    def aux_connect(self):
        for event in self.aux_events:
            event.add_listener(self.update)
    
    def aux_disconnect(self):
        for event in self.aux_events:
            event.remove_listener(self.update)

    def destroy(self, *args, **kwargs):
        self.aux_disconnect()
        self.disconnect()
        super().destroy(*args, **kwargs)