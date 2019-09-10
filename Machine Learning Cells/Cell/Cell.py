import math
import random as rand
from enum import Enum

from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np

# I'm not done converting yet!!

class BaseShape(Enum): # not sure if we will ever use this enum, but this is the standard I use in the class
    Square = 1
    Rect = 2
    Rhomb = 3

class Cell():
    def __init__(self, app):
        super().__init__()
        self.area = rand.randrange(50000, 100001) # selects a random area for the cell
        self.sides = [0, 0] # the value for the width and height(they are equivalent for squares and rhombuses(? hope this is the plural))
        self.angle = rand.randrange(30, 161) # this is only relevant for the rhombus
        self.baseShapeKey = self._chooseShape() # this is the shape from whitch the cell is drawn
        self._multiplier = np.random.uniform(low = 0.37, high = 0.8, size = (1,)) # this multiplies is used for determing the height(second side) of the rectangle; given the way the paint event works, if the random multiplier were to be calculated in the draw function, it would keep getting change at every call and make a very chaotic drawing
        self._baseShape = None # the base shape of the cell
        self._circles = [] # here will be saved the circles drawn on the cell
        self._circNum = self._chooseNumberOfCircles() # chooses whether to draw one or two circles(and their symmetric counterparts)
        self._sidesWithCircles = [] # similar to the older turtle algorithm, it won't draw two circles on the same side
        
        self.baseShapeKey = 2 # these two values are for testing only, once I finish the drawing algorithm, they will be deleted
        self._circNum = 2
        self._drawShape(app.mapScene, app.mapGView) # draws the base shape

        self._prepCircles(0, 0, app) # this function prepares the circles for being drawn and adds them to the scene, after they are prepped


        
    # FUNCTIONS FOR CHOOSING SOME RANDOM VALUES
    def _chooseShape(self):
        return rand.randrange(1, 4)

    def _chooseNumberOfCircles(self):
        return rand.randrange(1, 3)

    # FUNCTIONS FOR CHOOSING THE SIDE ON WHICH TO DRAW
    def _checkSideCircle(self, side): # some simple stuff, checks if this side was already used
        for usedSide in self._sidesWithCircles:
            if usedSide == side:
                return False
        return True

    def _chooseSide(self): # randomly chooses a side with no circle on it
        side = rand.randrange(1, 4)
        while not self._checkSideCircle(side):
            side = rand.randrange(1, 4)

        self._sidesWithCircles.append(side)
        self._sidesWithCircles.append(side + 2 if side <= 2 else side - 2) # for 1 and 2 appends 3 or 4 and for 3 or 4 appends 1 or 2(the opposing sides)


    # MISCELLANEOUS FUNCTIONS  
    # this function returns two circles made with QGraphicsEllipseItem
    # it is made specifically for this class, which is why it makes two circles(the circles come in pairs, that's how the algorithm works)
    def _makeCircle(self, side, sidex, sidey, opsidex, opsidey, radius):
        circle = QtWidgets.QGraphicsEllipseItem(sidex, sidey, radius * 2, radius * 2) # these two objects are temporarily made semi circles with the
        opCircle = QtWidgets.QGraphicsEllipseItem(opsidex, opsidey, radius * 2, radius * 2) # current coords used for checking collision
        if side == 1: # here we set the appropriate
            circle.setStartAngle(0); circle.setSpanAngle(180 * 16) # all angles are multiplied by 16 because Qt works with
            opCircle.setStartAngle(0); opCircle.setSpanAngle(180 * 16) # 1/16ths of angles for some reason
        elif side == 2:
            circle.setStartAngle(270 * 16); circle.setSpanAngle(180 * 16)
            opCircle.setStartAngle(270 * 16); opCircle.setSpanAngle(180 * 16)
        elif side == 3:
            circle.setStartAngle(180 * 16); circle.setSpanAngle(180 * 16)
            opCircle.setStartAngle(180 * 16); opCircle.setSpanAngle(180 * 16)
        else:
            circle.setStartAngle(90 * 16); circle.setSpanAngle(180 * 16)
            opCircle.setStartAngle(90 * 16); opCircle.setSpanAngle(180 * 16)
        return circle, opCircle
    
    # this function does everything needed for the pre-creation of the circles, such as choosing the coordinates, the radius and so on
    # sideLen refers to the length of the sidesWithCircles list
    # soFar represents the ammount of circles added so far
    # window is a MLCellApp object
    def _prepCircles(self, sideLen, soFar, app):
        if soFar >= self._circNum: # if there have been added enough circles, stop the function
            return 
        self._chooseSide() # pretty obvious, chooses a side

        coords = self._chooseCoords(self._sidesWithCircles[sideLen])
        radius = self._chooseRadius(self._sidesWithCircles[sideLen], coords[0], coords[1], coords[2], coords[3])
        self._resetCoords(None, None, None, None, self._sidesWithCircles[sideLen], radius, coords)
        
        circle, opCircle = self._makeCircle(self._sidesWithCircles[sideLen], coords[0], coords[1], coords[2], coords[3], radius)
        self._circles.append(circle) # the code should've been pretty straightforward so far
        self._circles.append(opCircle)
        app.mapScene.addItem(circle)
        app.mapScene.addItem(opCircle)

        self._prepCircles(len(self._sidesWithCircles), soFar + 1, app) # the recursive call makes sure all circles are added

    # this function works as a nice wrapper for the actual chooseRadius functions
    def _chooseRadius(self, side, sidex, sidey, opsidex, opsidey):
        if self.baseShapeKey == BaseShape.Square.value or self.baseShapeKey == BaseShape.Rect.value: # in this case, the function is literally identical
            return self._chooseRadiusSquareOrRect(side, sidex, sidey, opsidex, opsidey)

    # this is a wrapper for resetCoords functions
    def _resetCoords(self, sidex, sidey, opsidex, opsidey, side, radius, coords = None):
        if self.baseShapeKey == BaseShape.Square.value or self.baseShapeKey == BaseShape.Rect.value:
            self._resetCoordsSquareOrRect(sidex, sidey, opsidex, opsidey, side, radius, coords)


    # FUNCTIONS FOR CHOOSING THE COORDS AND THE RADIUS FOR THE SEMI-CIRCLES
    # THEY ARE 3 BY 3 FOR EACH SHAPE(COORDS AND RADIUS AND RESET COORDS FOR SQUARE AND SO ON)
    def _chooseCoords(self, side): # randomly chooses some coords that can draw a circle of minimum radius of 60 on the given side
        if self.baseShapeKey == BaseShape.Square.value:
            return self._chooseCoordsSquareOrRect(side, 60) # minimum 60 radius for squares
        elif self.baseShapeKey == BaseShape.Rect.value:
            return self._chooseCoordsSquareOrRect(side, min(60, self.sides[0] / 2 - 1, self.sides[1] / 2 - 1))
        else:   # for the rhombus
            return self._chooseRhombCoords(side)

    # under this are the 3 functions for squares and rects, they are essentially identical

    # !!READ THIS!!
    # this function is the same for both the square and the rect, because the only difference whatsoever between them is the way the radius
    # is calculated(for the square the minimum radius is 60, while for the rect it can be smaller, depending on the width and height)
    # this can be easily solved by passing the radius as a parameter
    def _chooseCoordsSquareOrRect(self, side, radius): # this function will return a list of the top-left coords of the rects of the both circles
        
        sideX = sideY = opSideX = opSideY = 0 # these are the top left coords of the circle on this side and on the opposite side
        foundGoodCoords = False
        while foundGoodCoords == False:
            foundGoodCoords = True

            # calculates random coordinates that fit on the side(with minimum radius range)
            if side == 1 or side == 3: # chooses the coordonates, depending on the sides
                sideX = rand.randrange(int(self._baseShape.rect().x()), int(self._baseShape.rect().x() + self._baseShape.rect().width() - radius * 2)) # * 2 because that's the diameter of the circle
                
                opSideX = sideX
                sideY = self._baseShape.rect().y() - radius
                opSideY = self._baseShape.rect().y() - radius + self.sides[1]
            elif side == 2 or side == 4:
                sideY = rand.randrange(int(self._baseShape.rect().y()), int(self._baseShape.rect().y() + self._baseShape.rect().height() - radius * 2))
                
                opSideY = sideY
                sideX = self._baseShape.rect().x() - radius
                opSideX = self._baseShape.rect().x() - radius + self.sides[0]

            for circle in self._circles: # iterates over all the already drawn semi circles and checks for collision
                miniCircle, opMiniCircle = self._makeCircle(side, sideX, sideY, opSideX, opSideY, radius)
                if circle.collidesWithItem(miniCircle) or circle.collidesWithItem(opMiniCircle):
                    foundGoodCoords = False
        # here ends this bigass while
        return [sideX, sideY, opSideX, opSideY]
    
    # this function finds the biggest possible radius starting from the given coords
    # just as before, this function would look literally the same for a rectangle
    def _chooseRadiusSquareOrRect(self, side, sidex, sidey, opsidex, opsidey):

        xPos = self._baseShape.rect().x() # x position of the square
        height = self._baseShape.rect().height() - 1
        width = self._baseShape.rect().width() - 1 # minus one because otherwise the circles might end up tangent on the edges, which triggers a collision
        yPos = self._baseShape.rect().y() # y position of the square
        minDim = min(height, width) # this variable is only useful when this function is called for a rectangle, the radius should not exceed the smaller value of the two
        
        maxPosRadNoCircs = 0 # this will hold the maximum possible radius if there were no other circles drawn on the figure
        if side == 1 or side == 3:
            maxPosRadNoCircs = (xPos + width - sidex) / 2 # divides by two because this is technically the biggest diameter
        else:
            maxPosRadNoCircs = (yPos + height - sidey) / 2

        if maxPosRadNoCircs > minDim: # in the case the maximum possible radius is bigger than the minimum dimension(only for rects), than the radius
            maxPosRadNoCircs = minDim # should be reseted to the value of the minimum dim, so the circle isn't drawn over the bounds of the rectangle

        # now it should check whether the current circle intersects other circle that are already drawn, in which case the radius has to be 
        # adjusted accordingly
        actualRadius = maxPosRadNoCircs
        for circle in self._circles:
            sidex, sidey, opsidex, opsidey = self._resetCoordsSquareOrRect(sidex, sidey, opsidex, opsidey, side, actualRadius) # the top left corner of the ellipse has to be updated every time the radius is changed
            currCircle, opCircle = self._makeCircle(side, sidex, sidey, opsidex, opsidey, actualRadius)

            otherCircCenter = [circle.rect().center().x(), circle.rect().center().y()] # center of the circle variable from the loop
            otherCircRadius = circle.rect().height() / 2 # the circle rect is a square (otherwise it would be an ellipse, not a circle)

            if circle.collidesWithItem(currCircle): # this time, each circle must be checked independently, since the max radius is calculated on the basis of circle intersection
                circleCenter = [currCircle.rect().center().x(), currCircle.rect().center().y()]
                circleDist = math.sqrt((otherCircCenter[0] - circleCenter[0]) ** 2 + (otherCircCenter[1] - circleCenter[1]) ** 2)
                actualRadius = circleDist - otherCircRadius
            elif circle.collidesWithItem(opCircle):
                circleCenter = [opCircle.rect().center().x(), opCircle.rect().center().y()]
                circleDist = math.sqrt((otherCircCenter[0] - circleCenter[0]) ** 2 + (otherCircCenter[1] - circleCenter[1]) ** 2)
                actualRadius = circleDist - otherCircRadius
        # here ends this for loop
        return actualRadius

    # this functions resets the "fixed" coords of the circle based on the radius parameter
    # what I mean by "fixed" coords are the coords that are constant on a given side, ie the y coords on side 1(or side 3)
    # again, the function for the square and rect is one and the same
    def _resetCoordsSquareOrRect(self, sidex, sidey, opsidex, opsidey, side, radius, coords = None):
        if coords is not None:
            if side == 1 or side == 3:
                coords[1] = self._baseShape.rect().y() - radius # keep in mind that the coords of an ellipse(a circle) are the top left coords
                coords[3] = coords[1] + self._baseShape.rect().height() # of the rectangle that contains it
            else:
                coords[0] = self._baseShape.rect().x() - radius
                coords[2] = coords[0] + self._baseShape.rect().width()
        else:
            if side == 1 or side == 3:
                sidey = self._baseShape.rect().y() - radius
                opsidey = sidey + self._baseShape.rect().height()
            else:
                sidex = self._baseShape.rect().x() - radius
                opsidex = sidex + self._baseShape.rect().width()
            return sidex, sidey, opsidex, opsidey


    def _chooseRhombCoords(self, side):
        opposingSide = side + 2 if side <= 2 else side - 2
        


    # DRAWING FUNCTIONS
    # this function draws the base shape
    def _drawShape(self, scene, view):
        if self.baseShapeKey == BaseShape.Square.value:
            return self._drawSquare(scene, view)
        elif self.baseShapeKey == BaseShape.Rect.value:
            return self._drawRect(scene, view)
        else:
            return self._drawRhomb(scene, view)

    def _drawRhomb(self, scene, view):

        self.sides[0] = self.sides[1] = math.sqrt(self.area / np.sin(np.deg2rad(self.angle))) # same way we used to build rhombs\rhombuses in the old program
        side = self.sides[0]

        rhombus = QtWidgets.QGraphicsPolygonItem()
        rhombPoly = QtGui.QPolygonF()
        rhombPoly.append(QtCore.QPointF(500 + np.sin(np.deg2rad(self.angle / 2)) * side, 500))
        rhombPoly.append(QtCore.QPointF(500, 500 + np.cos(np.deg2rad(self.angle / 2)) * side))
        rhombPoly.append(QtCore.QPointF(500 + np.sin(np.deg2rad(self.angle / 2)) * side, 500 + 2 * np.cos(np.deg2rad(self.angle / 2)) * side))
        rhombPoly.append(QtCore.QPointF(500 + 2 * np.sin(np.deg2rad(self.angle / 2)) * side, 500 + np.cos(np.deg2rad(self.angle / 2)) * side))
        rhombus.setPolygon(rhombPoly)
        self._baseShape = rhombus
        scene.addPolygon(self._baseShape)
        return self.sides


    def _drawRect(self, scene, view):
        self.sides[1] = math.sqrt(self.area) * self._multiplier[0] 
        self.sides[0] = self.area / self.sides[1]

        self._baseShape = QtWidgets.QGraphicsRectItem(500, 500, self.sides[0], self.sides[1])
        scene.addItem(self._baseShape)
        return self.sides

    def _drawSquare(self, scene, view):
        self.sides[0] = self.sides[1] = math.sqrt(self.area)

        self._baseShape = QtWidgets.QGraphicsRectItem(500, 500, self.sides[0], self.sides[1])
        scene.addItem(self._baseShape)
        return self.sides
    