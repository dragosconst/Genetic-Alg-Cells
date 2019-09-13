import math
import random as rand
from enum import Enum

from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np


class BaseShape(Enum): # not sure if we will ever use this enum, but this is the standard I use in the class
    Square = 1
    Rect = 2
    Rhomb = 3

class Cell():
    def __init__(self, app):
        super().__init__()
        self._area = rand.randrange(50000, 100001) # selects a random _area for the cell
        self._sides = [0, 0] # the value for the width and height(they are equivalent for squares and rhombuses(? hope this is the plural))
        self._angle = rand.randrange(30, 161) # this is only relevant for the rhombus
        self._baseShapeKey = self._chooseShape() # this is the shape from whitch the cell is drawn
        self._multiplier = np.random.uniform(low = 0.37, high = 0.8, size = (1,)) # this multiplies is used for determing the height(second side) of the rectangle; given the way the paint event works, if the random multiplier were to be calculated in the draw function, it would keep getting change at every call and make a very chaotic drawing
        self._baseShape = None # the base shape of the cell
        self._circles = [] # here will be saved the circles drawn on the cell
        self._circNum = self._chooseNumberOfCircles() # chooses whether to draw one or two circles(and their symmetric counterparts)
        self._sidesWithCircles = [] # similar to the older turtle algorithm, it won't draw two circles on the same side
        
        self._drawShape(app.mapScene, app.mapGView) # draws the base shape

        self._prepCircles(0, 0, app) # this function prepares the circles for being drawn and adds them to the scene, after they are prepared


        
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
        side = rand.randrange(1, 5)
        while not self._checkSideCircle(side):
            side = rand.randrange(1, 5)

        self._sidesWithCircles.append(side)
        self._sidesWithCircles.append(side + 2 if side <= 2 else side - 2) # for 1 and 2 appends 3 or 4 and for 3 or 4 appends 1 or 2(the opposing sides)


    # MISCELLANEOUS FUNCTIONS  
    # this function returns two circles made with QGraphicsEllipseItem
    # it is made specifically for this class, which is why it makes two circles(the circles come in pairs, that's how the algorithm works)
    def _makeCircle(self, side, sidex, sidey, opsidex, opsidey, radius):
        if self._baseShapeKey == BaseShape.Square.value or self._baseShapeKey == BaseShape.Rect.value:
            add = 360 - 90 * (side - 1) # neat little trick
        else: # add represents the angle that is added to the ellipse angles, it is used only for the rhombus
            line1, line2, line3, line4 = self._getRhombLines()
            if side == 1:
                add = line1.angle()
            elif side == 2:
                add = line2.angle()
            elif side == 3:
                add = line3.angle()
            else:
                add = line4.angle()
        
        circle = QtWidgets.QGraphicsEllipseItem(sidex, sidey, radius * 2, radius * 2) # these two objects are temporarily made semi circles with the
        opCircle = QtWidgets.QGraphicsEllipseItem(opsidex, opsidey, radius * 2, radius * 2) # current coords used for checking collision
        
        circle.setStartAngle(add * 16) ; circle.setSpanAngle(180 * 16)
        opCircle.setStartAngle(add * 16) ; opCircle.setSpanAngle(180 * 16)
        return circle, opCircle
    
    # this function does everything needed for the pre-creation of the circles, such as choosing the coordinates, the radius and so on
    # sideLen refers to the length of the sidesWithCircles list
    # soFar represents the ammount of circles added so far
    # app is a MLCellApp object
    def _prepCircles(self, sideLen, soFar, app):
        if soFar >= self._circNum: # if there have been added enough circles, stop the function
            return 
        self._chooseSide() # pretty obvious, chooses a side
        checkForBreak = self._circNum
        coords = self._chooseCoords(self._sidesWithCircles[sideLen]) # chooses the coords; the rhomb will return some coords ON the rhomb, not the coords of the top-left point
        if checkForBreak != self._circNum: # if circNum is changed, that means there was no space for a circle of minimum radius of 60
            return 
        newCoords = [coords[0], coords[1], coords[2], coords[3]] # given that lists are mutable, writing newCoords = coords would make any change to coords or newCoords apply to both lists, which is the opposite of what should happen here
        radius = self._chooseRadius(self._sidesWithCircles[sideLen], coords[0], coords[1], coords[2], coords[3])
        self._resetCoords(None, None, None, None, self._sidesWithCircles[sideLen], radius, coords, newCoords)

        circle, opCircle = self._makeCircle(self._sidesWithCircles[sideLen], newCoords[0], newCoords[1], newCoords[2], newCoords[3], radius)
        self._circles.append(circle) # the code should've been pretty straightforward so far
        self._circles.append(opCircle)
        app.mapScene.addItem(circle)
        app.mapScene.addItem(opCircle)
        self._prepCircles(len(self._sidesWithCircles), soFar + 1, app) # the recursive call makes sure all circles are added

    # this function works as a nice wrapper  for the actual chooseRadius functions
    def _chooseRadius(self, side, sidex, sidey, opsidex, opsidey):
        if self._baseShapeKey == BaseShape.Square.value or self._baseShapeKey == BaseShape.Rect.value: # in this case, the function is literally identical
            return self._chooseRadiusSquareOrRect(side, sidex, sidey, opsidex, opsidey)
        else:
            return self._chooseRadiusRhomb(side, sidex, sidey, opsidex, opsidey)

    # this is a wrapper for resetCoords functions
    def _resetCoords(self, sidex, sidey, opsidex, opsidey, side, radius, coords = None, newCoords = None):
        if self._baseShapeKey == BaseShape.Square.value or self._baseShapeKey == BaseShape.Rect.value:
            self._resetCoordsSquareOrRect(sidex, sidey, opsidex, opsidey, side, radius, coords, newCoords)
        else:
            self._resetCoordsRhomb(side, radius, coords, newCoords)
            

    # this function will return the nearest point on a line from a specified point
    def _nearestPoint(self, point, line):
        perpLine = QtCore.QLineF(point.x(), point.y(), point.x(), 0.0)
        perpLine.setAngle(90 + line.angle()) # rotates the new line in such a way that it becomes perpendicular on the old line
        interPoint = QtCore.QPointF(0, 0)
        line.intersect(perpLine, interPoint)
        return interPoint
    # this function will calculate the distance between a line and a point in a clever way
    def _disToLine(self, point, line):
        interPoint = self._nearestPoint(point, line) # looks for the nearest point on the line
        return QtCore.QLineF(point, interPoint).length() # returns the length of the line from this point to the nearest point


    # this function checks the collision between circles drawn "inside" the shape
    def _checkCircleColl(self, radius, circle, opCircle):
        otherCircCenter = circle.rect().center() # center of the circle variable from the loop
        otherCircRadius = circle.rect().height() / 2 # the circle rect is a square (otherwise it would be an ellipse, not a circle)

        opCircleCenter = opCircle.rect().center()
        opCircleDist = QtCore.QLineF(otherCircCenter, opCircleCenter).length()
        if circle.collidesWithItem(opCircle):
            if radius + otherCircRadius > opCircleDist:
                radius = opCircleDist - otherCircRadius # this isn't exactly correct, but a proper function would bloat the code even more; this is more detailed in the wiki
        return radius if radius > 0 else 0

    # FUNCTIONS FOR CHOOSING THE COORDS AND THE RADIUS FOR THE SEMI-CIRCLES
    def _chooseCoords(self, side): # randomly chooses some coords that can draw a circle of minimum radius of 60 on the given side
        if self._baseShapeKey == BaseShape.Square.value:
            return self._chooseCoordsSquareOrRect(side, 60) # minimum 20 radius for squares
        elif self._baseShapeKey == BaseShape.Rect.value:
            return self._chooseCoordsSquareOrRect(side, min(60, self._sides[0] / 2 - 1, self._sides[1] / 2 - 1))
        else:   # for the rhombus
            return self._chooseCoordsRhomb(side, 60)

    # under this are the 3 functions for squares and rects, they are essentially identical

    # !!READ THIS!!
    # this function is the same for both the square and the rect, because the only difference whatsoever between them is the way the radius
    # is calculated(for the square the minimum radius is 60, while for the rect it can be smaller, depending on the width and height)
    # this can be easily solved by passing the radius as a parameter
    def _chooseCoordsSquareOrRect(self, side, radius): # this function will return a list of the top-left coords of the rects of the both circles
        
        sideX = sideY = opSideX = opSideY = 0 # these are the top left coords of the circle on this side and on the opposite side
        foundGoodCoords = False
        tries = 0
        while foundGoodCoords == False:
            foundGoodCoords = True

            if tries >= 1000: # if the loop is executed this many times, it almost surely means there is no space for a circle of minimum 60 radius
                self._circNum -= 1
                return [0, 0, 0, 0]

            # calculates random coordinates that fit on the side(with minimum radius range)
            if side == 1 or side == 3: # chooses the coordonates, depending on the sides
                sideX = rand.randrange(int(self._baseShape.rect().x()), int(self._baseShape.rect().x() + self._baseShape.rect().width() - radius * 2)) # * 2 because that's the diameter of the circle
                
                opSideX = sideX
                sideY = self._baseShape.rect().y() - radius if side == 1 else self._baseShape.rect().y() - radius + self._sides[1]
                opSideY = self._baseShape.rect().y() - radius + self._sides[1] if side == 1 else self._baseShape.rect().y() - radius
            elif side == 2 or side == 4:
                sideY = rand.randrange(int(self._baseShape.rect().y()), int(self._baseShape.rect().y() + self._baseShape.rect().height() - radius * 2))
                
                opSideY = sideY
                sideX = self._baseShape.rect().x() - radius if side == 4 else self._baseShape.rect().x() - radius + self._sides[0]
                opSideX = self._baseShape.rect().x() - radius + self._sides[0] if side == 4 else self._baseShape.rect().x() - radius

            for circle in self._circles: # iterates over all the already drawn semi circles and checks for collision
                miniCircle, opMiniCircle = self._makeCircle(side, sideX, sideY, opSideX, opSideY, radius)
                if circle.collidesWithItem(miniCircle) or circle.collidesWithItem(opMiniCircle):
                    foundGoodCoords = False
            tries += 1
        # here ends this big while
        return [sideX, sideY, opSideX, opSideY]
    
    # this function finds the biggest possible radius starting from the given coords
    # just as before, this function would look literally the same for a rectangle
    def _chooseRadiusSquareOrRect(self, side, sidex, sidey, opsidex, opsidey):

        xPos = self._baseShape.rect().x() # x position of the square
        height = self._baseShape.rect().height() 
        width = self._baseShape.rect().width()
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
        index = 0
        for circle in self._circles:
            sidex, sidey, opsidex, opsidey = self._resetCoordsSquareOrRect(sidex, sidey, opsidex, opsidey, side, actualRadius) # the top left corner of the ellipse has to be updated every time the radius is changed
            currCircle, opCircle = self._makeCircle(side, sidex, sidey, opsidex, opsidey, actualRadius)
            
            if index > 0: # there is no point in checking with the first circle, because it will always be drawn "outside"
                actualRadius = self._checkCircleColl(actualRadius, circle, opCircle)
            index += 1
        # here ends this for loop
        return actualRadius

    # this functions resets the "fixed" coords of the circle based on the radius parameter
    # what I mean by "fixed" coords are the coords that are constant on a given side, ie the y coords on side 1(or side 3)
    # again, the function for the square and rect is one and the same
    def _resetCoordsSquareOrRect(self, sidex, sidey, opsidex, opsidey, side, radius, coords = None, newCoords = None):
        if coords is not None:
            if side == 1:
                newCoords[1] = coords[1] = self._baseShape.rect().y() - radius # keep in mind that the coords of an ellipse(a circle) are the top left coords
                newCoords[3] = coords[3] = coords[1] + self._baseShape.rect().height() # of the rectangle that contains it
            elif side == 3:
                newCoords[1] = coords[1] = self._baseShape.rect().y() + self._baseShape.rect().height() - radius # keep in mind that the coords of an ellipse(a circle) are the top left coords
                newCoords[3] = coords[3] = coords[1] - self._baseShape.rect().height() # of the rectangle that contains it
            elif side == 2:
                newCoords[0] = coords[0] = self._baseShape.rect().x() + self._baseShape.rect().width() - radius
                newCoords[2] = coords[2] = coords[0] - self._baseShape.rect().width()
            else:
                newCoords[0] = coords[0] = self._baseShape.rect().x() - radius
                newCoords[2] = coords[2] = coords[0] + self._baseShape.rect().width()
        else:
            if side == 1:
                sidey = self._baseShape.rect().y() - radius
                opsidey = sidey + self._baseShape.rect().height()
            elif side == 3:
                sidey = self._baseShape.rect().y() + self._baseShape.rect().height() - radius
                opsidey = sidey - self._baseShape.rect().height()
            elif side == 2:
                sidex = self._baseShape.rect().x() + self._baseShape.rect().width() - radius
                opsidex = sidex - self._baseShape.rect().width()
            else:
                sidex = self._baseShape.rect().x() - radius
                opsidex = sidex + self._baseShape.rect().width()
            return sidex, sidey, opsidex, opsidey


    # this algorithm is a bit weirder, given the nature of rhombuses, from the points chosen by this function it might still not be possible
    # for a circle of specified radius to be drawn, due to the way rhombuses' "inwards" are. oof this doesn't really makes sense, does it
    # it should be noted that it returns the coordinates projected on the rhombus, not of the rectangle in which the ellipse is included
    def _chooseCoordsRhomb(self, side, radius):
        
        sideX = sideY = opSideX = opSideY = 0
        noSmallCircs = 40 # this constant is used for the bounds of the coordinates, to make sure that no small circles appear
        line1, line2, line3, line4 = self._getRhombLines()
    
        leftX = self._baseShape.polygon()[3].x() # this is the way the points are added in the polygon; the most upward point is the last one
        midX = self._baseShape.polygon()[0].x() # and is, therefore, the "middle point" between the extremes of the rhombus on the x-axis.
        rightX = self._baseShape.polygon()[1].x()  

        xDist = midX - leftX # this is the distance between the center of the rhombus and its extremities
        foundGoodCoords = False
        tries = 0
        while foundGoodCoords == False:
            foundGoodCoords = True

            if tries >= 1000: # if the loop is executed this many times, it almost surely means there is no space for a circle of minimum 60 radius
                self._circNum -= 1
                return [0, 0, 0, 0]

            # calculates random coordinates that fit on the side(with minimum radius range)
            firstBound = leftX + noSmallCircs if side == 3 or side == 4 else midX + noSmallCircs # starts from the leftmost point + radius because otherwise it might
            lastBound = midX - noSmallCircs if side == 3 or side == 4 else rightX - noSmallCircs # choose a point very close to the extremities, which would make for a very small circle
            sideX = rand.randrange(int(firstBound), int(lastBound))
            opSideX = sideX + xDist if side == 3 or side == 4 else sideX - xDist

            """ The next lines of code are a neat trick I came up with. Basically, in order to find the projection of the chosen x-point
                on the rhombus, the program creates an imaginary(imaginary because it is never drawn on the app) line that is perpendicular
                on the x-Axis and goes through the given x-points. The intersection point of this imaginary line and the line of the current
                "side" of the rhombus give the y-projection. This way, there's basically no maths involved in doing this(besides what Qt does
                in the background ofc)."""
            sidePoint = QtCore.QPointF(sideX, 0)
            opSidePoint = QtCore.QPointF(opSideX, 0) 
            interSideLine = QtCore.QLineF(sidePoint, QtCore.QPointF(sideX, 1000))
            interOpLine = QtCore.QLineF(opSidePoint, QtCore.QPointF(opSideX, 1000))
            interSidePoint = QtCore.QPointF(0, 0)
            interOpPoint = QtCore.QPointF(0, 0)
            if side == 1:
                line1.intersect(interSideLine, interSidePoint)
                line3.intersect(interOpLine, interOpPoint)
            elif side == 2:
                line2.intersect(interSideLine, interSidePoint)
                line4.intersect(interOpLine, interOpPoint)
            elif side == 3:
                line3.intersect(interSideLine, interSidePoint)
                line1.intersect(interOpLine, interOpPoint)
            else:
                line4.intersect(interSideLine, interSidePoint)
                line2.intersect(interOpLine, interOpPoint)
            sideY = interSidePoint.y()
            opSideY = interOpPoint.y()

            for circle in self._circles: # iterates over all the already drawn semi circles and checks for collision
                miniCircle, opMiniCircle = self._makeCircle(side, sideX, sideY, opSideX, opSideY, radius)
                if circle.collidesWithItem(miniCircle) or circle.collidesWithItem(opMiniCircle):
                    foundGoodCoords = False
            tries += 1
        # here ends the while
        return [sideX, sideY, opSideX, opSideY]

    # this algorithm will also be trickier, I will try to use as much Qt as possible, in order to avoid bloating the code with trigonometry
    def _chooseRadiusRhomb(self, side, sidex, sidey, opsidex, opsidey):
        oppositeSide = side + 2 if side == 1 or side == 2 else side - 2

        sidePoint = QtCore.QPointF(sidex, sidey) # the center of the circle
        opSidePoint = QtCore.QPointF(opsidex, opsidey) # the center of the opposite circle

        dist = min(self._smallestDistRhomb(sidePoint, side), self._smallestDistRhomb(opSidePoint, oppositeSide)) # this is the smallest distance to any line from either this sides' circle or the opposite sides'
        maxPosRadNoCircs = dist # as in the other function, this is the biggest possible radius if there were no other circles drawn
       

        actualRadius = maxPosRadNoCircs
        coords = [sidex, sidey, opsidex, opsidey]
        newCoords = [coords[0], coords[1], coords[2], coords[3]] # given that lists are mutable, writing newCoords = coords would make any change to coords or newCoords apply to both lists, which is the opposite of what should happen here
        index = 0
        for circle in self._circles:
            self._resetCoords(sidex, sidey, opsidex, opsidey, side, actualRadius, coords, newCoords)
            currCircle, opCircle = self._makeCircle(side, newCoords[0], newCoords[1], newCoords[2], newCoords[3], actualRadius)

            if index > 0: # the first circle is always drawn outside the rhombus and therefore cannot overlap with any other circle
                actualRadius = self._checkCircleColl(actualRadius, circle, opCircle)
            index += 1
        
        return actualRadius


        
    # this does what the other function for the square does, except that in a slightly more compelx manner
    def _resetCoordsRhomb(self, side, radius, coords, newCoords):
        if coords is None:
            assert False # this will return an error

        if newCoords is not None:
            newCoords[0] = coords[0] - radius # this assumes that the coordinates passed by the coords list are the coordinates of the center of the circle
            newCoords[1] = coords[1] - radius
            newCoords[2] = coords[2] - radius
            newCoords[3] = coords[3] - radius
        else:
            assert False # this will return an error, this function would be too tirseome to implement without the use of lists

    # UNDER HERE ARE FUNCTIONS MADE SPECIFICALLY FOR THE RHOMBUS
    # SO FAR, THERE ARE ONLY 3 OF THEM
    # this function will return all the points of the rhombus polygon
    def _getRhombPoints(self):
        poly = self._baseShape.polygon()
        return poly[0], poly[1], poly[2], poly[3]
    # this function will return all the lines of the rhombus polygon
    def _getRhombLines(self):
        poly = self._baseShape.polygon()
        p1, p2, p3, p4 = self._getRhombPoints()

        l1 = QtCore.QLineF(p1, p2)
        l2 = QtCore.QLineF(p2, p3)
        l3 = QtCore.QLineF(p3, p4)
        l4 = QtCore.QLineF(p4, p1)
        return l1, l2, l3, l4

    # this function finds the smallest distances from this point to any of the rhombus' lines and then returns the smallest of these
    def _smallestDistRhomb(self, point, side):
        line1, line2, line3, line4 = self._getRhombLines()
        dist1 = self._disToLine(point, line1) if side != 1 else line1.length() * 1000 # calculates the minimum distance to every line, keeping both circles in mind
        dist2 = self._disToLine(point, line2) if side != 2 else line1.length() * 1000
        dist3 = self._disToLine(point, line3) if side != 3 else line1.length() * 1000
        dist4 = self._disToLine(point, line4) if side != 4 else line1.length() * 1000

        smolDist = min(dist1, dist2, dist3, dist4) # finds the absolute smalles distance to any line on the rhombus
        return smolDist

                

    # DRAWING FUNCTIONS
    # this function draws the base shape
    def _drawShape(self, scene, view):
        if self._baseShapeKey == BaseShape.Square.value:
            self._drawSquare(scene, view)
        elif self._baseShapeKey == BaseShape.Rect.value:
            self._drawRect(scene, view)
        else:
            self._drawRhomb(scene, view)

    def _drawRhomb(self, scene, view):

        self._sides[0] = self._sides[1] = math.sqrt(self._area / np.sin(np.deg2rad(self._angle))) # same way we used to build rhombs\rhombuses in the old program
        side = self._sides[0]

        rhombus = QtWidgets.QGraphicsPolygonItem()
        rhombPoly = QtGui.QPolygonF()
        rhombPoly.append(QtCore.QPointF(300 + np.sin(np.deg2rad(self._angle / 2)) * side, 300))
        rhombPoly.append(QtCore.QPointF(300 + 2 * np.sin(np.deg2rad(self._angle / 2)) * side, 300 + np.cos(np.deg2rad(self._angle / 2)) * side))
        rhombPoly.append(QtCore.QPointF(300 + np.sin(np.deg2rad(self._angle / 2)) * side, 300 + 2 * np.cos(np.deg2rad(self._angle / 2)) * side))
        rhombPoly.append(QtCore.QPointF(300, 300 + np.cos(np.deg2rad(self._angle / 2)) * side))
        rhombus.setPolygon(rhombPoly)
        self._baseShape = rhombus
        scene.addItem(self._baseShape)


    def _drawRect(self, scene, view):
        self._sides[1] = math.sqrt(self._area) * self._multiplier[0] 
        self._sides[0] = self._area / self._sides[1]

        self._baseShape = QtWidgets.QGraphicsRectItem(300, 300, self._sides[0], self._sides[1])
        scene.addItem(self._baseShape)

    def _drawSquare(self, scene, view):
        self._sides[0] = self._sides[1] = math.sqrt(self._area)

        self._baseShape = QtWidgets.QGraphicsRectItem(300, 300, self._sides[0], self._sides[1])
        scene.addItem(self._baseShape)
    