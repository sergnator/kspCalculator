# pip install -r requirements.txt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt

import sys
import traceback

from interface import Ui_MainWindow
from interface2 import Ui_MainWindow_Error
from interface3 import Ui_Form
import kspPlanetsTransphere
import Constans
import WriteAndReadFilesFunctions


class CalculatorKsp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pixmap_icon = QPixmap(Constans.IMAGES + 'KspIcon.png')
        self.Icon.setPixmap(self.pixmap_icon)
        self.fill_combobox()
        self.start_text = ''
        self.end_text = ''
        self.start.currentTextChanged.connect(self.change_start)
        self.End.currentTextChanged.connect(self.change_end)
        self.Calculate.clicked.connect(self.calculate)

    def fill_combobox(self):
        planets = kspPlanetsTransphere.planet_classes()
        planets = list(map(lambda x: x.returnname(), planets))[1:]
        self.start.addItems(planets)
        self.End.addItems(planets)

    def calculate(self):
        palette = QPalette()
        color = palette.color(QPalette.Window)
        self.Angel.setText(
            str(round(float(kspPlanetsTransphere.create_angle(self.start_text, self.end_text)), 1)) + '°')
        self.Image.setPixmap(
            QPixmap(kspPlanetsTransphere.draw_angle(self.start_text, self.end_text, width=self.Image.width(),
                                                    height=self.Image.height(), color=color.rgb())))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter - 1:
            self.calculate()

    def change_start(self, text):
        self.start_text = text

    def change_end(self, text):
        self.end_text = text

    def error_message(self):
        dialog = MyDialog(self)
        dialog.show()
        result = dialog.exec_()
        return result


# окно ошибки
class MyDialog(QDialog, Ui_MainWindow_Error):
    def __init__(self, window=None):
        super().__init__(window)
        self.setupUi(self)
        self.Yes.clicked.connect(self.accept)
        self.No.clicked.connect(self.reject)


class DialogAddPlanet(QDialog, Ui_Form):
    def __init__(self, window=None):
        super().__init__(window)
        self.save.clicked.connect(self.save_func)

    def save_func(self):
        if any(map(lambda x: x no))
        return [self.accept()] + [self.name, self.acceleration, self.atmoph, self.second_space_speed, self.color,
                                  self.alt]


def except_hook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    WriteAndReadFilesFunctions.write_exception(tb)
    res = ex.error_message()
    if res == Constans.OK_RESULT:
        sys.exit()


sys.excepthook = except_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalculatorKsp()
    ex.show()
    sys.exit(app.exec_())
