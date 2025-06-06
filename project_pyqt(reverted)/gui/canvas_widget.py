# canvas_widget.py

from typing import List, Tuple
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QMouseEvent, QCursor, QKeyEvent
from PyQt5.QtCore import Qt, QPoint

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(512, 512)
        self.strokes: List[Tuple[QColor, int, List[QPoint]]] = []
        self.current_stroke: List[QPoint] = []
        self.brush_color = QColor(0, 0, 255)
        self.brush_radius = 10
        self.current_tool = "brush"
        self.eraser_mode = "stroke"
        self.eraser_radius = 20
        self.mouse_inside = False
        self._last_key = None 
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)

    def set_brush_color(self, color: QColor):
        self.brush_color = color

    def set_brush_radius(self, radius: int):
        self.brush_radius = radius

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.current_tool == "brush":
                self.current_stroke = [event.pos()]
            elif self.current_tool == "eraser":
                if self.eraser_mode == "stroke":
                    self.erase_whole_stroke_at(event.pos())
                elif self.eraser_mode == "area":
                    self.erase_area_at(event.pos())
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.current_tool == "brush":
                self.current_stroke.append(event.pos())
            elif self.current_tool == "eraser":
                if self.eraser_mode == "stroke":
                    self.erase_whole_stroke_at(event.pos())
                elif self.eraser_mode == "area":
                    self.erase_area_at(event.pos())
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.current_stroke:
            self.strokes.append((self.brush_color, self.brush_radius, self.current_stroke))
            self.current_stroke = []

    def wheelEvent(self, event):
        delta = event.angleDelta().y() // 120
        if self.current_tool == "brush":
            self.brush_radius = max(1, self.brush_radius + delta)
        elif self.current_tool == "eraser":
            self.eraser_radius = max(1, self.eraser_radius + delta)
        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        if self._last_key == Qt.Key_B and key == Qt.Key_1:
            self.current_tool = "brush"
            print("🖌️ 브러시 모드로 전환")
            self.update()

        elif self._last_key == Qt.Key_E and key == Qt.Key_1:
            self.current_tool = "eraser"
            self.eraser_mode = "stroke"
            print("✂️ 획 지우개 모드로 전환")
            self.update()

        elif self._last_key == Qt.Key_E and key == Qt.Key_2:
            self.current_tool = "eraser"
            self.eraser_mode = "area"
            print("🧼 영역 지우개 모드로 전환")
            self.update()

        self._last_key = key  # 현재 키를 저장해서 다음과 비교

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)

        for color, radius, stroke in self.strokes:
            pen = QPen(color, radius)
            pen.setStyle(Qt.SolidLine)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            for i in range(1, len(stroke)):
                painter.drawLine(stroke[i - 1], stroke[i])

        if self.current_stroke:
            pen = QPen(self.brush_color, self.brush_radius)
            pen.setStyle(Qt.SolidLine)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            for i in range(1, len(self.current_stroke)):
                painter.drawLine(self.current_stroke[i - 1], self.current_stroke[i])

        if self.mouse_inside:
            cursor = self.mapFromGlobal(QCursor.pos())
            radius = self.brush_radius if self.current_tool == "brush" else self.eraser_radius
            pen = QPen(Qt.black)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.transparent)
            painter.drawEllipse(cursor, radius, radius)

    def erase_whole_stroke_at(self, pos: QPoint):
        new_strokes = []
        for color, radius, stroke in self.strokes:
            if any((pt - pos).manhattanLength() <= self.eraser_radius for pt in stroke):
                continue  # 이 stroke는 제거
            new_strokes.append((color, radius, stroke))
        self.strokes = new_strokes

    def erase_area_at(self, pos: QPoint):
        updated_strokes = []

        for color, radius, stroke in self.strokes:
            kept_segments = []
            current_segment = []

            for pt in stroke:
                if (pt - pos).manhattanLength() <= self.eraser_radius:
                    if current_segment:
                        kept_segments.append(current_segment)
                        current_segment = []
                else:
                    current_segment.append(pt)

            if current_segment:
                kept_segments.append(current_segment)

            for segment in kept_segments:
                if len(segment) >= 2:
                    updated_strokes.append((color, radius, segment))

        self.strokes = updated_strokes

    def enterEvent(self, event):
        self.mouse_inside = True
        self.update()

    def leaveEvent(self, event):
        self.mouse_inside = False
        self.update()
