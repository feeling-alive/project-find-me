import sys

from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton


class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 150)
        self.setWindowTitle("Регистрация")
        self.setStyleSheet("background-color:#082567;")
        layout = QVBoxLayout()

        self.label = QLabel("Введите ваше имя:")
        layout.addWidget(self.label)
        self.label.setStyleSheet("""
        font-size:15px;
        color:white;
        font-family: Better VCR;
        """)

        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)
        self.text_input.setStyleSheet("""
        *{
            background-color:#082567;
            border-radius:14px;
            padding:5px 0;
            border:1px solid #082567;	
            color:#fff;
            font-size:16 px;
            font-family: Better VCR;
        }
        *:focus{
            border:1px solid #8b86aa;
            background-color:#343155;
        }
        """)

        ok_button = QPushButton("ОК")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        ok_button.setStyleSheet("""
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

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)
        cancel_button.setStyleSheet("""
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

        self.setLayout(layout)
    def getText(self):
        self.text = self.text_input.text().replace(" ", "")
        if len(self.text) == 0:
            sys.exit(0)
        return self.text


if __name__ == "__main__":
    app = QApplication([])

    input_dialog = InputDialog()
    if input_dialog.exec() == QDialog.DialogCode.Accepted:
        text = input_dialog.getText()
        print(text)

    app.exec()
