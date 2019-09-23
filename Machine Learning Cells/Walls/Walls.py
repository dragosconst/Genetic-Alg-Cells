from PyQt5 import QtWidgets, QtCore, QtGui

# this will be the class of the walls that border the available area for 
class Wall(QtWidgets.QGraphicsRectItem):
    def __init__(self, side):
        super().__init__()
        self._colorText = "darkblue" # this will be the default color for all walls
        self.setRect(0, 0, self._buildRect(side).width(), self._buildRect(side).height()) # the graphics item
        self.setPos(self._buildRect(side).x(), self._buildRect(side).y()) # this is the coordinate trick explained in the wiki
        self.setPen(QtGui.QPen(QtGui.QColor(self._colorText)))
        self.setBrush(QtGui.QBrush(QtGui.QColor(self._colorText)))

        self._side = side


    # returns the side of the scene which this wall occupies
    def side(self):
        return self._side

    # methods for getting the wall dimensions
    def wallHeight(self):
        return self.rect().height()
    def wallWidth(self):
        return self.rect().width()

    # the scene\absolute coords of the wall
    def wallX(self):
        return self.x()
    def wallY(self):
        return self.y()

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
        topRect = QtCore.QRectF(0, 0, 1000, 25)

        return topRect

    # second side and so on
    def _buildRect2(self):
        rightRect = QtCore.QRectF(975, 0, 25, 1000)

        return rightRect

    def _buildRect3(self):
        bottomRect = QtCore.QRectF(0, 975, 1000, 25)

        return bottomRect

    def _buildRect4(self):
        leftRect = QtCore.QRectF(0, 0, 25, 1000)

        return leftRect
        

