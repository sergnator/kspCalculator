# pip install -r requirements.txt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QColorDialog, QLabel
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor
from PyQt5.QtCore import Qt, QPoint
import qdarktheme

import sys
import traceback

from interface import Ui_MainWindow
from interface2 import Ui_MainWindow_Error
from interface3 import Ui_Form
import kspPlanetsTransphere
from Constans import *
import WriteAndReadFilesFunctions
from MainClasses import *


class CalculatorKsp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.root()
        qdarktheme.setup_theme('light')

    def root(self):
        self.pixmap_icon = QPixmap(IMAGES + 'KspIcon.png')
        self.Icon.setPixmap(self.pixmap_icon)
        self.fill_combobox()
        self.start_text = ''
        self.end_text = ''
        self.start.currentTextChanged.connect(self.change_start)
        self.End.currentTextChanged.connect(self.change_end)
        self.Calculate.clicked.connect(self.calculate)
        self.addBut.clicked.connect(self.add_planet)
        self.dark = False
        self.darkTheme.clicked.connect(self.theme_change)
        self.darkTheme.setIcon(QIcon(QPixmap(IMAGES + 'icon-light.png')))
        self.map_but.clicked.connect(self.map)

    def map(self):
        dialog = DialogMapPlanets(self)
        dialog.setModal(True)
        dialog.show()

    def fill_combobox(self):
        planets = kspPlanetsTransphere.planet_classes()
        planets = list(map(str, planets))[1:]
        self.start.addItems(planets)
        self.End.addItems(planets)

    def calculate(self):
        valid(self.start_text)
        valid(self.end_text)
        color = (248, 249, 250)
        color_text = (0, 0, 0)
        if self.dark:
            color = (32, 33, 36)
            color_text = (255, 255, 255)
        self.Angel.setText(
            str(round(float(kspPlanetsTransphere.create_angle(self.start_text, self.end_text)), 1)) + '°')
        self.Image.setPixmap(
            QPixmap(kspPlanetsTransphere.draw_angle(self.start_text, self.end_text, width=self.Image.width(),
                                                    height=self.Image.height(), color=color, color_text=color_text)))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter - 1:
            self.calculate()

    def change_start(self, text):
        self.start_text = text

    def change_end(self, text):
        self.end_text = text

    def error_message(self, text=None):
        if text is not None:
            dialog = MyDialog(self, text)
        else:
            dialog = MyDialog(self)
        dialog.show()
        result = dialog.exec_()
        return result

    def add_planet(self):
        dialog = DialogAddPlanet(self)
        dialog.show()
        res = dialog.exec_()
        if res != BAD_RESULT:
            res = dialog.param
            WriteAndReadFilesFunctions.add_obj_in_database(DATABASE + 'planets.db', res, (
                'name', 'g', 'atmosphere', 'secondSpaceSpeed', 'color', 'alt'))

    def theme_change(self):
        if self.dark:
            qdarktheme.setup_theme('light')
            self.darkTheme.setIcon(QIcon(QPixmap(IMAGES + 'icon-light.png')))
        else:
            qdarktheme.setup_theme('dark')
            self.darkTheme.setIcon(QIcon(QPixmap(IMAGES + 'icon-dark.png')))
        self.dark = not self.dark
        try:
            self.calculate()
        except Exception:
            pass


# окно ошибки
class MyDialog(QDialog, Ui_MainWindow_Error):
    def __init__(self, window=None, text=None):
        super().__init__(window)
        self.setupUi(self)
        if text is not None:
            self.label.setText(text)
        self.Yes.clicked.connect(self.accept)
        self.No.clicked.connect(self.reject)
        self.setModal(True)


class DialogAddPlanet(QDialog, Ui_Form):
    def __init__(self, window=None):
        super().__init__(window)
        self.setupUi(self)
        self.saveBut.clicked.connect(self.save_func)
        self.cancel.clicked.connect(self.reject)
        self.color = ''
        self.color_button.clicked.connect(self.choice_color)
        self.Icon.setPixmap(QPixmap(IMAGES + 'KspIcon.png'))

    def save_func(self):
        param = (self.name.text(), self.acceleration.text(), self.atmoph.isChecked(), self.second_space_speed.text(),
                 self.color, self.alt.text())
        for i in param:
            valid(i)
        self.param = param
        self.accept()

    def choice_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_button.setStyleSheet(f'background-color: {color.value()}')
            self.color = color.rgb()


class DialogMapPlanets(QDialog):
    def __init__(self, window=None):
        super().__init__(window)
        self.window_main = window
        self.setGeometry(150, 100, 1000, 1000)
        self.x = 1000
        self.y = 1000
        self.label = QLabel(self)
        self.resize(1000, 1000)
        self.move(0, 0)
        self.draw()

    def draw(self):
        color = (248, 249, 250)
        color_text = (0, 0, 0)
        if self.window_main.dark:
            color = (32, 33, 36)
            color_text = (255, 255, 255)

        self.label.setPixmap(kspPlanetsTransphere.draw_map(color=color, color_text=color_text))


def except_hook(exc_type, exc_value, exc_tb):
    if not issubclass(exc_type, ExceptionGroupKSP):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        WriteAndReadFilesFunctions.write_exception(tb)
        res = ex.error_message()
        if res == OK_RESULT:
            sys.exit()

    else:
        ex.error_message(exc_value.message)


sys.excepthook = except_hook


def valid(str_: str):
    if str_ is None or str_ == '':
        raise NoAnyoneSelect('нужно заполнить все поля')
    if isinstance(str_, str):
        if str_.isdigit():
            if int(str_) < 0:
                raise NegativeValue("число в поле не может быть отрицательным")


if __name__ == '__main__':
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    app.setStyleSheet("""QComboBox {
    border: 1px solid gray;
    border-radius: 3px;
    min-width: 6em;
}""")
    ex = CalculatorKsp()
    ex.show()
    sys.exit(app.exec_())
