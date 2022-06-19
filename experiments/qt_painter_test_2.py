import sys
import random
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt


COLORS = [
# 17 undertones https://lospec.com/palette-list/17undertones
'#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
'#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
'#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]

SPRAY_PARTICLES = 100
SPRAY_DIAMETER = 10

class QPaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24,24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)


class Canvas(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        pixmap = QtGui.QPixmap(600, 300)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')
        self.pen_diameter = 1

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def set_pen_diameter(self, d):
        self.pen_diameter = d

    def mouseMoveEvent(self, e):
        canvas = self.pixmap()
        painter = QtGui.QPainter(canvas)
        p = painter.pen()
        p.setWidth(self.pen_diameter)
        p.setColor(self.pen_color)
        painter.setPen(p)

        for n in range(SPRAY_PARTICLES):
            xo = random.gauss(0, SPRAY_DIAMETER)
            yo = random.gauss(0, SPRAY_DIAMETER)
            painter.drawPoint(e.x()+xo, e.y()+yo)

        painter.end()
        self.setPixmap(canvas)

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.canvas = Canvas()

        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        w.setLayout(l)
        l.addWidget(self.canvas)

        palette = QtWidgets.QHBoxLayout()
        self.add_palette_buttons(palette)
        l.addLayout(palette)

        controls = QtWidgets.QHBoxLayout()
        
        diameter_slider = QtWidgets.QSlider(Qt.Horizontal)
        diameter_slider.setMinimum(1)
        diameter_slider.setMaximum(20)
        diameter_slider.sliderMoved.connect(lambda d: self.canvas.set_pen_diameter(d))
        controls.addWidget(diameter_slider)

        l.addLayout(controls)

        self.setCentralWidget(w)

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()