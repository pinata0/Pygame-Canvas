# vectorlayer.py

from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QPoint, Qt
from engine.stroke import Stroke

class VectorLayer:
    def __init__(self):
        self.strokes = []

    def add_stroke(self, stroke):
        self.strokes.append(stroke)

    def render(self, painter: QPainter):
        for stroke in self.strokes:
            if len(stroke.points) >= 2:
                pen = QPen(QColor(*stroke.color[:3]), stroke.radius)
                pen.setCapStyle(Qt.PenCapStyle.RoundCap)
                pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
                painter.setPen(pen)
                for i in range(1, len(stroke.points)):
                    painter.drawLine(stroke.points[i - 1], stroke.points[i])
            for pt in stroke.points:
                painter.setPen(QPen(QColor(*stroke.color[:3]), 1))
                painter.setBrush(QColor(*stroke.color[:3]))
                painter.drawEllipse(pt, stroke.radius // 2, stroke.radius // 2)

    def erase_near(self, x, y, radius):
        for stroke in self.strokes[:]:  # 복사 순회
            for pt in stroke.points:
                if (pt.x() - x) ** 2 + (pt.y() - y) ** 2 <= radius ** 2:
                    self.strokes.remove(stroke)
                    break

    @staticmethod
    def find_erased_indices(stroke, x, y, radius):
        erased = []
        for i, pt in enumerate(stroke.points):
            if (pt.x() - x) ** 2 + (pt.y() - y) ** 2 <= radius ** 2:
                erased.append(i)
        return erased

    @staticmethod
    def split_stroke(stroke, erased_indices):
        if not erased_indices:
            return [stroke]

        segments = []
        current_points = []
        erased_set = set(erased_indices)

        for i, pt in enumerate(stroke.points):
            if i in erased_set:
                if current_points:
                    new_stroke = Stroke(stroke.color, stroke.radius)
                    new_stroke.points = current_points
                    segments.append(new_stroke)
                    current_points = []
            else:
                current_points.append(pt)

        if current_points:
            new_stroke = Stroke(stroke.color, stroke.radius)
            new_stroke.points = current_points
            segments.append(new_stroke)

        return segments

    def partial_erase(self, x, y, radius):
        updated_strokes = []

        for stroke in self.strokes:
            erased = self.find_erased_indices(stroke, x, y, radius)
            if erased:
                split = self.split_stroke(stroke, erased)
                updated_strokes.extend(split)
            else:
                updated_strokes.append(stroke)

        self.strokes = updated_strokes
