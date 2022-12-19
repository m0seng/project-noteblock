from dataclasses import dataclass

@dataclass(slots=True)
class Note:
    instrument: int = 0
    pitch: int = 0
    volume: float = 1 # 0 to 1
    pan: float = 0 # -1 to 1

    def apply_volume_and_pan(self, volume: float, pan: float):
        new_volume = min(self.volume * volume, 1)
        new_pan = max(min(self.pan + pan, 1), -1)
        return Note(
            instrument=self.instrument,
            pitch=self.pitch,
            volume=new_volume,
            pan=new_pan
        )