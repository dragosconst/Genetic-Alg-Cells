from PySide2 import QtCore, QtWidgets, QtGui

from NewSimBase import Ui_NewSimDialogBase
from CellNoErrDia import CellNoErr

class NewSimDia(Ui_NewSimDialogBase, QtWidgets.QDialog):
    def __init__(self, MLwindow):
        super().__init__()
        self.setupUi(self)

        self.cancelButton.clicked.connect(lambda: self.close())
        self.cellNoLine.setValidator(QtGui.QIntValidator()) # the validators make sure the user can only input 
        self.genDurLine.setValidator(QtGui.QDoubleValidator()) # integers or real numbers(in the case of the second line)
        self.algaeNoLine.setValidator(QtGui.QIntValidator())

        self.okButton.clicked.connect(lambda: self._passData(MLwindow))
        self.cancelButton.clicked.connect(lambda: self.closeSelf(MLwindow))
        

    def _passData(self, MLwindow):
        if self.cellNoLine.text() == "" or self.genDurLine.text() == "": # if one of the fields is empty
            errDia = CellNoErr()
            errDia.errText.setText("Please enter a valid input\n for both fields!")
            errDia.setWindowTitle("Invalid Input")
            errDia.exec_()
            return

        if int(self.cellNoLine.text()) > 50: # if the number for the cell generation is too huge, return an error dialog box
            errDia = CellNoErr()
            errDia.exec_()
            return

        if self.algaeNoLine.text() != "" and int(self.algaeNoLine.text()) > int(self.cellNoLine.text()):
            errDia = CellNoErr()
            errDia.errText.setText("Don't enter an algae number greater\n than the cell population!")
            errDia.setWindowTitle("Invalid Input")
            errDia.exec_()
            return


        MLwindow._startNewSim(self, int(self.cellNoLine.text()), float(self.genDurLine.text()),\
           int(self.algaeNoLine.text()) if self.algaeNoLine.text() != "" else 0)
        self.close()

    def closeSelf(self, MLwindow):
        # unpause the current sim
        if MLwindow.currentSim() is not None:
            MLwindow.currentSim().restartSim()
        self.close()
