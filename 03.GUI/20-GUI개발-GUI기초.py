from PyQt5.QtWidgets import *
import sys
from PyQt5 import uic

ui_file = "./test.ui"


class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(ui_file, self)
        self.button.clicked.connect(self.show_string)
        self.deleteButton.clicked.connect(self.delete_string)

    def show_string(self):
        user_input = self.inputBox.text()
        self.inputBox.clear()
        self.outputBox.append(user_input)

    def delete_string(self):
        self.outputBox.clear()

# Theme Setting
QApplication.setStyle("fusion")

app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())