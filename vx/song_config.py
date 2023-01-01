from node import Node

class SongConfig(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_property("name", "song name")
        self._set_property("pattern_length", 16)
        self._set_property("sequence_length", 20)
        self._set_property("loop_enabled", False)
        self._set_property("loop_start", 0)
        self._set_property("loop_end", 4)