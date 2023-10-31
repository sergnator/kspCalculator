from interface import Ui_MainWindow
from interface2 import Ui_MainWindow_Error
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import QPixmap, QPalette
import sys
import kspPlanetsTransphere
import Constans
import WriteAndReadFilesFunctions
import traceback


class CalculatorKsp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pixmapicon = QPixmap(Constans.IMAGES + 'KspIcon.png')
        self.Icon.setPixmap(self.pixmapicon)
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

    def change_start(self, text):
        self.start_text = text

    def change_end(self, text):
        self.end_text = text

    def ErrorMessage(self):
        dialog = MyDialog(self)
        dialog.show()
        result = dialog.exec_()
        return result


class MyDialog(QDialog, Ui_MainWindow_Error):
    def __init__(self, window=None):
        super().__init__(window)
        self.setupUi(self)
        self.Yes.clicked.connect(self.accept)
        self.No.clicked.connect(self.reject)


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    WriteAndReadFilesFunctions.write_exception(tb)
    res = ex.ErrorMessage()
    print(res)
    if res == 1:
        sys.exit()



sys.excepthook = excepthook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalculatorKsp()
    ex.show()
    sys.exit(app.exec_())
