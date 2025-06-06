# app.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from gui.canvas_widget import CanvasWidget
from gui.color_palette import ColorPaletteWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photoshop Clone - PyQt")
        self.setFixedSize(512, 560)

        self.canvas = CanvasWidget()
        self.setCentralWidget(self.canvas)

        self.palette_window = ColorPaletteWindow()
        self.palette_window.color_selected.connect(self.canvas.set_brush_color)

        # I 키 눌렀을 때 팔레트 창 보이기 버튼 (개발용으로 배치)
        self.palette_btn = QPushButton("🎨 색상 선택창 열기 (I)", self)
        self.palette_btn.move(10, 520)
        self.palette_btn.clicked.connect(self.toggle_palette)

    def keyPressEvent(self, event):
        if event.key() == ord('I'):
            self.toggle_palette()

    def toggle_palette(self):
        if self.palette_window.isVisible():
            self.palette_window.hide()
        else:
            self.palette_window.show()

# if __name__ == "__main__":
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
