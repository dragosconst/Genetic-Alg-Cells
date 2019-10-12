# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cell_no_err.ui',
# licensing of 'cell_no_err.ui' applies.
#
# Created: Sat Oct 12 18:02:49 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CellNoErr(object):
    def setupUi(self, CellNoErr):
        CellNoErr.setObjectName("CellNoErr")
        CellNoErr.resize(340, 145)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/iconPic/cell_app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CellNoErr.setWindowIcon(icon)
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
        CellNoErr.setWindowTitle(QtWidgets.QApplication.translate("CellNoErr", "Cell Number Too Large", None, -1))
        self.errText.setText(QtWidgets.QApplication.translate("CellNoErr", "Don\'t enter a cell number\n"
" greater than 50!", None, -1))
        self.okButton.setText(QtWidgets.QApplication.translate("CellNoErr", "OK", None, -1))

import icon_rc
