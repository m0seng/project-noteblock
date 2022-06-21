from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt


def _clamp(value, lower, upper):
    return lower if value < lower else upper if value > upper else value


class LabeledSlider(QtWidgets.QWidget):
    sliderMoved = QtCore.Signal(float)

    def __init__(
        self,
        title: str,
        value_format: str,
        min_value: float,
        max_value: float,
        slider_steps: int,
        init_value: float,
        *args, **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._title = title
        self._value_format = value_format
        self._min_value = min_value
        self._max_value = max_value
        self._slider_steps = slider_steps
        self._init_value = init_value

        self._init_ui()

    def _init_ui(self):
        self._layout = QtWidgets.QVBoxLayout()

        self._title_label = QtWidgets.QLabel(self._title)
        self._title_label.setAlignment(Qt.AlignHCenter)
        self._layout.addWidget(self._title_label)

        self._slider = QtWidgets.QSlider(Qt.Horizontal)
        self._slider.setRange(0, self._slider_steps)
        self._slider.sliderMoved.connect(self._slider_moved)

        self._layout.addWidget(self._slider)

        self._value_label = QtWidgets.QLabel()
        self._value_label.setAlignment(Qt.AlignHCenter)
        self._layout.addWidget(self._value_label)

        self.set_value(self._init_value)
        self.setLayout(self._layout)

    def set_value(self, value: float):
        self._value_label.setText(self._format_for_display(value))
        self._slider.setValue(self._convert_to_slider(self._init_value))

    def _slider_moved(self, slider_value: int):
        value = self._convert_from_slider(slider_value)
        self._value_label.setText(self._format_for_display(value))
        self.sliderMoved.emit(value)

    def _convert_to_slider(self, value: float) -> int:
        return int(
            self._slider_steps
            * (value - self._min_value)
            / (self._max_value - self._min_value)
        )

    def _convert_from_slider(self, value: int) -> float:
        return (
            self._min_value
            + (value / self._slider_steps)
            * (self._max_value - self._min_value)
        )

    def _format_for_display(self, value: float) -> str:
        return self._value_format.format(value=value)


class AutoClampedSliderValue:
    def __init__(
        self,
        title: str = "placeholder",
        value_format: str = "{value:.2f}",
        min_value: float = 0.0,
        max_value: float = 1.0,
        slider_steps: int = 100,
        init_value: float = 0.5,
    ):
        self._min_value = min_value
        self._max_value = max_value

        self.ui = LabeledSlider(
            title=title,
            value_format=value_format,
            min_value=min_value,
            max_value=max_value,
            slider_steps=slider_steps,
            init_value=init_value
        )
        self.ui.sliderMoved.connect(self._set_value_from_slider)

        self.value = init_value

    def _set_value_from_slider(self, value: float):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: float):
        self._value = _clamp(val, self._min_value, self._max_value)
        self.ui.set_value(self._value)

app = QtWidgets.QApplication([])
thing = AutoClampedSliderValue(
    title="stuff",
    min_value=1.0,
    max_value=2.0,
    slider_steps=100,
    init_value=1.5
)

thing.ui.show()
app.exec()