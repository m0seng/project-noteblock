from node import Node

class PatternGroup(Node):
    """Song object - holds all of a song's patterns."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)