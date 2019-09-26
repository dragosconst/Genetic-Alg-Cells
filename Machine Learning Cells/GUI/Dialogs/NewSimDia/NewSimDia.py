from PyQt5 import QtCore, QtWidgets, QtGui

from NewSimBase import Ui_NewSimDialogBase

class NewSimDia(Ui_NewSimDialogBase, QtWidgets.QDialog):
    def __init__(self, MLwindow):
        super().__init__()
        self.setupUi(self)

        self.cancelButton.clicked.connect(lambda: self.close())
        self.cellNoLine.setValidator(QtGui.QIntValidator())
        self.genDurLine.setValidator(QtGui.QDoubleValidator())

        self.okButton.clicked.connect(lambda: self._passData(MLwindow))
        
    def _passData(self, MLwindow):

        MLwindow._startNewSim(self, int(self.cellNoLine.text()), float(self.genDurLine.text()))
        self.close()