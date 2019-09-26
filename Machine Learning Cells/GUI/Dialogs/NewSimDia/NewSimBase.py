# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_simulation.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewSimDialogBase(object):
    def setupUi(self, NewSimDialogBase):
        NewSimDialogBase.setObjectName("NewSimDialogBase")
        NewSimDialogBase.resize(339, 226)
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
        self.cellNoForm = QtWidgets.QFormLayout()
        self.cellNoForm.setObjectName("cellNoForm")
        self.cellNoText = QtWidgets.QLabel(NewSimDialogBase)
        self.cellNoText.setAlignment(QtCore.Qt.AlignCenter)
        self.cellNoText.setObjectName("cellNoText")
        self.cellNoForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.cellNoText)
        self.cellNoLine = QtWidgets.QLineEdit(NewSimDialogBase)
        self.cellNoLine.setObjectName("cellNoLine")
        self.cellNoForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cellNoLine)
        self.mainLayout.addLayout(self.cellNoForm)
        self.genDurForm = QtWidgets.QFormLayout()
        self.genDurForm.setObjectName("genDurForm")
        self.genDurText = QtWidgets.QLabel(NewSimDialogBase)
        self.genDurText.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.genDurText.setAlignment(QtCore.Qt.AlignCenter)
        self.genDurText.setObjectName("genDurText")
        self.genDurForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.genDurText)
        self.genDurLine = QtWidgets.QLineEdit(NewSimDialogBase)
        self.genDurLine.setPlaceholderText("")
        self.genDurLine.setObjectName("genDurLine")
        self.genDurForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.genDurLine)
        self.mainLayout.addLayout(self.genDurForm)
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
        QtCore.QMetaObject.connectSlotsByName(NewSimDialogBase)

    def retranslateUi(self, NewSimDialogBase):
        _translate = QtCore.QCoreApplication.translate
        NewSimDialogBase.setWindowTitle(_translate("NewSimDialogBase", "New Generation"))
        self.welcomeText.setText(_translate("NewSimDialogBase", "Create a new simulation..."))
        self.cellNoText.setText(_translate("NewSimDialogBase", "Write here how many cells\n"
" should be in a generation"))
        self.cellNoLine.setPlaceholderText(_translate("NewSimDialogBase", "No more than 50 cells..."))
        self.genDurText.setText(_translate("NewSimDialogBase", "Write here how many seconds\n"
" should a generation last"))
        self.okButton.setText(_translate("NewSimDialogBase", "OK"))
        self.cancelButton.setText(_translate("NewSimDialogBase", "Cancel"))
