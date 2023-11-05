# pip install -r requirements.txt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QColorDialog, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QPoint
import qdarktheme

import sys
import traceback
from random import randint
import math

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
        self.first = ''
        self.second = ''

    def map(self):
        dialog = DialogMapPlanets(self)
        dialog.setModal(True)
        dialog.show()

    def fill_combobox(self):
        planets = kspPlanetsTransphere.planet_classes()
        planets = list(map(str, planets))[1:]
        self.start.addItems(planets)
        self.End.addItems(planets)

    def calculate(self, flag=False):
        first = self.start_text
        second = self.end_text
        if flag:
            first = self.first
            second = self.second
        valid(first)
        valid(second)
        color = (248, 249, 250)
        color_text = (0, 0, 0)
        if self.dark:
            color = (32, 33, 36)
            color_text = (255, 255, 255)
        self.Angel.setText(
            str(round(float(kspPlanetsTransphere.create_angle(first, second)), 1)) + '°')
        self.Image.setPixmap(
            QPixmap(kspPlanetsTransphere.draw_angle(first, second, width=self.Image.width(),
                                                    height=self.Image.height(), color=color, color_text=color_text)))
        self.first = first
        self.second = second

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter - 1:
            self.calculate()

    def change_start(self, text):
        self.start_text = text

    def change_end(self, text):
        self.end_text = text

    def error_message(self, text=None, flag=False):
        if flag:
            dialog = ErrorCriticalDialog(self)
            dialog.show()
            result = dialog.exec_()
        else:
            dialog = ErrorMessage(text, window=self)
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
            self.calculate(flag=True)
        except ExceptionGroupKSP:
            pass


# окна ошибки
class ErrorCriticalDialog(QDialog, Ui_MainWindow_Error):
    def __init__(self, window=None):
        super().__init__(window)
        self.setupUi(self)
        self.Yes.clicked.connect(self.accept)
        self.No.clicked.connect(self.reject)
        self.setModal(True)


class ErrorMessage(QDialog):
    def __init__(self, message, window=None):
        super().__init__(window)
        self.message = message
        self.set_ui()

    def set_ui(self):
        self.setModal(True)
        self.resize(500, 200)
        self.label = QLabel(self)
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setText(self.message)
        self.label.setScaledContents(True)
        self.label.move(150, 50)
        self.but = QPushButton(self)
        self.but.setText('ok')
        self.but.move(250, 150)
        self.but.setFont(font)
        self.but.clicked.connect(self.accept)


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

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp: QPainter):
        height = 1000
        width = 1000
        color = (248, 249, 250)
        color_text = (0, 0, 0)

        if self.window_main.dark:
            color = (32, 33, 36)
            color_text = (255, 255, 255)

        planets = WriteAndReadFilesFunctions.planet_classes()[1:]
        planets1 = []
        for planet in planets:
            if planet.parent == 0:
                planets1.append(planet)

        planets = planets1[:]
        planets = sorted(planets, key=lambda x: x.alt)
        qp.setBrush(QColor(*color))
        pen_black = QPen()
        pen_black.setColor(QColor(*color_text))
        qp.setPen(pen_black)
        pen_light = QPen()
        pen_light.setBrush(QColor(*color))

        i = 0.4 * width / len(planets)
        b = 0.9 * width / 2

        center = QPoint(500, 500)

        for j in range(len(planets), 0, -1):
            qp.setPen(pen_black)
            qp.setBrush(QColor(*color))
            # орбита
            qp.drawEllipse(center, b, b)

            # планета
            angle = randint(0, 360)
            x0 = int(0.5 * width)
            y0 = int(0.5 * height)
            x = int(x0 + b * -math.cos(math.radians(angle)))
            y = int(y0 + b * math.sin(math.radians(angle)))

            qp.setPen(pen_light)
            qp.setBrush(QColor(planets[j - 1].color))
            qp.drawEllipse(QPoint(x, y), 25, 25)
            b -= i
            # текст
            qp.setPen(pen_black)
            qp.drawText(QPoint(x - 15, y + 35), planets[j - 1].name)
        # Kerbol
        qp.setPen(pen_light)
        qp.setBrush(QColor('yellow'))
        qp.drawEllipse(center, 50, 50)
        qp.setPen(pen_black)
        qp.drawText(QPoint(500 - 15, 500 + 65), 'Kerbol')


def except_hook(exc_type, exc_value, exc_tb):
    if not issubclass(exc_type, ExceptionGroupKSP):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        WriteAndReadFilesFunctions.write_exception(tb)
        res = ex.error_message(flag=True)
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
