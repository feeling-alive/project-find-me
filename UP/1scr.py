from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QApplication, QGridLayout, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPixmap, QBrush, QPalette, QCursor, QMovie
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QTime, QAbstractTableModel
import sys
from window import InputDialog
import random


class helpWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle("Правила")
        self.label = QLabel("В начале игры искомый персонаж появляется на поле."
                            "\nИгрок должен найти заданного персонажа среди других персонажей на клетчатом поле, "
                            "используя критерии, заданные в начале игры."
                            "\nИгрок имеет ограниченное количество времени и попыток для нахождения персонажа. "
                            "\nЕсли игрок находит персонажа, он получает очки и продвигается на следующий уровень. "
                            "\nС каждым уровнем количество различных персонажей на поле увеличивается, они могут быть"
                            "одинаковыми, "
                            "искомый персонаж остаётся неизменным."
                            "\nПо истечению определённого колличества раундов время на таймере уменьшится на 15 секунд,"
                            "минимальное время таймера 15 секунд."
                            "\nЗа каждое правильное нахождение игрок получает баллы, чем меньше максимальное время"
                            "таймера тем больше очков игрок получит. "
                            "\nИгра завершится по истечению времени или по окончанию попыток на нахождение "
                            "нужного персонажа .")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label.setStyleSheet("""
        font-size:15px;
        """)
        layout.addWidget(self.label)
        self.setLayout(layout)


class Screen1(QMainWindow):
    def __init__(self):
        super(Screen1, self).__init__()
        self.setWindowTitle("Find Met")
        self.setFixedSize(1080, 720)
        self.background_label = QLabel(self)
        self.load_background_image()
        self.button = QPushButton('Старт', self)
        self.button.clicked.connect(self.next_scr)
        self.button.move(420, 470)
        self.button.resize(250, 60)
        self.button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; font-weight: bold; "
                                  "font-size: 20px;")

        self.button_help = QPushButton('?', self)
        self.button_help.pressed.connect(lambda: self.askButtn())
        self.button_help.move(1000, 20)
        self.w = None
        self.button_help.resize(56, 56)
        self.button_help.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 10px; font-weight: bold; "
            "font-size: 20px;")

        self.label = QLabel(self)
        self.label.setGeometry(250, 60, 600, 342)
        movie = QMovie("ch_startgm.gif")
        self.label.setMovie(movie)
        movie.start()

    def askButtn(self):
        if self.w is None:
            self.w = helpWindow()
            self.w.show()
        else:
            self.w.close()
            self.w = None

    def load_background_image(self):
        pixmap = QPixmap("start2.png").scaled(1080, 720)
        brush = QBrush(pixmap)
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)

        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, pixmap.width(), pixmap.height())
        self.background_label.show()

    def next_scr(self):
        self.hide()
        game_window.show()

