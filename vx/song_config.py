from node import Node

class SongConfig(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_property("pattern_length", 16)
        self._set_property("sequence_length", 20)