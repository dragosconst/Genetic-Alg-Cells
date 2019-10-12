# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_simulation.ui',
# licensing of 'new_simulation.ui' applies.
#
# Created: Sat Oct 12 14:18:56 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_NewSimDialogBase(object):
    def setupUi(self, NewSimDialogBase):
        NewSimDialogBase.setObjectName("NewSimDialogBase")
        NewSimDialogBase.resize(360, 289)
        self.gridLayout = QtWidgets.QGridLayout(NewSimDialogBase)
        self.gridLayout.setObjectName("gridLayout")
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setObjectName("mainLayout")
        self.welcomeText = QtWidgets.QLabel(NewSimDialogBase)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.welcomeText.setFont(font)
        self.welcomeText.setAlignment(QtCore.Qt.AlignCenter)
        self.welcomeText.setObjectName("welcomeText")
        self.mainLayout.addWidget(self.welcomeText)
        self.formLay = QtWidgets.QFormLayout()
        self.formLay.setObjectName("formLay")
        self.cellNoText = QtWidgets.QLabel(NewSimDialogBase)
        self.cellNoText.setAlignment(QtCore.Qt.AlignCenter)
        self.cellNoText.setObjectName("cellNoText")
        self.formLay.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.cellNoText)
        self.cellNoLine = QtWidgets.QLineEdit(NewSimDialogBase)
        self.cellNoLine.setObjectName("cellNoLine")
        self.formLay.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cellNoLine)
        self.genDurText = QtWidgets.QLabel(NewSimDialogBase)
        self.genDurText.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.genDurText.setAlignment(QtCore.Qt.AlignCenter)
        self.genDurText.setObjectName("genDurText")
        self.formLay.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.genDurText)
        self.genDurLine = QtWidgets.QLineEdit(NewSimDialogBase)
        self.genDurLine.setPlaceholderText("")
        self.genDurLine.setObjectName("genDurLine")
        self.formLay.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.genDurLine)
        self.algaeText = QtWidgets.QLabel(NewSimDialogBase)
        self.algaeText.setAlignment(QtCore.Qt.AlignCenter)
        self.algaeText.setObjectName("algaeText")
        self.formLay.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.algaeText)
        self.algaeNoLine = QtWidgets.QLineEdit(NewSimDialogBase)
        self.algaeNoLine.setObjectName("algaeNoLine")
        self.formLay.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.algaeNoLine)
        self.algaeSpreadText = QtWidgets.QLabel(NewSimDialogBase)
        self.algaeSpreadText.setAlignment(QtCore.Qt.AlignCenter)
        self.algaeSpreadText.setObjectName("algaeSpreadText")
        self.formLay.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.algaeSpreadText)
        self.algaeSpreadCombo = QtWidgets.QComboBox(NewSimDialogBase)
        self.algaeSpreadCombo.setObjectName("algaeSpreadCombo")
        self.algaeSpreadCombo.addItem("")
        self.algaeSpreadCombo.addItem("")
        self.formLay.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.algaeSpreadCombo)
        self.threshText = QtWidgets.QLabel(NewSimDialogBase)
        self.threshText.setAlignment(QtCore.Qt.AlignCenter)
        self.threshText.setObjectName("threshText")
        self.formLay.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.threshText)
        self.threshLine = QtWidgets.QLineEdit(NewSimDialogBase)
        self.threshLine.setObjectName("threshLine")
        self.formLay.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.threshLine)
        self.mainLayout.addLayout(self.formLay)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addItem(spacerItem)
        self.loadNewSim = QtWidgets.QProgressBar(NewSimDialogBase)
        self.loadNewSim.setProperty("value", 0)
        self.loadNewSim.setObjectName("loadNewSim")
        self.mainLayout.addWidget(self.loadNewSim)
        self.buttonLay = QtWidgets.QHBoxLayout()
        self.buttonLay.setObjectName("buttonLay")
        self.okButton = QtWidgets.QPushButton(NewSimDialogBase)
        self.okButton.setObjectName("okButton")
        self.buttonLay.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(NewSimDialogBase)
        self.cancelButton.setObjectName("cancelButton")
        self.buttonLay.addWidget(self.cancelButton)
        self.mainLayout.addLayout(self.buttonLay)
        self.gridLayout.addLayout(self.mainLayout, 0, 0, 1, 1)

        self.retranslateUi(NewSimDialogBase)
        self.algaeSpreadCombo.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(NewSimDialogBase)

    def retranslateUi(self, NewSimDialogBase):
        NewSimDialogBase.setWindowTitle(QtWidgets.QApplication.translate("NewSimDialogBase", "New Simulation", None, -1))
        self.welcomeText.setText(QtWidgets.QApplication.translate("NewSimDialogBase", "Create a new simulation...", None, -1))
        self.cellNoText.setText(QtWidgets.QApplication.translate("NewSimDialogBase", "Write here how many cells\n"
" should be in a generation", None, -1))
        self.cellNoLine.setPlaceholderText(QtWidgets.QApplication.translate("NewSimDialogBase", "No more than 50 cells...", None, -1))
        self.genDurText.setText(QtWidgets.QApplication.translate("NewSimDialogBase", "Write here how many seconds\n"
" should a generation last", None, -1))
        self.algaeText.setText(QtWidgets.QApplication.translate("NewSimDialogBase", "Write here how many algae\n"
"should a generation have\n"
"(optional)", None, -1))
        self.algaeNoLine.setPlaceholderText(QtWidgets.QApplication.translate("NewSimDialogBase", "No more than the cell pop...", None, -1))
        self.algaeSpreadText.setText(QtWidgets.QApplication.translate("NewSimDialogBase", "Choose algae spread", None, -1))
        self.algaeSpreadCombo.setItemText(0, QtWidgets.QApplication.translate("NewSimDialogBase", "Regular algae spread", None, -1))
        self.algaeSpreadCombo.setItemText(1, QtWidgets.QApplication.translate("NewSimDialogBase", "Full map algae spread", None, -1))
        self.threshText.setText(QtWidgets.QApplication.translate("NewSimDialogBase", "Write the CELL_EAT_THRESHOLD\n"
"value here\n"
"(optional)", None, -1))
        self.okButton.setText(QtWidgets.QApplication.translate("NewSimDialogBase", "OK", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("NewSimDialogBase", "Cancel", None, -1))

