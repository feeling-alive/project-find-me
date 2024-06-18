from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from window import InputDialog
import sys
import csv
import pandas as pd
import random

global end_window_reference
end_window_reference = None

#Создание записей
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
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

    def removeRows(self, row, count, parent):
        self.beginRemoveRows(parent, row, row + count - 1)
        self._data = self._data.drop(self._data.index[row:row + count])
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True
#Создание таблицы отображение всех записей в ней так же их удаление
class Scoreboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица лидеров")
        self.index = []
        self.table = QTableView()
        self.setStyleSheet("background-color:#082567;")
        self.data = []

        with open("newlb.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["Name"]
                count = row["Count"]
                self.data.append([name, count])

        for i in range(len(self.data) - 1):
            for j in range(len(self.data) - 1 - i):
                if int(self.data[j][1].strip()) < int(self.data[j + 1][1].strip()):
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]

        for i in range(1, len(self.data) + 1):
            self.index.append(f"{i} место")

        data = pd.DataFrame(self.data, columns=['Имя', 'Очки'], index=self.index)
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.table.setStyleSheet("""
        QTableView {
            background-color: #0d6efd;
            font-size: 15px;
            color: white;
            font-family: "Better VCR";
            selection-background-color: #0b5ed7;
        }
        QHeaderView::section {
            background-color: #0d6efd;
            font-size: 15px;
            color: white;
            font-family: "Better VCR";
            padding: 6px;
            border-bottom: 1px solid #343155;
        }
        QTableView::viewport {
            background-color: #0d6efd;  
        }
        QTableView::cornerButton {
            background-color: #0d6efd;  
        }
        """)

        self.btn_delete = QPushButton("Удалить запись")
        self.btn_delete.setStyleSheet("""
        *{
            background-color:#0d6efd;
            border-radius:10px;
            padding:6px ;
            border:1px solid #343155;  
            color:#fff;
            margin-top:1px;
            font-size:16px;
            font-weight:bold;
            font-family: Better VCR;
        }
        *:hover{
            background-color:#0b5ed7;
            border:1px solid #9ac3fe;
        }
        """)
        self.btn_delete.clicked.connect(self.delete_row)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.btn_delete)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def delete_row(self):
        selected_index = self.table.selectionModel().currentIndex()
        if selected_index.isValid():
            self.model.removeRows(selected_index.row(), 1, selected_index)
            row_to_delete = selected_index.row()

            with open("newlb.csv", "r", encoding="utf-8") as f:
                records = list(csv.DictReader(f))

            with open("newlb.csv", "w", newline='', encoding="utf-8") as f:
                fieldnames = ['Name', 'Count']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for idx, row in enumerate(records):
                    if idx != row_to_delete:
                        writer.writerow(row)

            with open("lb.csv", "r", encoding="utf-8") as f:
                records = list(csv.DictReader(f))

            with open("lb.csv", "w", newline='', encoding="utf-8") as f:
                fieldnames = ['Name', 'Count']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for idx, row in enumerate(records):
                    if idx != row_to_delete:
                        writer.writerow(row)

#Окно с правилами
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
                            "\nПо истечению 5-7 раундов время на таймере \nуменьшится на 15 секунд,"
                            " максимальное время таймера 15 секунд."
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

#Начальное окно с кнопкой старт и кнопкой правила
class Screen1(QMainWindow):
    def __init__(self):
        super(Screen1, self).__init__()
        self.setWindowTitle("Find Me")
        self.setFixedSize(1080, 720)
        self.background_label = QLabel(self)
        self.load_background_image()
        input_dialog = InputDialog()
        input_dialog.show()
        if input_dialog.exec() == QDialog.DialogCode.Accepted:
            self.text = input_dialog.getText()
        else:
            self.text = "Неизвестный пользователь"
        self.button = QPushButton('Старт', self)
        self.button.clicked.connect(self.next_scr)
        self.button.move(420, 470)
        self.button.resize(250, 60)
        self.button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; font-weight: bold; "
                                  "font-size: 20px; font-family: Better VCR")

        self.button_help = QPushButton('?', self)
        self.button_help.pressed.connect(lambda: self.askButtn())
        self.button_help.move(1000, 20)
        self.w = None
        self.button_help.resize(56, 56)
        self.button_help.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 10px; font-weight: bold; "
            "font-size: 20px; font-family: Better VCR")

        self.label = QLabel(self)
        self.label.setGeometry(250, 60, 600, 342)
        movie = QMovie("sprite\ch_startgm.gif")
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
        pixmap = QPixmap("sprite\start2.png").scaled(1080, 720)
        brush = QBrush(pixmap)
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)

        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, pixmap.width(), pixmap.height())
        self.background_label.show()

    def next_scr(self):
        self.hide()
        self.game_window = GameWindow(self.text)  # Создаём экземпляр GameWindow здесь и передаём имя пользователя.
        self.game_window.show()

