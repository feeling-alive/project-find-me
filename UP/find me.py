from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from window import InputDialog
import sys
import csv
import pandas as pd
import random


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])


class Scoreboard(QMainWindow):
    def __init__(self):
        super().__init__()
        input_dialog = InputDialog()
        input_dialog.show()
        if input_dialog.exec() == QDialog.DialogCode.Accepted:
            self.text = input_dialog.getText()
        else:
            self.text = "Неизвестный пользователь"

        menu_bar = self.menuBar()
        score = menu_bar.addAction("Таблица")
        score.triggered.connect(self.table)

        self.setStatusBar(QStatusBar(self))

        menu_bar.setStyleSheet("""
               *{
               background-color:white;
               font-size:13px;
               font-color:#343155;
               font-weight:bold;
               }
               """)

        pageLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout(self)
        self.outerLayout = QHBoxLayout(self)
        self.frame = QFrame()
        self.frame.setStyleSheet("""
                   border-width: 6px;
                   border-height: 10px;
                   border-radius:4px;
                   font-size:20px;
                   font-weight:bold;
                   color: #F8F8FF;
               """)
        self.setWindowTitle("Таблица лидеров")
        self.index = []
        self.table = QTableView()
        self.data = []
        self.setFixedWidth(254)

        with open("newlb.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["Name"]
                count = row["Count"]
                self.data.append([name, count])

        for i in range(len(self.data) - 1):
            for j in range(len(self.data) - 1 - i):
                if int(self.data[j][1]) < int(self.data[j + 1][1]):
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]

        for i in range(1, len(self.data) + 1):
            self.index.append(f"{i} место")
        data = pd.DataFrame(self.data,
                            columns=['Имя', 'Очки'], index=self.index
                            )
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

    def table(self):
        if self.a is None:
            self.a = Scoreboard()
            self.a.show()
        else:
            self.a.close()
            self.a = None


class helpWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle("Правила")
        self.label = QLabel("В начале игры искомый персонаж появляется на поле."
                            "\nИгрок должен найти заданного персонажа \nсреди других персонажей на клетчатом поле, "
                            "используя критерии, заданные в начале игры."
                            "\nИгрок имеет ограниченное количество времени \nи попыток для нахождения персонажа. "
                            "\nЕсли игрок находит персонажа, он получает очки \nи продвигается на следующий уровень. "
                            "\nС каждым уровнем количество различных персонажей \nна поле увеличивается, они могут быть"
                            " одинаковыми, "
                            " искомый персонаж остаётся неизменным."
                            "\nПо истечению определённого колличества раундов время \nна таймере уменьшится на 15 секунд,"
                            " минимальное время таймера 15 секунд."
                            "\nЗа каждое правильное нахождение игрок получает баллы, \nчем меньше максимальное время"
                            " таймера, тем больше очков игрок получит. "
                            "\nИгра завершится по истечению времени \nили по окончанию попыток на нахождение "
                            "нужного персонажа.")
        self.label.setStyleSheet("font-size: 12pt; color: black; font-family: Better VCR")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setStyleSheet("background-image: url('help.png'); background-position: cover;")

        self.setLayout(layout)


class Screen1(QMainWindow):
    def __init__(self):
        super(Screen1, self).__init__()
        self.setWindowTitle("Find Me")
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
        movie = QMovie("C:/Users\Никита\PycharmProjects/UP\sprite\ch_startgm.gif")
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
        pixmap = QPixmap("C:/Users\Никита\PycharmProjects/UP\sprite\start2.png").scaled(1080, 720)
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

        self.image_paths = ['C:/Users\Никита\PycharmProjects/UP\sprite\ch0.png']
        self.ostch = ['C:/Users\Никита\PycharmProjects/UP\sprite\ch1.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch2.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch3.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch4.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch5.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch6.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch7.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch8.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch9.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch10.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch11.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch12.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch13.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch14.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch15.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch16.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch17.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch18.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch19.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch20.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch21.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch22.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch23.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch24.png',
                      'C:/Users\Никита\PycharmProjects/UP\sprite\ch25.png']

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
        self.score_count = 000000
        self.score_end = 0

        self.dead = QLabel(self)
        pixmap = QPixmap("C:/Users\Никита\PycharmProjects/UP\sprite\dead.png")
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
            self.dead.setPixmap(QPixmap("C:/Users\Никита\PycharmProjects/UP\sprite\dead1.png"))
        if self.dc == 2:
            self.dead.setPixmap(QPixmap("C:/Users\Никита\PycharmProjects/UP\sprite\dead2.png"))
        if self.dc == 3:
            self.dead.setPixmap(QPixmap("C:/Users\Никита\PycharmProjects/UP\sprite\dead3.png"))
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
        self.timer.stop()

    def score_up(self):
        if self.time_uper == 60:
            self.score_count += 100
        if self.time_uper == 45:
            self.score_count += 200
        if self.time_uper == 30:
            self.score_count += 300
        if self.time_uper == 15:
            self.score_count += 400
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
                if character.pixmap().toImage() == QPixmap(
                        "C:/Users\Никита\PycharmProjects/UP\sprite\ch0.png").toImage():
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
                    self.dc += 1
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
        pixmap = QPixmap("C:/Users\Никита\PycharmProjects/UP\sprite\start.png").scaled(1080, 720)
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

        for i, image_path in enumerate(self.image_paths):
            pixmap = QPixmap(image_path)
            character_label = QLabel(self)
            character_label.setPixmap(pixmap)
            character_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

            x = xc
            y = yc if i == 0 else random.randint(xc - d, xc + d)
            while not self.is_inside_rhombus(x, y, xc, yc, d):
                x, y = random.randint(xc - d, xc + d), random.randint(yc - d, yc + d)

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

        self.scoreboard_button = QPushButton('Таблица Рекордов', self)
        self.scoreboard_button.clicked.connect(self.show_scoreboard)
        self.scoreboard_button.move(420, 470)  # Вы должны указать правильные координаты
        self.scoreboard_button.resize(250, 60)
        self.scoreboard_button.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 10px; font-weight: bold; font-size: 20px;")
        self.scoreboard_button.clicked.connect(self.show_scoreboard)

        self.endbutton = QPushButton('Выход', self)
        self.endbutton.clicked.connect(self.end)
        self.endbutton.move(620, 470)
        self.endbutton.resize(250, 60)
        self.endbutton.setStyleSheet("background-color: red; color: white; border-radius: 10px; font-weight: bold; "
                                     "font-size: 20px; font-family: Better VCR")
        self.label = QLabel(self)
        self.label.setGeometry(250, 60, 600, 342)
        movie = QMovie("C:/Users\Никита\PycharmProjects/UP\sprite\ch_startgm.gif")
        self.label.setMovie(movie)
        movie.start()

    def show_scoreboard(self):
        self.scoreboard_window = Scoreboard()
        self.scoreboard_window.show()

    def load_background_image(self):
        pixmap = QPixmap("C:/Users\Никита\PycharmProjects/UP\sprite\start2.png").scaled(1080, 720)
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

    scoreboard = Scoreboard()
    scoreboard.show()

    screen1 = Screen1()
    game_window = GameWindow()
    end_window = EndWindow()
    screen1.show()

    sys.exit(app.exec())
