# color_palette.py

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QRect, pyqtSignal

class ColorPaletteWindow(QWidget):
    color_selected = pyqtSignal(QColor)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Palette")
        self.setFixedSize(200, 120)
        self.colors = [
            QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255),
            QColor(255, 255, 0), QColor(0, 255, 255), QColor(255, 255, 255)
        ]
        self.rects = []

    def paintEvent(self, event):
        painter = QPainter(self)
        self.rects.clear()
        w, h = 40, 40
        for i, color in enumerate(self.colors):
            x = 10 + (i % 3) * (w + 10)
            y = 10 + (i // 3) * (h + 10)
            rect = QRect(x, y, w, h)
            self.rects.append((rect, color))
            painter.fillRect(rect, color)

    def mousePressEvent(self, event):
        for rect, color in self.rects:
            if rect.contains(event.pos()):
                self.color_selected.emit(color)
                break
