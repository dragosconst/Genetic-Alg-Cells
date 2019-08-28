# This is the main program source file.

# here we import standard libraries\modules
import sys

# here we import third party libraries\modules
from PyQt5 import QtCore, QtGui, QtWidgets

# here we import local modules
from GUI import MainWindow as mw

class MLCellApp(mw.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self): 
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__': # yeah i guess we have to use this
    app = QtWidgets.QApplication([])
    qtApp = MLCellApp()
    qtApp.show()
    app.exec_()