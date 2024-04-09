from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QApplication, QGridLayout
from PyQt6.QtGui import QPixmap, QBrush, QPalette
from PyQt6.QtCore import Qt
import sys

class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Find Me")
        self.setFixedSize(1080, 720)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.grid = QGridLayout(central_widget)

        pixmap2 = QPixmap("chel1.png").scaled(350, 200)
        self.character_label1 = QLabel()
        self.character_label1.setPixmap(pixmap2)
        self.character_label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.character_label1, 0, 0)

        self.load_background_image()

    def load_background_image(self):
        pixmap = QPixmap("start.png").scaled(1080, 720)
        brush = QBrush(pixmap)
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
