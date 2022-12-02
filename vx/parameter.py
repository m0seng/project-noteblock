from dataclasses import dataclass

@dataclass(slots=True)
class ParameterRange:
    min: float
    max: float
    start: float
    step: float

class Parameter:
    def __init__(self, range: ParameterRange):
        self.range = range
        self._value = self.range.start

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v <= self.range.min:
            self._value = self.range.min
        elif v >= self.range.max:
            self._value = self.range.max
        else:
            if self.range.step is not None:
                # TODO: fix this without floating point nightmares
                step_number = (v - self.range.min) // self.range.step
                self._value = (step_number * self.range.step) + self.range.min
            else:
                self._value = v

def main():
    param = Parameter(ParameterRange(
        min=0,
        max=11.5,
        start=4,
        step=2))
    
    while True:
        print("Enter value to set: ", end='')
        param.value = float(input())
        print(f"Parameter value set to: {param.value}")

if __name__ == "__main__":
    main()