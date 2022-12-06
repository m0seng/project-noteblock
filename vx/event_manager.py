from action import Action

class EventManager:
    def perform(self, action: Action):
        action.perform() # TODO: replace with the undo management