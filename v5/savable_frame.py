from abc import ABC, abstractmethod
import tkinter as tk
import tkinter.ttk as ttk
from .savable import Savable
from . import events

# TODO: HOW TO ATTACH TO MULTIPLE THINGS?
# e.g.: Piano Roll attaches to Pattern, PatternGroup, Config and Preferences

class SavableFrame(ttk.Frame, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model: Savable = None
        self.suppress_sync = False # use when this Frame is making the edits

    @abstractmethod
    def sync(self):
        ...

    def update(self, sender):
        if sender is self.model and not self.suppress_sync:
            self.sync()

    def connect(self, model: Savable):
        self.model = model
        events.edit.add_listener(self.update)
        self.sync()

    def disconnect(self):
        events.edit.remove_listener(self.update)
        self.model = None

    def destroy(self, *args, **kwargs):
        self.disconnect()
        super().destroy(*args, **kwargs)