import math
import random as rand
from enum import Enum

from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np

import util
from GenDataCls import CellData



class BaseShape(Enum): # not sure if we will ever use this enum, but this is the standard I use in the class
    Square = 1
    Rect = 2
    Rhomb = 3

class Cell(QtWidgets.QGraphicsPolygonItem):
    # Class variables
    cellDisjoint = 0 # this represents how many cells do not intersect with other cells; will be used for making
                     # all cells start movement only when all cells have been correctly positioned
    CELL_GEN_POP = 40 # how many cells will be in a generation
    EAT_CELL_THRESHOLD = 130 # the amount of Food Points a cell should exceed in order to eat another celll

    # CLASS METHODS START

    # this function resets the position of every cell, one by one
    @classmethod
    def resetCells(cls, scene, simDia = None, totalEntities = 0, soFar = 0):
        if scene is None: # if the scene object was not constructed, wait a bit for it(by recalling the function 10 ms later)
            reset = QtCore.QTimer()
            reset.singleShot(10, lambda: cls.resetCells(scene))
            return

        for item in scene.items(): # check all cells
            if util.getClassName(item) == "Cell": # if it is a cell
                if item.collidingItems() != []: # if the item collides with anything
                    cls.resetCellPos(scene, item)
                    cls.cellDisjoint += 1
                    if simDia is not None:
                        simDia.loadNewSim.setValue((cls.cellDisjoint + soFar) / totalEntities * 100)
                else:
                    cls.cellDisjoint += 1
                    if simDia is not None:
                        simDia.loadNewSim.setValue((cls.cellDisjoint + soFar) / totalEntities * 100)


    # this function resets the position of an individual cell
    @classmethod
    def resetCellPos(cls, scene, cell):
    
            allCoords = list(range(100, 801))
            allCoords = [allCoords] * 701 # create a 701 x 701 matrix with all possible positions

            for item in scene.items():
                if util.getClassName(item) == "Cell" and item is not cell:
                    yStart = item.actualPos().y() - cell.height() # the bounds in which this cell cannot spawn 
                    yStop = item.actualPos().y() + item.height() # in refernence to the cell it is currently checking
                    if yStart <= 100:
                        yStart = 100
                    if yStop >= 800:
                        yStop = 800
                    xStart = item.actualPos().x() - cell.width()
                    xStop = item.actualPos().x() + item.width()
                    if xStart <= 100:
                        xStart = 100
                    if xStop >= 800:
                        xStop = 800

                    yStart = int(yStart) # given that they might probably end up with floating coordinates 
                    yStop = int(yStop) # they should be casted to whole numbers
                    xStart = int(xStart)
                    xStop = int(xStop)
                    for i in range(yStart - 100, yStop - 100): 
                        for j in range(xStart - 100, xStop - 100):
                            allCoords[i][j] = -1 # -1 means that it cannot spawn on this point
                elif util.getClassName(item) == "Alga": # look for algae too
                    yStart = item.pos().y() - cell.height() # the bounds in which this cell cannot spawn 
                    yStop = item.pos().y() + item.radius() * 2 # in refernence to the alga it is currently checking
                    if yStart <= 100:
                        yStart = 100
                    if yStop >= 800:
                        yStop = 800
                    xStart = item.pos().x() - cell.width()
                    xStop = item.pos().x() + item.radius() * 2
                    if xStart <= 100:
                        xStart = 100
                    if xStop >= 800:
                        xStop = 800

                    yStart = int(yStart) # given that they might probably end up with floating coordinates 
                    yStop = int(yStop) # they should be casted to whole numbers
                    xStart = int(xStart)
                    xStop = int(xStop)
                    for i in range(yStart - 100, yStop - 100): 
                        for j in range(xStart - 100, xStop - 100):
                            allCoords[i][j] = -1 # -1 means that it cannot spawn on this point


            possibleCoords = [] # these will be all the coords in which a cell could be spawn alright
            for i  in range(0, 701):
                for j in range(0, 701):
                    if allCoords[i][j] != -1:
                        possibleCoords.append((i + 100, j + 100))

            newY, newX = rand.choice(possibleCoords) # chooses a random suitable position
            cell.setActualPos(newX, newY)
            cell.resetOrigin(QtCore.QPointF(newX, newY)) # resets the origin point to this

    # start moving all cells once all the positions have been set
    @classmethod
    def startMoving(cls, scene):
        if cls.cellDisjoint == cls.CELL_GEN_POP:
            for item in scene.items():
                if util.getClassName(item) == "Cell":
                    item.createActionRadCirc()
                    item.startFrameClock() 
                    item.startHungerClock()
                    item.updateLoop()
        else:
            tryAgain = QtCore.QTimer()
            tryAgain.singleShot(10, lambda: cls.startMoving(scene))
    # CLASS METHODS END

    # OBJECT\INSTANCE METHODS START

    def __init__(self, genData, genNumber = None, parents = None):
        super().__init__()
        ## VARIABLES TIED TO GENERATION DATA
        self._genData = genData

        ## VARIABLES DIRECTLY RELATED TO THE BASE SHAPE AND THE SEMI-CIRCLES
        self._area = rand.randrange(50, 251) # selects a random _area for the cell
        self._sides = [0, 0] # the value for the width and height(they are equivalent for squares and rhombuses(? hope this is the plural))
        self._angle = rand.randrange(30, 161) # this is only relevant for the rhombus
        self._baseShapeKey = self._chooseShape() # this is the shape from whitch the cell is drawn
        self._multiplier = np.random.uniform(low = 0.37, high = 0.8, size = (1,)) # this multiplies is used for determing the height(second side) of the rectangle; given the way the paint event works, if the random multiplier were to be calculated in the draw methods, it would keep getting change at every call and make a very chaotic drawing
        self._baseShape = None # the base shape of the cell 
        self._circles = [] # here will be saved the circles drawn on the cell
        self._circNum = self._chooseNumberOfCircles() # chooses whether to draw one or two circles(and their symmetric counterparts)
        self._sidesWithCircles = [] # similar to the older turtle algorithm, it won't draw two circles on the same side    
        ##

        self._createShape() # creates the base shape

        ## VARIABLES DIRECTLY RELATED TO THE CREATION OF THE FINAL ITEM(AND TO THE ITEM ITSELF)
        self._prepCircles(0, 0) # this methods prepares the circles for being drawn and adds them to the scene, after they are prepared
        self.setPolygon(self._createPoly()) # the Final Item of the Cell becomes
        initPos = QtCore.QPointF(rand.randrange(200, 601), rand.randrange(200, 601))
        self._originPoint = initPos
        self.setPos(initPos.x(), initPos.y())
        self.setBrush(QtGui.QBrush(QtGui.QColor("skyblue")))
        self._height = None # the height of the Final Shape(and Final Item)
        self._width = None
        self._topLeftPoint = None # the top-left point of the Final Shape
        ##
        # for rotation
        #self.rotateBy(360 * 3)

        ## VARIABLES DIRECTLY RELATED TO CELL MOVEMEMNT
        self._timeDir = QtCore.QTimer() # this timer is used for storing the time during which the cell moves in a certain direction
        self._timeDir.setSingleShot(True) # sets the timer to work only as a single shot
        self._movementFrameTime = QtCore.QTime() # this clock will be used for determining the elapsed time between calls of the move method
        self._turnTime = QtCore.QTime() # this clock will be used to count the second during which a cell turns
        self._turnTime.start()

        self._actionRadius = self.height() + self.width() # this is the radius in which the cell can sense things 
        self._actionRadiusCirc = None # this is the graphics item made with the action radius
        ##

        ### FROM HERE ON START THE A.I.-RELATED VARIABLES
        ## THESE ARE VARIABLES THAT ARE DIRECTLY TIED TO EVOLUTION
        # this checks if this cell has parents
        if parents == None:
            self.size = self._area
            self.speedFactor = rand.uniform(-0.1, 0.1) 
            self.hunger = 1.0
            self.hungerTime = QtCore.QTime()
            self.lifeSpawn = (20 - self.speedFactor * 20) * 1000 
            self.speed = 1 / (self.size ** 2) * 1000 + self.speedFactor + 1 / (1 + self.hunger)
            self.kills = 0
            self.algae = 0
            self.secondsAlive = 0
            self.survivability = 0
            self.initFoodPref = 0.5
            self.actualFoodPref = 0
        else:
            self.buildFromParents(parents)
        ##

        ## THESE ARE A.I.-RELATED VARS THAT ARE NOT TIED TO EVOLUTION
        self._prey = None # this is the prey the cell locked on for eating
        self._alga = None # this is the alga it wants to eat
        self.dead = False
        ##


    #boundinGRect override
    def boundingRects(self):
        bounds = QtCore.QRectF(self.actualPos().x() - self.pos().x(), self.actualPos().y() - self.pos().y(),
                               self.width(), self.height())
        return bounds


    ### INTERNAL LOGIC OF THE CELL STARTS  HERE
        
    # METHODS FOR CHOOSING SOME RANDOM VALUES
    def _chooseShape(self):
        return rand.randrange(1, 4)

    def _chooseNumberOfCircles(self):
        return rand.randrange(1, 3)

    # METHODS FOR CHOOSING THE SIDE ON WHICH TO DRAW
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
    
    # HERE END THE METHODS FOR CHOOSING SOME RANDOM VALUES


    # MISCELLANEOUS METHODS  

    # this method should only be called after the Final Shape is done
    # it returns the height of the Final Shape(which will, most likely, be distinct from the height of the Base Shape)
    def height(self):
        if self._height == None: # if this is the first time the height is calculated
            heightVal = 0
            if self._baseShapeKey == BaseShape.Square.value or self._baseShapeKey == BaseShape.Rect.value:
                heightVal += self._baseShape.rect().height()
            else: # in the case the Base Shape is a rhombus
                heightVal += self._baseShape.polygon()[2].y() - self._baseShape.polygon()[0].y()
         
            index = 0
            for circle in self._circles:
                side = self._sidesWithCircles[index]
                if side == 1 or side == 3:
                    if self._baseShapeKey == BaseShape.Square.value or self._baseShapeKey == BaseShape.Rect.value:
                        heightVal += self._circles[index].rect().height() / 2 # adds the radius of the circle
                        break
                # in the case of a rhombus, the circles might not affect the width or the height at all
                if self._baseShapeKey == BaseShape.Rhomb.value:
                    if circle.rect().y() < self._baseShape.polygon()[0].y():
                        if index % 2 == 0: # if it is an outer circle
                            heightVal += abs(self._baseShape.polygon()[0].y() - circle.rect().y()) 
                    elif circle.rect().y() + circle.rect().height() > self._baseShape.polygon()[2].y():
                        if index % 2 == 0: # if it is an outer circle
                            heightVal += abs(circle.rect().y() + circle.rect().height()  - self._baseShape.polygon()[2].y())
                index += 1
            
            self._height = heightVal # set the Cell height to the heightVal that was just calculated
            return heightVal
        else: # dont do the calculations more than once
            return self._height

    # same as before, but for width
    def width(self):
        if self._width == None: # same as for the height
            widthVal = 0
            if self._baseShapeKey == BaseShape.Square.value or self._baseShapeKey == BaseShape.Rect.value:
                widthVal += self._baseShape.rect().width()
            else: # in the case the Base Shape is a rhombus
                widthVal += self._baseShape.polygon()[1].x() - self._baseShape.polygon()[3].x()
         
            index = 0
            for circle in self._circles:
                side = self._sidesWithCircles[index]
                if side == 2 or side == 4:
                    if self._baseShapeKey == BaseShape.Square.value or self._baseShapeKey == BaseShape.Rect.value:
                        widthVal += self._circles[index].rect().height() / 2 # adds the radius of the circle
                        break
                # in the case of a rhombus, the circles might not affect the width or the height at all
                if self._baseShapeKey == BaseShape.Rhomb.value:
                    if circle.rect().x() < self._baseShape.polygon()[3].x():
                        if index % 2 == 0: # if it is an outer circle
                            widthVal += abs(self._baseShape.polygon()[3].x() - circle.rect().x())
                    elif circle.rect().x() + circle.rect().width() > self._baseShape.polygon()[1].x():
                        if index % 2 == 0: # if it is an outer circle
                            widthVal += abs(circle.rect().x() + circle.rect().width()  - self._baseShape.polygon()[1].x())
                index += 1

            self._width = widthVal
            return widthVal
        else:
            return self._width


    # this method returns two circles made with QGraphicsEllipseItem
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


    # this method does everything needed for the pre-creation of the circles, such as choosing the coordinates, the radius and so on
    # sideLen refers to the length of the sidesWithCircles list
    # soFar represents the ammount of circles added so far
    # app is a MLCellApp object
    def _prepCircles(self, sideLen, soFar):
        if soFar >= self._circNum: # if there have been added enough circles, stop the method
            return 
        self._chooseSide() # pretty obvious, chooses a side
        checkForBreak = self._circNum
        coords = self._chooseCoords(self._sidesWithCircles[sideLen]) # chooses the coords; the rhomb will return some coords ON the rhomb, not the coords of the top-left point
        if checkForBreak != self._circNum: # if circNum is changed, that means there was no space for a circle of minimum radius of 60
            return 
        radius = self._chooseRadius(self._sidesWithCircles[sideLen], coords[0], coords[1], coords[2], coords[3], coords)
        newCoords = [coords[0], coords[1], coords[2], coords[3]] # given that lists are mutable, writing newCoords = coords would make any change to coords or newCoords apply to both lists, which is the opposite of what should happen here
        self._resetCoords(None, None, None, None, self._sidesWithCircles[sideLen], radius, coords, newCoords)

        circle, opCircle = self._makeCircle(self._sidesWithCircles[sideLen], newCoords[0], newCoords[1], newCoords[2], newCoords[3], radius)
        self._circles.append(circle) # the code should've been pretty straightforward so far
        self._circles.append(opCircle)
        self._prepCircles(len(self._sidesWithCircles), soFar + 1) # the recursive call makes sure all circles are added

    # this method works as a nice wrapper  for the actual chooseRadius methods
    def _chooseRadius(self, side, sidex, sidey, opsidex, opsidey, coords):
        if self._baseShapeKey == BaseShape.Square.value or self._baseShapeKey == BaseShape.Rect.value: # in this case, the method is literally identical
            return self._chooseRadiusSquareOrRect(side, sidex, sidey, opsidex, opsidey, coords)
        else:
            return self._chooseRadiusRhomb(side, sidex, sidey, opsidex, opsidey)

    # this is a wrapper for resetCoords methods
    def _resetCoords(self, sidex, sidey, opsidex, opsidey, side, radius, coords = None, newCoords = None):
        if self._baseShapeKey == BaseShape.Square.value or self._baseShapeKey == BaseShape.Rect.value:
            self._resetCoordsSquareOrRect(sidex, sidey, opsidex, opsidey, side, radius, coords, newCoords)
        else:
            self._resetCoordsRhomb(side, radius, coords, newCoords)
            

    # returns all four points of the Base Shape, starting from the top-left clockwise
    def _getPoints(self):
        if self._baseShapeKey == BaseShape.Rect.value or self._baseShapeKey == BaseShape.Square.value:
            return self._getSquareOrRectPoints()
        else:
            return self._getRhombPoints()
    
    # returns the index of a circle in the self._circles list on the side given by the "side" parameter
    def _findCircle(self, side):
        index = 0
        for circle in self._circles:
            if self._sidesWithCircles[index] == side:
                return index
            index += 1
        return -1 # if no circle was found, the program returns -1

    # this method will return the nearest point on a line from a specified point
    def _nearestPoint(self, point, line):
        perpLine = QtCore.QLineF(point.x(), point.y(), point.x(), 0.0)
        perpLine.setAngle(90 + line.angle()) # rotates the new line in such a way that it becomes perpendicular on the old line
        interPoint = QtCore.QPointF(0, 0)
        line.intersect(perpLine, interPoint)
        return interPoint
    # this method will calculate the distance between a line and a point in a clever way
    def _disToLine(self, point, line):
        interPoint = self._nearestPoint(point, line) # looks for the nearest point on the line
        return QtCore.QLineF(point, interPoint).length() # returns the length of the line from this point to the nearest point


    # this method checks the collision between circles drawn "inside" the shape
    def _checkCircleColl(self, radius, circle, opCircle):
        otherCircCenter = circle.rect().center() # center of the circle variable from the loop
        otherCircRadius = circle.rect().height() / 2 # the circle rect is a square (otherwise it would be an ellipse, not a circle)

        opCircleCenter = opCircle.rect().center()
        opCircleDist = QtCore.QLineF(otherCircCenter, opCircleCenter).length()
        if circle.collidesWithItem(opCircle):
            if radius + otherCircRadius > opCircleDist:
                radius = opCircleDist - otherCircRadius # this isn't exactly correct, but a proper method would bloat the code even more; this is more detailed in the wiki
        return radius if radius > 0 else 0
    # HERE END THE MISCELLANEOUS METHODS

    # METHODS FOR CHOOSING THE COORDS AND THE RADIUS FOR THE SEMI-CIRCLES
    def _chooseCoords(self, side): # randomly chooses some coords that can draw a circle of minimum radius of 60 on the given side
        if self._baseShapeKey == BaseShape.Square.value:
            return self._chooseCoordsSquareOrRect(side, 1) # minimum 20 radius for squares
        elif self._baseShapeKey == BaseShape.Rect.value:
            return self._chooseCoordsSquareOrRect(side, min(60, self._sides[0] / 2 - 1, self._sides[1] / 2 - 1))
        else:   # for the rhombus
            return self._chooseCoordsRhomb(side, 1)

    # under this are the 3 methods for squares and rects, they are essentially identical

    # !!READ THIS!!
    # this method is the same for both the square and the rect, because the only difference whatsoever between them is the way the radius
    # is calculated(for the square the minimum radius is set in the _chooseCoords method, while for the rect it can be smaller, depending on the width and height)
    # this can be easily solved by passing the radius as a parameter
    def _chooseCoordsSquareOrRect(self, side, radius): # this method will return a list of the top-left coords of the rects of the both circles
        
        sideX = sideY = opSideX = opSideY = 0 # these are the top left coords of the circle on this side and on the opposite side
        foundGoodCoords = False
        tries = 0
        while foundGoodCoords == False:
            foundGoodCoords = True

            if tries >= 1000: # if the loop is executed this many times, it almost surely means there is no space for a circle of minimum radius
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
    
    # this method finds the biggest possible radius starting from the given coords
    # just as before, this method would look literally the same for a rectangle
    def _chooseRadiusSquareOrRect(self, side, sidex, sidey, opsidex, opsidey, coords):

        xPos = self._baseShape.rect().x() # x position of the square
        height = self._baseShape.rect().height() 
        width = self._baseShape.rect().width()
        yPos = self._baseShape.rect().y() # y position of the square
        minDim = min(height, width) # this variable is only useful when this method is called for a rectangle, the radius should not exceed the smaller value of the two
        
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
                oldRadius = actualRadius
                actualRadius = self._checkCircleColl(actualRadius, circle, opCircle)
                if side == 1 or side == 3:
                    sidex += oldRadius - actualRadius
                    opsidex += oldRadius - actualRadius
                else:
                    sidey += oldRadius - actualRadius
                    opsidey += oldRadius - actualRadius
                # updating the coordinates if anything changed
                if oldRadius != actualRadius:
                    coords[0] = sidex
                    coords[1] = sidey
                    coords[2] = opsidex
                    coords[3] = opsidey
            index += 1
        # here ends this for loop
        return actualRadius 

    # this methods resets the "fixed" coords of the circles based on the radius parameter
    # what I mean by "fixed" coords are the coords that are constant on a given side, ie the y coords on side 1(or side 3)
    # again, the method for the square and rect is one and the same
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

    # returns all four points of a Square or a Rectangle, starting from the top-left in a clockwise direction
    def _getSquareOrRectPoints(self):
        shape = self._baseShape.rect()
        return shape.topLeft(), shape.topRight(), shape.bottomRight(), shape.bottomLeft()


    # this algorithm is a bit weirder, given the nature of rhombuses, from the points chosen by this method it might still not be possible
    # for a circle of specified radius to be drawn, due to the way rhombuses' "inwards" are. oof this doesn't really makes sense, does it
    # it should be noted that it returns the coordinates projected on the rhombus, not of the rectangle in which the ellipse is included
    # to further clarify the last comment, the method returns the coordinates of the center of the circle(which are on one of the rhomb's
    # sides)
    def _chooseCoordsRhomb(self, side, radius):
        
        sideX = sideY = opSideX = opSideY = 0
        noSmallCircs = 0 # this constant is irrelevant for smaller cells, but it is kept in the code for the sake of compatibility
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
        maxPosRadNoCircs = dist # as in the other method, this is the biggest possible radius if there were no other circles drawn
       

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


        
    # this does what the other method for the square does, except that in a slightly more compelx manner
    def _resetCoordsRhomb(self, side, radius, coords, newCoords):
        if coords is None:
            assert False # this will return an error

        if newCoords is not None:
            newCoords[0] = coords[0] - radius # this assumes that the coordinates passed by the coords list are the coordinates of the center of the circle
            newCoords[1] = coords[1] - radius
            newCoords[2] = coords[2] - radius
            newCoords[3] = coords[3] - radius
        else:
            assert False # this will return an error, this method would be too tirseome to implement without the use of lists

    # UNDER HERE ARE METHODS MADE SPECIFICALLY FOR THE RHOMBUS
    # SO FAR, THERE ARE ONLY 3 OF THEM
    # this method will return all the points of the rhombus polygon
    def _getRhombPoints(self):
        poly = self._baseShape.polygon()
        return poly[0], poly[1], poly[2], poly[3]
    # this method will return all the lines of the rhombus polygon
    def _getRhombLines(self):
        poly = self._baseShape.polygon()
        p1, p2, p3, p4 = self._getRhombPoints()

        l1 = QtCore.QLineF(p1, p2)
        l2 = QtCore.QLineF(p2, p3)
        l3 = QtCore.QLineF(p3, p4)
        l4 = QtCore.QLineF(p4, p1)
        return l1, l2, l3, l4

    # this method finds the smallest distances from this point to all of the rhombus' lines and then returns the smallest of these
    def _smallestDistRhomb(self, point, side):
        line1, line2, line3, line4 = self._getRhombLines()
        dist1 = self._disToLine(point, line1) if side != 1 else line1.length() * 1000 # calculates the minimum distance to every line, keeping both circles in mind
        dist2 = self._disToLine(point, line2) if side != 2 else line1.length() * 1000
        dist3 = self._disToLine(point, line3) if side != 3 else line1.length() * 1000
        dist4 = self._disToLine(point, line4) if side != 4 else line1.length() * 1000

        smolDist = min(dist1, dist2, dist3, dist4) # finds the absolute smalles distance to any line on the rhombus
        return smolDist

    # HERE END THE METHODS FOR CHOOSING THE COORDS AND THE RADIUS FOR THE SEMI-CIRCLES
                

    # METHODS THAT MANAGE CREATING THE BASE SHAPE
    # this method draws the base shape
    def _createShape(self):
        if self._baseShapeKey == BaseShape.Square.value:
            self._createSquare()
        elif self._baseShapeKey == BaseShape.Rect.value:
            self._createRect()
        else:
            self._createRhomb()

    def _createRhomb(self):

        self._sides[0] = self._sides[1] = math.sqrt(self._area / np.sin(np.deg2rad(self._angle))) # same way we used to build rhombs\rhombuses in the old program
        side = self._sides[0]

        rhombus = QtWidgets.QGraphicsPolygonItem()
        rhombPoly = QtGui.QPolygonF()
        rhombPoly.append(QtCore.QPointF(np.sin(np.deg2rad(self._angle / 2)) * side, 0))
        rhombPoly.append(QtCore.QPointF(2 * np.sin(np.deg2rad(self._angle / 2)) * side, np.cos(np.deg2rad(self._angle / 2)) * side))
        rhombPoly.append(QtCore.QPointF(np.sin(np.deg2rad(self._angle / 2)) * side, 2 * np.cos(np.deg2rad(self._angle / 2)) * side))
        rhombPoly.append(QtCore.QPointF(0, np.cos(np.deg2rad(self._angle / 2)) * side))
        rhombus.setPolygon(rhombPoly)
        self._baseShape = rhombus


    def _createRect(self):
        self._sides[1] = math.sqrt(self._area) * self._multiplier[0] 
        self._sides[0] = self._area / self._sides[1]
        initPos = QtCore.QPointF(rand.randrange(200, 601), rand.randrange(200, 601))

        self._baseShape = QtWidgets.QGraphicsRectItem(0, 0, self._sides[0], self._sides[1])

    def _createSquare(self):
        self._sides[0] = self._sides[1] = math.sqrt(self._area)
        initPos = QtCore.QPointF(rand.randrange(200, 601), rand.randrange(200, 601))

        self._baseShape = QtWidgets.QGraphicsRectItem(0, 0, self._sides[0], self._sides[1])
           
    # HERE END THE CREATION MANAGEMENT METHODS


    # THE METHODS FROM HERE ON DEAL WITH CREATING THE FINAL SHAPE POLYGON

    # this method returns a list of all the points needed to draw the corresponding semi-circle
    def _getCirclePoints(self, circIndex):
        points = [] # this list will contain all the poins of the given semi-circle
        circle = self._circles[circIndex] # the corresponding circle
        angle = circle.startAngle() + (180 * 16 if circIndex % 2 == 0 else 0) # this will be explained in the wiki, it would take too many words to be explained here
        circleCenter = circle.rect().center()
        radius = circle.rect().height() / 2

        # add every point on the circle, one by one
        radiusLine = QtCore.QLineF()
        radiusLine.setP1(circleCenter)
        radiusLine.setLength(radius)
        radiusLine.setAngle(angle / 16)

        for addAngle in range(1, 180 * 16 + 1):
            lastPoint = radiusLine.p2()
            points.append(lastPoint)
            angle = angle - (1 if circIndex % 2 == 0 else -1) # same as the previous conditional expression(it is explained in the wiki)
            radiusLine.setAngle(angle / 16)

        return points

    # adds a semi-circle to the polygon of the final shape
    def _addCirclePoints(self, side, poly):
        nextCircleIndex = self._findCircle(side) # searches for this side
        if nextCircleIndex >= 0: # if the index is greater than equal to 0, it means that the program could find a circle on this side
            circPoints = self._getCirclePoints(nextCircleIndex)
            for point in circPoints:
                poly.append(point)


    # this method returns a QPolygonF object that is essentially the final shape that the Cell should have
    def _createPoly(self):
        poly = QtGui.QPolygonF()
        
        # the points start from the top-left one and go up to the bottom-left one, clockwise
        p1, p2, p3, p4 = self._getPoints()

        # add the first point
        poly.append(p1)
        self._addCirclePoints(1, poly)
        
        # adds the second point
        poly.append(p2)
        self._addCirclePoints(2, poly)

        # third point
        poly.append(p3)
        self._addCirclePoints(3, poly)

        # last point
        poly.append(p4)
        self._addCirclePoints(4, poly)

        return poly
    
    # HERE END THE METHODS THAT DEAL WITH CREATING THE FINAL SHAPE POLYGON


    ### INTERNAL LOGIC OF THE CELL ENDS HERE

    
    ### EXTERNAL LOGIC STARTS HERE
    
    # METHOD FOR RESETING THE ORIGIN POINT
    def resetOrigin(self, origin):
        self._originPoint = origin



    # MISCELLANEOUS METHODS

    # start the hunger clock; this function comes in handy for the class method that makes all the cells move
    def startHungerClock(self):
        self.hungerTime.start()

    # start the frame clock; this function comes in handy for the class method that makes all the cells move
    def startFrameClock(self):
        self._movementFrameTime.start()

    # checks if another cell is very close to this cell
    def _cellIsInVicinity(self, otherCell):
        if otherCell is self: # if they are the same cell
            return False
        extendedX = self.actualPos().x() # the extended things represent the dimensions and coordinates
        extendedY = self.actualPos().y() # of the vicinity
        extendedWidth = self.width() # the vicinity will extend by the cell's dimensions
        extendedHeight = self.height()

        otherX = otherCell.actualPos().x() # the coordinates and dimensions of the other cell
        otherY = otherCell.actualPos().y()
        otherWidth = otherCell.width()
        otherHeight = otherCell.height()

        # EXPERIMENTAL - MIGHT PROVE TO BE VERY SLOW
        # 26.09.2019 - IT PROVED TO BE QUITE FAST
        vicinity = QtCore.QRectF(extendedX, extendedY, extendedWidth, extendedHeight)
        otherArea = QtCore.QRectF(otherX, otherY, otherWidth, otherHeight)
        # checks all four corners
        if vicinity.contains(otherArea.topLeft()) or vicinity.contains(otherArea.topRight())\
        or vicinity.contains(otherArea.bottomLeft()) or vicinity.contains(otherArea.bottomRight()):
            return True
        return False

    # rotation thingy
    def rotateBy(self, degrees):
        self.setTransformOriginPoint(self.boundingRect().center().x(), selfboundingRect().center().y())
        timer = QtCore.QTimer()
        if degrees < 5:
            self.setRotation(self.rotation() + degrees)
        else:
            self.setRotation(self.rotation() + 5)
            timer.singleShot(16, lambda: self.rotateBy(degrees - 5))

    # METHODS FOR POSITIONS AND STUFF RELATED TO POSITIONS

    # i have no idea what the pos() of a polygon graphics item is; either way this looks in the polygon's points
    # and finds its extremities. im adding self.pos() to every point because the points' coordonate system is in relation
    # to the original graphics item(ie the Final Item), not the scene itself
    def actualPos(self):
        if self._topLeftPoint == None: # if the top-left point has not been yet determined
            topY = 1000
            yPos = self.pos().y() # the position of the cell might slightly change during the for loop, which makes the function return all kinds of weird results
            for point in self.polygon():
                if point.y() + yPos < topY:
                    topY = point.y() + yPos

            leftX = 1000
            xPos = self.pos().x()
            for point in self.polygon():
                if point.x() + xPos < leftX:
                    leftX = point.x() + xPos

            self._topLeftPoint = QtCore.QPointF(leftX - xPos, topY - yPos)
            return QtCore.QPointF(leftX, topY)
        else:
            return QtCore.QPointF(self._topLeftPoint.x() + self.pos().x(), self._topLeftPoint.y() + self.pos().y())

    # this method takes coordinates for the actualPosition and translates them to regular position of the item
    # note that I genuinely have no idea what the regular position of the item actually is, Qt can get really
    # weird
    def setActualPos(self, x, y):
        itemPos = self.pos()
        actualPos = self.actualPos()

        x -= actualPos.x() - itemPos.x()
        y -= actualPos.y() - itemPos.y()
        self.setPos(x, y)
        if self._actionRadiusCirc is not None: # while the cells are being reset, they sometimes change their actual position and, obviously, the action radius is None at the time
            circCenterX = self.actualPos().x() + self.width() / 2 # set the radius circle's position, too
            circCenterY = self.actualPos().y() + self.height() / 2
            self._actionRadiusCirc.setPos(circCenterX - self._actionRadius, circCenterY - self._actionRadius)
    
    # HERE END METHODS FOR POSITIONING 


    # HERE START METHODS RELATED TO MOVING THE CELL
    
    def _chooseDir(self):
        return rand.randrange(0, 360)

    # this method will be sort of an update loop
    def updateLoop(self, dirAngle = 0):
        # due to the weird way names work in python, there might be left some names of this cell even after it was killed
        # so this kills them all
        if self.dead == True:
            del self
            return

        # check if the cell died of hunger
        if self.hunger <= 0:
            self.die()
            return # stop the update loop
        # update the speed 
        self._updateSpeed()
        # hunger percentage
        self.hunger -= self._movementFrameTime.elapsed() / self.lifeSpawn

        # if someone else ate its prey
        if self._prey is not None and (not util.itemIsInScene(self.scene(), self._prey) or self._prey.dead == True):
            self._prey = None
            self.setBrush(QtGui.QBrush(QtGui.QColor("skyblue"))) 
        # if someone else ate its alga
        if self._alga is not None and (not util.itemIsInScene(self.scene(), self._alga) or self._alga.dead == True):
            self._alga = None
            self.setBrush(QtGui.QBrush(QtGui.QColor("skyblue"))) 


        if self._timeDir.isActive() == False and self._turnTime.elapsed() >= 250 and self._prey is None: # if the timer has not started yet or if it has stopped
            dirAngle = self._chooseDir()
            self._timeDir.start(rand.randrange(3, 5) * 1000)
        if self._turnTime.elapsed() >= 250 and self._prey is not None:
            dirAngle = QtCore.QLineF(self.actualPos(), self._prey.actualPos()).angle()
        if self._turnTime.elapsed() >= 250 and self._alga is not None:
            dirAngle = QtCore.QLineF(self.actualPos(), self._alga.pos()).angle()
        
        # if it somehow ends up outside the scene(if the time between two frames is huge, this might happen)
        if self.actualPos().x() <= 0 or self.actualPos().x() >= 1000:
            self.setActualPos(self._originPoint.x(), self._originPoint.y())
        elif self.actualPos().y() <= 0 or self.actualPos().y() >= 1000:
            self.setActualPos(self._originPoint.x(), self._originPoint.y())

        timeElapsed = self._movementFrameTime.restart() / 20 # the timeElapsed is used for keeping the speed constant
        if self._turnTime.elapsed() >= 250:
            self._moveInDir(timeElapsed, dirAngle)
        else:
            self._moveInDir(timeElapsed, dirAngle + 180)
        
        # check radius
        self._checkRadius(self.scene())

        # check for collisions
        self._checkCol(dirAngle)

        tempTimer = QtCore.QTimer() # this timer only serves to call the movement loop back
        tempTimer.singleShot(20, lambda: self.updateLoop(dirAngle))


    # method for updating the speed
    def _updateSpeed(self):
        self.speed = 1 / (self.size ** 2) * 1000 + self.speedFactor + 1 / (1 + self.hunger)

    # moves the Final Item in the direction given by the angle
    def _moveInDir(self, timeElapsed, angle):
        startPoint = QtCore.QPointF(0.001, 0.001)
        lineDir = QtCore.QLineF() # im using the line trick again, it's just so much better than doing the maths

        lineDir.setP1(startPoint)
        lineDir.setLength(1 * timeElapsed * self.speed)
        lineDir.setAngle(angle)

        self.moveBy(lineDir.p2().x(), lineDir.p2().y())
        self._actionRadiusCirc.moveBy(lineDir.p2().x(), lineDir.p2().y())

    # METHODS FOR DETECTING AND HANDLING COLLISIONS


    def _checkCol(self, angle):
        scene = self.scene() # the qgraphicsscene in which this cell is contained
        if scene is None: # the cell is added to the scene only AFTER it is created, so for some brief time it might not be added to any scene yet
            return 
        checkCellCol = True
        if self._turnTime.elapsed() <= 250: # during the turning time, no collision shall be checked
            checkCellCol = False
        for item in scene.items():
            if util.getClassName(item) == "Wall":
                if self.collidesWithItem(item):
                    self._handleWall(item) # this method pushes the cell out of the walls
            elif util.getClassName(item) == "Cell":
                if checkCellCol and self._cellIsInVicinity(item): # if it is not turning
                    self._turnTime.restart()
                    checkCellCol = False
                    if item == self._prey:
                        self._fightCell()
            elif util.getClassName(item) == "Alga":
                if self._algaIsInVicinity(item):
                    self._handleAlga(item) # similar to the wall, it pushes the cell out of the alga
                    if item == self._alga:
                        self._eatAlga()
       
    # move the cell outside the wall   
    def _handleWall(self, wall):
        if wall.side() == 1:
            self.setActualPos(self.actualPos().x(), wall.wallX() + wall.wallHeight() + 4) # adds one so they don't end up tangent
        elif wall.side() == 2:
            self.setActualPos(wall.wallX() - self.width() - 4, self.actualPos().y())
        elif wall.side() == 3:
            self.setActualPos(self.actualPos().x(), wall.wallY() - self.height() - 4)
        elif wall.side() == 4:
            self.setActualPos(wall.wallX() + wall.wallWidth() + 4, self.actualPos().y())

    # checks if the cell is too close to an alga
    def _algaIsInVicinity(self, alga):
        extendedX = self.actualPos().x() # the extended things represent the dimensions and coordinates
        extendedY = self.actualPos().y() # of the vicinity
        extendedWidth = self.width() # the vicinity will extend by the cell's dimensions
        extendedHeight = self.height()

        vicinity = QtCore.QRectF(extendedX, extendedY, extendedWidth, extendedHeight)
        algaArea = QtCore.QRectF(alga.x(), alga.y(), alga.radius() * 2, alga.radius() * 2)
        if vicinity.intersects(algaArea):
            return True
        return False

    # move the cell outside the alga
    def _handleAlga(self, alga):
        algaCenter = QtCore.QPointF(alga.x() + alga.radius(), alga.y() + alga.radius())
        cellPos = self.actualPos()
        lineHit = QtCore.QLineF(algaCenter, cellPos)
        hitAngle = lineHit.angle()

        lineDist = QtCore.QLineF() # line trick yet again
        lineDist.setP1(algaCenter)
        lineDist.setAngle(hitAngle)
        lineDist.setLength(lineHit.length() + 5)

        newPos = lineDist.p2()
        self.setActualPos(newPos.x(), newPos.y())

    # METHODS FOR DETECTING AND HANDLING COLLISIONS END HERE

    # METHOD FOR INITIALIZING THE RADIUS

    # returns the circle radius
    def createActionRadCirc(self):
        centerX = self.actualPos().x() + self.width() / 2 # the centerish of the Cell
        centerY = self.actualPos().y() + self.height() / 2

        circle = QtWidgets.QGraphicsEllipseItem(0, 0, self._actionRadius * 2, self._actionRadius * 2)
        circle.setPos(centerX - self._actionRadius, centerY - self._actionRadius) # coordinate trick
        self._actionRadiusCirc = circle 
        
    # METHODS FOR INITIALIZING THE RADIUS END

    # METHODS FOR EATING STUFF

    # returns the length from the first point of the first line to the second line
    def _lenToLine(self, line1, line2):
        interPoint = QtCore.QPointF()
        intersects = line1.intersect(line2, interPoint)
        if intersects == 0: # if they dont intersect
            return 999999 # return a very high value if they are parallel
        return QtCore.QLineF(line1.p1(), interPoint).length()

    # returns the distance to the point on the intersection between the given line and the closest side of a given rect
    def _nearestPointOnRectDist(self, rect, line):
        p1 = rect.topLeft()
        p2 = rect.topRight()
        p3 = rect.bottomRight()
        p4 = rect.bottomLeft()

        line1 = QtCore.QLineF(p1, p2)
        line2 = QtCore.QLineF(p2, p3)
        line3 = QtCore.QLineF(p3, p4)
        line4 = QtCore.QLineF(p4, p1)

        return min(self._lenToLine(line, line1), self._lenToLine(line, line2), self._lenToLine(line, line3),\
                    self._lenToLine(line, line4))
        

        
    # this checks if the item(other cell) intersects with the radius
    def _cellIntersectRadius(self, item):
        circCenterX = self._actionRadiusCirc.x() + self._actionRadius
        circCenterY = self._actionRadiusCirc.y() + self._actionRadius

        itemCenterX = item.actualPos().x() + item.width() / 2
        itemCenterY = item.actualPos().y() + item.height() / 2
    
        distLine = QtCore.QLineF(QtCore.QPointF(itemCenterX, itemCenterY), QtCore.QPointF(circCenterX, circCenterY))
        totLen = distLine.length() # total length between the two centers
        cellRect = QtCore.QRectF(0, 0, item.width(), item.height())
        cellRect.setTopLeft(item.actualPos())
        cellDist = self._nearestPointOnRectDist(cellRect, distLine) # distance from rect center to whatever rect side the line intersects
        if cellDist + self._actionRadius > totLen:
            return True
        return False
    # this checks if the item(alga) intersects with the radius
    def _algaIntersectRadius(self, item):
        circCenterX = self._actionRadiusCirc.x() + self._actionRadius
        circCenterY = self._actionRadiusCirc.y() + self._actionRadius

        itemCenterX = item.pos().x() + item.rect().width() / 2
        itemCenterY = item.pos().y() + item.rect().height() / 2
    
        distLine = QtCore.QLineF(QtCore.QPointF(itemCenterX, itemCenterY), QtCore.QPointF(circCenterX, circCenterY))
        totLen = distLine.length() # total length between the two centers
        if item.rect().height() / 2 + self._actionRadius > totLen: # the action radius and the alga radius
            return True
        return False

    # this checks which items are inside the radius and handles them
    def _checkRadius(self, scene):
        if scene is None: # if the cell wasn't added in the scene or the scene doesn't exist
            return

        if self.hunger <= 0.8 and self._prey is None and self._alga is None: # only search for food when it is kinda hungry and when it isn't already lock on something
            maxFood = 0 # find out the best thing it can eat
            maxItem = None
            for item in scene.items():
                if util.getClassName(item) == "Cell" and item is not self:
                    if self._cellIntersectRadius(item):
                        foodPoints = 0
                        foodPoints += self.size / item.size * 100 # this is how much damage it can deal to the other cell
                        foodPoints += self.initFoodPref * 100
                        if foodPoints > Cell.EAT_CELL_THRESHOLD and maxFood < self.size / item.size:
                            maxFood = self.size / item.size
                            maxItem = item
                elif util.getClassName(item) == "Alga":
                    if self._algaIntersectRadius(item):
                        foodPoints = item.size / self.size
                        foodPoints -= self.initFoodPref / 2
                        if foodPoints > 0 and maxFood < item.size / self.size:
                            maxFood = item.size / self.size
                            maxItem = item
            
            
            if maxItem is not None and util.getClassName(maxItem) == "Cell":
                self._prey = maxItem
                self.setBrush(QtGui.QBrush(QtGui.QColor("red")))
            elif maxItem is not None and util.getClassName(maxItem) == "Alga":
                self._alga = maxItem
                self.setBrush(QtGui.QBrush(QtGui.QColor("green")))
                
               

    def _fightCell(self):
        if self.dead == True: # the name thing
            return
        self.hunger += self._prey.size / self.size
        if self.hunger > 1:
            self.hunger = 1
        # kill the prey
        self._prey.die()
        self._prey = None
        self.setBrush(QtGui.QBrush(QtGui.QColor("skyblue")))
        self.kills += 1

    def _eatAlga(self):
        if self.dead == True: # the name thing
            return
        self.hunger += self._alga.size / self.size
        if self.hunger > 1:
            self.hunger = 1
        # kill the alga
        self._alga.die()
        self._alga = None
        self.setBrush(QtGui.QBrush(QtGui.QColor("skyblue")))
        self.algae += 1
            

    # METHOD FOR DYING
    def die(self):
        if self.dead == True:
            return
        # calculate all the post-mortem variables
        self.secondsAlive = self.hungerTime.elapsed()
        self.survivability = self.secondsAlive + max(self.kills, self.algae)
        self.actualFoodPref = self.kills / (self.algae + self.kills) if self.algae + self.kills > 0 else -1 # if it ate nothing, set its FP to -1

        # kill self
        self.scene().removeItem(self)
        self.dead = True
        cellInfo = CellData()
        cellInfo.setData(self.size, self.speedFactor, self.secondsAlive, self.kills, self.algae, self.survivability, self.initFoodPref, self.actualFoodPref)
        self._genData.addCellData(cellInfo)
        del self


    # METHOD FOR BUILDING A CELL BASED ON TWO GIVEN PARENTS
    def buildFromParents(self, parents):
        parent1 = parents[0]
        parent2 = parents[1]

        # choose the parent from which it take two traits and the one from which it takes one trait
        twoTraitsPar = rand.choice(parents)
        oneTraitPar = parent1 if parent2 == twoTraitsPar else parent2
        sizeDice = rand.choice([1, 2, 3])
        self.size = twoTraitsPar.data["size"] if sizeDice <= 2 else oneTraitPar.data["size"]
        if sizeDice == 3: # this means that the trait from the one trait parent was just used
            self.speedFactor = twoTraitsPar.data["speedFactor"]
            self.initFoodPref = twoTraitsPar.data["actualFoodPref"]
        else:
            speedFDice = rand.choice([1, 2])
            self.speedFactor = twoTraitsPar.data["speedFactor"] if speedFDice <= 1 else oneTraitPar.data["speedFactor"]
            if speedFDice == 2: # this means that the trait from the one trait parent was just used
                self.initFoodPref = twoTraitsPar.data["actualFoodPref"]
            else:
                self.initFoodPref = oneTraitPar.data["actualFoodPref"]
        self.hunger = 1.0
        self.hungerTime = QtCore.QTime()
        self.lifeSpawn = (20 + self.speedFactor * 20) * 1000 
        self.speed = 1 / (self.size ** 2) * 1000 + self.speedFactor + 1 / (1 + self.hunger)
        self.kills = 0
        self.algae = 0
        self.secondsAlive = 0
        self.survivability = 0
        self.actualFoodPref = 0
        self.mutate()

    # managing mutations for cells with parents
    def mutate(self):
        sizeMutate = rand.uniform(-10, 10)
        self.size += self.size * sizeMutate / 100
        if self.size < 30: # some evolution locks
            self.size = 30
        if self.size > 400:
            self.size = 400
        speedFMutate = rand.uniform(-10, 10)
        self.speedFactor += self.speedFactor * speedFMutate / 100
        initFPMutate = rand.uniform(-10, 10)
        self.initFoodPref += self.initFoodPref * initFPMutate / 100
    # EXTERNAL LOGIC ENDS HERE
