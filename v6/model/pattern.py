from .value_tree import ValueTree

class Pattern(ValueTree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)