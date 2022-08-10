from PyQt5.QtWidgets import *
import sys
from PyQt5 import uic
from math import *
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# ui_file = "./calculator.ui"
ui_file = resource_path("./calculator.ui")


class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(ui_file, self)
        self.equalButton.clicked.connect(self.calculate)
        self.deleteButton.clicked.connect(self.outputBox.clear)

    def calculate(self):
        user_input = self.inputBox.text().strip()
        self.inputBox.clear()
        try:
            result = eval(user_input)
            self.outputBox.append(f"{user_input}\n = {result}\n")
        except NameError:
            result = "Error!!"
            self.outputBox.append(f"Error!!")


# Theme Setting
QApplication.setStyle("fusion")

app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())

# pyinstaller --onefile --noconsole ./21-GUI개발-공학용계산기.py
# pyinstaller ./21-GUI개발-공학용계산기.spec
