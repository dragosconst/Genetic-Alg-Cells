# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cell_no_err.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CellNoErr(object):
    def setupUi(self, CellNoErr):
        CellNoErr.setObjectName("CellNoErr")
        CellNoErr.resize(340, 145)
        self.gridLayout_2 = QtWidgets.QGridLayout(CellNoErr)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.errText = QtWidgets.QLabel(CellNoErr)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.errText.setFont(font)
        self.errText.setAlignment(QtCore.Qt.AlignCenter)
        self.errText.setObjectName("errText")
        self.gridLayout_2.addWidget(self.errText, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.okButton = QtWidgets.QPushButton(CellNoErr)
        self.okButton.setObjectName("okButton")
        self.gridLayout_2.addWidget(self.okButton, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 2, 1, 1)

        self.retranslateUi(CellNoErr)
        QtCore.QMetaObject.connectSlotsByName(CellNoErr)

    def retranslateUi(self, CellNoErr):
        _translate = QtCore.QCoreApplication.translate
        CellNoErr.setWindowTitle(_translate("CellNoErr", "Cell Number Too Large"))
        self.errText.setText(_translate("CellNoErr", "Don\'t enter a cell number\n"
" greater than 50!"))
        self.okButton.setText(_translate("CellNoErr", "OK"))
