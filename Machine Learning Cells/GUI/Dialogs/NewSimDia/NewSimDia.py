from PyQt5 import QtCore, QtWidgets, QtGui

from NewSimBase import Ui_NewSimDialogBase
from CellNoErrDia import CellNoErr

class NewSimDia(Ui_NewSimDialogBase, QtWidgets.QDialog):
    def __init__(self, MLwindow):
        super().__init__()
        self.setupUi(self)

        self.cancelButton.clicked.connect(lambda: self.close())
        self.cellNoLine.setValidator(QtGui.QIntValidator())
        self.genDurLine.setValidator(QtGui.QDoubleValidator())

        self.okButton.clicked.connect(lambda: self._passData(MLwindow))
        
    def _passData(self, MLwindow):
        if self.cellNoLine.text() == "" or self.genDurLine.text() == "":
            errDia = CellNoErr()
            errDia.errText.setText("Please enter a valid input\n for both fields!")
            errDia.setWindowTitle("Invalid Input")
            errDia.exec_()
            return

        if int(self.cellNoLine.text()) > 50:
            errDia = CellNoErr()
            errDia.exec_()
            return

        MLwindow._startNewSim(self, int(self.cellNoLine.text()), float(self.genDurLine.text()))
        self.close()

