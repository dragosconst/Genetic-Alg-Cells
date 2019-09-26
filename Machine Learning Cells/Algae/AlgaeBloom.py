from PyQt5 import QtCore, QtGui, QtWidgets

class Bloom(QtCore.QRectF):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self._algae = 0

    # call this before adding an alga to this bloom
    def addAlga(self):
        self._algae += 1

    def algae(self):
        return self._algae
