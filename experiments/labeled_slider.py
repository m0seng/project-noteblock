from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt


class LabeledSlider(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(float)
    def __init__(
        self,
        text="stuff",
        min_value=0.0,
        max_value=1.0,
        steps=100,
        init_value=0.5,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.text = text
        self.min_value = min_value
        self.max_value = max_value
        self.steps = steps
        self.init_value = init_value

        self._layout = QtWidgets.QVBoxLayout()

        self._text_label = QtWidgets.QLabel(self.text)
        self._text_label.setAlignment(Qt.AlignHCenter)
        self._layout.addWidget(self._text_label)

        self._slider = QtWidgets.QSlider(Qt.Horizontal)
        self._slider.setRange(0, self.steps)
        self._slider.setValue(self.convert_to_slider(self.init_value))
        self._slider.valueChanged.connect(self.slider_value_changed)
        self._layout.addWidget(self._slider)

        self._value_label = QtWidgets.QLabel(text=str(self.init_value))
        self._value_label.setAlignment(Qt.AlignHCenter)
        self._layout.addWidget(self._value_label)

        self.setLayout(self._layout)

    def convert_to_slider(self, value: float) -> int:
        return int(self.steps * (value - self.min_value) / (self.max_value - self.min_value))

    def convert_from_slider(self, value: int) -> float:
        return self.min_value + (value / self.steps) * (self.max_value - self.min_value)

    def slider_value_changed(self, value: int):
        converted_value = self.convert_from_slider(value)
        self._value_label.setText(str(converted_value))
        self.valueChanged.emit(converted_value)
        

app = QtWidgets.QApplication([])
slider = LabeledSlider()
slider.show()
app.exec()