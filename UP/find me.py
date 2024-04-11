from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QApplication, QGridLayout
from PyQt6.QtGui import QPixmap, QBrush, QPalette
from PyQt6.QtCore import Qt
import sys
import random, pyautogui, cv2, difflib, mouse

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
#спавн дебиков
class Search:
    image_paths = ['ch0.png', 'ch1.png', 'ch2.png']

    def CalcImageHash(self, FileName):
        image = cv2.imread(FileName)
        resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        avg = gray_image.mean()
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)

        _hash = ""
        for x in range(8):
            for y in range(8):
                val = threshold_image[x, y]
                if val == 255:
                    _hash += "1"
                else:
                    _hash += "0"

        return _hash

    def run(self):
        chel_alg = [self.CalcImageHash("ch0.png")]
        osthash = [self.CalcImageHash(image) for image in self.image_paths]
#двоичный код картинок
    def mouse(self):
        x = 0
        y = 0
        for _ in range(3):
                if mouse.is_pressed(button='left'):
                    x, y = mouse.get_position()
                    print(f"Mouse clicked at: X={x}, Y={y}")
#ничтожная попытка получить координаты
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    search = Search()
    search.run()
    search.mouse()
    sys.exit(app.exec())