#Окно игрового процесса
class GameWindow(QMainWindow):
    cp = pyqtSignal(int, int)

    def __init__(self, name):
        super().__init__()
        self.player_name = name
        self.image_paths = ['sprite\ch0.png']
        self.ostch = ['sprite\ch1.png',
                      'sprite\ch2.png',
                      'sprite\ch3.png',
                      'sprite\ch4.png',
                      'sprite\ch5.png',
                      'sprite\ch6.png',
                      'sprite\ch7.png',
                      'sprite\ch8.png',
                      'sprite\ch9.png',
                      'sprite\ch10.png',
                      'sprite\ch11.png',
                      'sprite\ch12.png',
                      'sprite\ch13.png',
                      'sprite\ch14.png',
                      'sprite\ch15.png',
                      'sprite\ch16.png',
                      'sprite\ch17.png',
                      'sprite\ch18.png',
                      'sprite\ch19.png',
                      'sprite\ch20.png',
                      'sprite\ch21.png',
                      'sprite\ch22.png',
                      'sprite\ch23.png',
                      'sprite\ch24.png',
                      'sprite\ch25.png']

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
        pixmap = QPixmap("sprite\dead.png")
        self.dead.setPixmap(pixmap)
        self.dead.resize(180, 60)
        self.dead.move(20, 80)
        self.dc = 0

        self.rounds_played = 0
        self.rounds_to_next_reduction = random.randint(5, 7)

        self.countdown_time = 60
        self.initUI()

    def end_game(self):
        global end_window_reference
        if self.dc == 1:
            self.dead.setPixmap(QPixmap("sprite\dead1.png"))
        if self.dc == 2:
            self.dead.setPixmap(QPixmap("sprite\dead2.png"))
        if self.dc == 3:
            self.dead.setPixmap(QPixmap("sprite\dead3.png"))
            self.close()
            self.timer.stop()
            end_window_reference = EndWindow(self.player_name, self.score_count)
            end_window_reference.show()

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
#Функция добавления очков
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

#Функция таймера
    def update_timer(self):
        global end_window_reference
        if self.timer_started == False:
            self.timer.stop()
        else:
            self.countdown_time -= 1
            self.timer_label.setText(f"{self.countdown_time}")
        if self.countdown_time == 0:
            self.timer.stop()
            self.close()
            end_window_reference = EndWindow(self.player_name, self.score_count)
            end_window_reference.show()

#Функция поска персонажа по клику
    def on_character_clicked(self, x, y):
        if not self.timer_started:
            self.timer_started = True

        index = 0
        search = False

        while index < len(self.characters):
            character = self.characters[index]

            if character.underMouse():
                if character.pixmap().toImage() == QPixmap("sprite\ch0.png").toImage():
                    print(True)
                    self.search = True
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
                    search = True
                    break
                else:
                    if not search:
                        print(False)
                        self.dc += 1
                        self.end_game()
                        search = True
            index += 1


    def timer_rearm(self, countdown_time):
        self.countdown_time = countdown_time
        self.countdown_time -= 1
        self.timer_label.setText(f"{self.countdown_time}")
        if self.countdown_time == 0:
            self.timer.stop()

#Добавление персонажа
    def new_pers(self):
        xc = 525
        yc = 300
        d = 300

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

# Добавление персонажей
    def add_new_characters(self, count):
        xc = 525
        yc = 300
        d = 300

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

#Отслеживание клика мыши и вывод координат
    def mousePressEvent(self, e):
        p = e.pos()
        global_pos = self.mapToGlobal(p)
        print(p.x(), p.y())

        self.cp.emit(p.x(), p.y())


    def load_background_image(self):
        pixmap = QPixmap("sprite\start.png").scaled(1080, 720)
        brush = QBrush(pixmap)
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)

        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, pixmap.width(), pixmap.height())
        self.background_label.show()
#Нахождение границ ромба
    def is_inside_rhombus(self, x, y, xc, yc, d):
        return abs(x - xc) / d + abs(y - yc) / d <= 1

# Добавление персонажа
    def print_heroes(self):
        xc = 525
        yc = 300
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

#Окно окончания с кнопками перезапуск, выход и таблица рекордов
class EndWindow(QMainWindow):
    def __init__(self, player_name, player_score):
        super(EndWindow, self).__init__()
        self.setWindowTitle("Find Me")
        self.a = None
        self.add_to_table(player_name, player_score)
        self.setFixedSize(1080, 720)
        self.background_label = QLabel(self)
        self.load_background_image()
        self.player_name = player_name
        self.player_score = player_score 
        self.rebutton = QPushButton('Перезапуск', self)
        self.rebutton.clicked.connect(self.restart)
        self.rebutton.move(120, 470)
        self.rebutton.resize(250, 60)
        self.rebutton.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; font-weight: bold; "
                                    "font-size: 20px; font-family: Better VCR")

        self.scoreboard_button = QPushButton('Таблица Рекордов', self)
        self.scoreboard_button.move(420, 470)
        self.scoreboard_button.resize(250, 60)
        self.scoreboard_button.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 10px; font-weight: bold; "
            "font-size: 18px; font-family: Better VCR")
        self.scoreboard_button.clicked.connect(self.table)

        self.endbutton = QPushButton('Выход', self)
        self.endbutton.clicked.connect(self.end)
        self.endbutton.move(720, 470)
        self.endbutton.resize(250, 60)
        self.endbutton.setStyleSheet("background-color: red; color: white; border-radius: 10px; font-weight: bold; "
                                     "font-size: 20px; font-family: Better VCR")
        self.label = QLabel(self)
        self.label.setGeometry(250, 60, 600, 342)
        movie = QMovie("sprite\ch_startgm.gif")
        self.label.setMovie(movie)
        movie.start()

    def add_to_table(self, name, count):
        with open("lb.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([name, count])
        file.close()

        with (open("lb.csv", "r", encoding="utf-8") as r,
              open("newlb.csv", "w", encoding="utf-8") as o):
            for line in r:
                if line.strip():
                    o.write(line)
        r.close()
        o.close()

    def table(self):
        if self.a is None:
            self.a = Scoreboard()
            self.a.show()
        else:
            self.a.close()
            self.a = None

    def load_background_image(self):
        pixmap = QPixmap("sprite\start2.png").scaled(1080, 720)
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
        global end_window_reference
        self.close()
        end_window_reference = GameWindow(
            self.player_name)
        end_window_reference.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen1 = Screen1()
    screen1.show()
    sys.exit(app.exec())
