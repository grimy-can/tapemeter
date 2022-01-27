from PyQt5 import QtWidgets, QtGui, QtCore
from qlabel import Ui_MainWindow
import sys


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label.setFont(QtGui.QFont('SansSerif', 30))
        # Изменение шрифта и размера
        self.ui.label.setGeometry(
            QtCore.QRect(10, 10, 300, 100))
        # изменить геометрию ярлыка
        self.ui.label.setText("Tapemeter")  # Меняем текст


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