class GameWindow(QMainWindow):
    cp = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

        self.image_paths = ['ch0.png']
        self.ostch = ['ch1.png', 'ch2.png', 'ch3.png', 'ch4.png', 'ch5.png', 'ch6.png', 'ch7.png', 'ch8.png', 'ch9.png'
            , 'ch10.png', 'ch11.png', 'ch12.png', 'ch13.png', 'ch14.png', 'ch15.png', 'ch16.png', 'ch17.png',
                      'ch18.png', 'ch19.png', 'ch20.png', 'ch21.png', 'ch22.png', 'ch23.png', 'ch24.png', 'ch25.png']
        self.background_label = QLabel(self)
        self.characters = []

        self.timer_label = QLabel(self)
        self.timer_label.move(25, 5)
        self.timer_label.resize(200, 100)
        self.timer_label.setStyleSheet("font-size: 25pt; color: black; font-family: Better VCR")
        self.time_uper = 60
        self.timer_label.setText("60")
        self.timer_started = False

        self.score = QLabel(self)
        self.score.move(900, 5)
        self.score.resize(200, 100)
        self.score.setStyleSheet("font-size: 25pt; color: black; font-family: Better VCR")
        self.score.setText('000000')
        self.score_count =  000000

        self.dead = QLabel(self)
        pixmap = QPixmap("dead.png")
        self.dead.setPixmap(pixmap)
        self.dead.resize(180, 60)
        self.dead.move(20, 80)
        self.dc = 0

        self.rounds_played = 0
        self.rounds_to_next_reduction = random.randint(5, 7)

        self.countdown_time = 60
        self.initUI()

    def end_game(self):
        if self.dc == 1:
            self.dead.setPixmap(QPixmap("dead1.png"))
        if self.dc == 2:
            self.dead.setPixmap(QPixmap("dead2.png"))
        if self.dc == 3:
            self.dead.setPixmap(QPixmap("dead3.png"))
            self.close()
            end_window.show()
            self.timer.stop()

    def initUI(self):
        self.setWindowTitle("Find Me")
        self.setFixedSize(1080, 720)
        self.load_background_image()
        self.print_heroes()
        self.cp.connect(self.on_character_clicked)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)


    def score_up(self):
        if self.time_uper == 60:
            self.score_count +=100
        if self.time_uper == 45:
            self.score_count +=200
        if self.time_uper == 30:
            self.score_count +=300
        if self.time_uper == 15:
            self.score_count +=400
        self.score.setText(f"{self.score_count:06}")

    def update_timer(self):
        if self.timer_started == False:
            self.timer.stop()
        else:
            self.countdown_time -= 1
            self.timer_label.setText(f"{self.countdown_time}")
        if self.countdown_time == 0:
            self.timer.stop()
            self.close()
            end_window.show()

    def on_character_clicked(self, x, y):
        if not self.timer_started:
            self.timer_started = True
        for character in self.characters:
            if character.underMouse():
                if character.pixmap().toImage() == QPixmap("ch0.png").toImage():
                    print(True)
                    self.characters.remove(character)
                    character.hide()
                    new_characters_count = random.randint(3, 5)
                    self.rounds_played += 1
                    self.add_new_characters(new_characters_count)
                    self.countdown_time = self.time_uper
                    self.timer_label.setText(f"{self.countdown_time}")
                    self.timer.start()
                    self.score_up()
                    if self.rounds_played == self.rounds_to_next_reduction:
                        if self.time_uper > 15:
                            self.time_uper -= 15
                            self.timer_label.setText(f"{self.countdown_time}")
                            self.rounds_played = 0
                            self.rounds_to_next_reduction = random.randint(5, 7)
                else:
                    print(False)
                    self.dc +=1
                    self.end_game()

    def timer_rearm(self, countdown_time):
        self.countdown_time = countdown_time
        self.countdown_time -= 1
        self.timer_label.setText(f"{self.countdown_time}")
        if self.countdown_time == 0:
            self.timer.stop()

    def new_pers(self):
        xc = 520
        yc = 260
        d = 290

        for _ in range(1):
            pixmap = QPixmap(random.choice(self.image_paths))
            character_label = QLabel(self)
            character_label.setPixmap(pixmap)
            character_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

            x, y = random.randint(xc - d, xc + d), random.randint(yc - d, yc + d)
            while not self.is_inside_rhombus(x, y, xc, yc, d):
                x, y = random.randint(xc - d, xc + d), random.randint(yc - d, yc + d)

            character_label.move(x, y)
            character_label.show()
            self.characters.append(character_label)

    def add_new_characters(self, count):
        xc = 520
        yc = 260
        d = 290

        for _ in range(count):
            pixmap = QPixmap(random.choice(self.ostch))
            character_label = QLabel(self)
            character_label.setPixmap(pixmap)
            character_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

            x, y = random.randint(xc - d, xc + d), random.randint(yc - d, yc + d)
            while not self.is_inside_rhombus(x, y, xc, yc, d):
                x, y = random.randint(xc - d, xc + d), random.randint(yc - d, yc + d)

            character_label.move(x, y)
            character_label.show()
            self.characters.append(character_label)
        self.new_pers()

    def mousePressEvent(self, e):
        p = e.pos()
        global_pos = self.mapToGlobal(p)
        print(p.x(), p.y())

        self.cp.emit(p.x(), p.y())

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
        xc = 520
        yc = 260
        d = 300
        pastuh = []

        for i, image_path in enumerate(self.image_paths):
            pixmap = QPixmap(image_path)
            character_label = QLabel(self)
            character_label.setPixmap(pixmap)
            character_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

            x = xc
            y = yc if i == 0 else random.randint(xc - d, xc + d)
            while not self.is_inside_rhombus(x, y, xc, yc, d):
                x, y = random.randint(xc - d, xc + d), random.randint(yc - d, yc + d)


            pastuh.append(x)
            pastuh.append(y)
            print(pastuh)
            character_label.move(x, y)
            character_label.show()
            self.characters.append(character_label)

class EndWindow(QMainWindow):
    def __init__(self):
        super(EndWindow, self).__init__()
        self.setWindowTitle("Find Me")
        self.setFixedSize(1080, 720)
        self.background_label = QLabel(self)
        self.load_background_image()
        self.rebutton = QPushButton('Перезапуск', self)
        self.rebutton.clicked.connect(self.restart)
        self.rebutton.move(220, 470)
        self.rebutton.resize(250, 60)
        self.rebutton.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; font-weight: bold; "
                                    "font-size: 20px; font-family: Better VCR")
        self.endbutton = QPushButton('Выход', self)
        self.endbutton.clicked.connect(self.end)
        self.endbutton.move(620, 470)
        self.endbutton.resize(250, 60)
        self.endbutton.setStyleSheet("background-color: red; color: white; border-radius: 10px; font-weight: bold; "
                                     "font-size: 20px; font-family: Better VCR")
        self.label = QLabel(self)
        self.label.setGeometry(250, 60, 600, 342)
        movie = QMovie("ch_startgm.gif")
        self.label.setMovie(movie)
        movie.start()

    def load_background_image(self):
        pixmap = QPixmap("start2.png").scaled(1080, 720)
        brush = QBrush(pixmap)
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)

        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, pixmap.width(), pixmap.height())
        self.background_label.show()

    def end(self):
        exit()

    def restart(self):
        global game_window
        game_window.close()
        game_window = GameWindow()
        game_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    screen1 = Screen1()
    game_window = GameWindow()
    end_window = EndWindow()

    screen1.show()

    sys.exit(app.exec())
