from abc import ABC, abstractmethod
import tkinter as tk
import tkinter.ttk as ttk
from savable import Savable
import events

# TODO: HOW TO ATTACH TO MULTIPLE THINGS?
# e.g.: Piano Roll attaches to Pattern, PatternGroup, Config and Preferences
# solution: model is a loose coupling
# just hook into the events and run custom class/object checks

class SavableFrame(ttk.Frame, ABC):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model: Savable = None
        self.suppress_sync = False # use when this Frame is making the edits
        events.edit.add_listener(self.update)

    @abstractmethod
    def update(self, sender):
        ...

    def connect(self, model: Savable):
        if self.model is not None:
            self.disconnect()
        self.model = model

    def disconnect(self):
        self.model = None

    def destroy(self, *args, **kwargs):
        self.disconnect()
        events.edit.remove_listener(self.update)
        super().destroy(*args, **kwargs)