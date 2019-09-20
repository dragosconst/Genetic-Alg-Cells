from PyQt5 import QtWidgets, QtCore, QtGui

# this will be the class of the walls that border the available area for 
class Wall():
    def __init__(self, side):
        self._colorText = "darkblue" # this will be the default color for all walls
        self._rectItem = self._buildRect(side) # the graphics item


    def rectItem(self):
        return self._rectItem

    # returns the QGraphicsRectItem for the wall of the corresponding side
    def _buildRect(self, side):
        if side == 1:
            return self._buildRect1()
        elif side == 2:
            return self._buildRect2()
        elif side == 3:
            return self._buildRect3()
        else:
            return self._buildRect4()

    # this method builds a rectangle for the first side of the graphics view(using the same encoding we used for a rect's sides)
    def _buildRect1(self):
        topRect = QtWidgets.QGraphicsRectItem(0, 0, 1000, 25)
        topRect.setPen(QtGui.QPen(QtGui.QColor(self._colorText)))
        topRect.setBrush(QtGui.QBrush(QtGui.QColor(self._colorText)))

        return topRect

    # second side and so on
    def _buildRect2(self):
        rightRect = QtWidgets.QGraphicsRectItem(975, 0, 25, 1000)
        rightRect.setPen(QtGui.QPen(QtGui.QColor(self._colorText)))
        rightRect.setBrush(QtGui.QBrush(QtGui.QColor(self._colorText)))

        return rightRect

    def _buildRect3(self):
        bottomRect = QtWidgets.QGraphicsRectItem(0, 975, 1000, 25)
        bottomRect.setPen(QtGui.QPen(QtGui.QColor(self._colorText)))
        bottomRect.setBrush(QtGui.QBrush(QtGui.QColor(self._colorText)))

        return bottomRect

    def _buildRect4(self):
        leftRect = QtWidgets.QGraphicsRectItem(0, 0, 25, 1000)
        leftRect.setPen(QtGui.QPen(QtGui.QColor(self._colorText)))
        leftRect.setBrush(QtGui.QBrush(QtGui.QColor(self._colorText)))

        return leftRect
        

