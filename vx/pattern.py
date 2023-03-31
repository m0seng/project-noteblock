from node import Node

class Pattern(Node):
    """Song object - contains a chronological list of notes."""

    def __init__(self, *args, pattern_length: int = 16, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_property("name", "pattern name")
        self._set_property("colour", "gray75")
        self._set_property("notes", [-1] * pattern_length)

    def get_notes(self, pat_tick: int) -> list[int]:
        return [self.get_property("notes")[pat_tick]]