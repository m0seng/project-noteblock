from dataclasses import dataclass

@dataclass(slots=True)
class Note:
    instrument: int = 0
    pitch: int = 0
    volume: float = 1 # 0 to 1
    pan: float = 0 # -1 to 1
    is_main: bool = True