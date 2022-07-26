class Parameter:
    def __init__(
        self,
        display_name: str,
        value_format: str,
        min_value: float,
        max_value: float,
        init_value: float,
    ):
        self.display_name = display_name
        self.value_format = value_format
        self.min_value = min_value
        self.max_value = max_value
        self.init_value = init_value

        self.value = self.init_value

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, val: float):
        self._value = self._clamped_value(val)

    def value_string(self) -> str:
        return self.value_format.format(value=self._value)

    def _clamped_value(self, val: float) -> float:
        return min(max(val, self.min_value), self.max_value)