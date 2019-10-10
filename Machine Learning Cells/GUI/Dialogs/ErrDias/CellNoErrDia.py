from PySide2 import QtCore, QtGui, QtWidgets

from CellNoErrBase import Ui_CellNoErr

class CellNoErr(Ui_CellNoErr, QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.okButton.clicked.connect(lambda: self.close())
