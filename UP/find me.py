from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QApplication, QGridLayout
from PyQt6.QtGui import QPixmap, QBrush, QPalette
from PyQt6.QtCore import Qt
import sys
import random


class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Find Me")
        self.setFixedSize(1080, 720)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.grid = QGridLayout(central_widget)

        self.image_paths = ['ch0.png', 'ch1.png', 'ch2.png']

        self.background_label = QLabel(self)


        self.load_background_image()

        self.characters = []
        self.print_heroes()


    def load_background_image(self):
        pixmap = QPixmap("start.png").scaled(1080, 720)
        brush = QBrush(pixmap)
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)

        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, pixmap.width(), pixmap.height())
        self.background_label.show()

    def is_inside_rhombus(self, x, y, xc, yc, d):
        return abs(x - xc) / d + abs(y - yc) / d <= 1

    def print_heroes(self):
        xc = 530
        yc = 250
        d = 350

        for i, image_path in enumerate(self.image_paths):
            pixmap = QPixmap(image_path)
            character_label = QLabel(self)
            character_label.setPixmap(pixmap)
            character_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

            x, y = random.randint(xc - d, xc + d), random.randint(yc - d, yc + d)
            while not self.is_inside_rhombus(x, y, xc, yc, d):
                x, y = random.randint(xc - d, xc + d), random.randint(yc - d, yc + d)

            character_label.move(x, y)
            character_label.show()
            self.characters.append(character_label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())