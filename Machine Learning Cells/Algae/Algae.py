import random as rand

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

from AlgaeBloom import Bloom
import util

class Alga(QtWidgets.QGraphicsEllipseItem):
    population = 0 # this will be the total Algae population inside the scene
    disjoint = 0 # similar to the disjoint class variable from the Cell class

    DESIRED_POP = 0 # this will be the desired population at every moment

    ALGAE_RAD = 10 # at the moment, all algae have the same radius

    @classmethod
    def resetAlgae(cls, scene, simDia = None, totalEntities = 0, soFar = 0):
        if scene is None: # if the scene object was not constructed, wait a bit for it(by recalling the function 10 ms later)
            reset = QtCore.QTimer()
            reset.singleShot(10, lambda: cls.resetAlgae(scene))
            return

        for item in scene.items():
            if util.getClassName(item) == "Alga":
                if item.collidingItems() != []:
                    cls.resetAlgaInit(scene, item)
                    cls.disjoint += 1
                    if simDia is not None:
                        simDia.loadNewSim.setValue((cls.disjoint + soFar) / totalEntities)
                else:
                    cls.disjoint += 1
                    if simDia is not None:
                        simDia.loadNewSim.setValue((cls.disjoint + soFar) / totalEntities)

    # this method works only at the init phase, in which the cells have not been drawn yet
    @classmethod
    def resetAlgaInit(cls, scene, alga):
    
            bloom = alga.bloom()
            bloomX = int(bloom.x())
            bloomY = int(bloom.y())
            bloomWidth = int(bloom.width())
            bloomHeight = int(bloom.height())
            allCoords = list(range(bloomX, bloomX + bloomWidth))
            allCoords = [allCoords] * bloomHeight # create a bloomHeight x bloomWidth matrix with all possible positions

            for item in scene.items():
                if util.getClassName(item) == "Alga" and item is not alga:
                    yStart = item.pos().y() - alga.radius() * 2 # the bounds in which this alga cannot spawn 
                    yStop = item.pos().y() + item.radius() * 2 # in refernence to the alga it is currently checking
                    if yStart <= bloomY:
                        yStart = bloomY
                    if yStop >= bloomY + bloomHeight:
                        yStop = bloomY + bloomHeight
                    xStart = item.pos().x() - alga.radius() * 2
                    xStop = item.pos().x() + item.radius() * 2
                    if xStart <= bloomX:
                        xStart = bloomX
                    if xStop >= bloomX + bloomWidth:
                        xStop = bloomX + bloomWidth

                    yStart = int(yStart) # given that they might probably end up with floating coordinates 
                    yStop = int(yStop) # they should be casted to whole numbers
                    xStart = int(xStart)
                    xStop = int(xStop)
                    for i in range(yStart - bloomY, yStop - bloomY): 
                        for j in range(xStart - bloomX, xStop - bloomX):
                            allCoords[i][j] = -1 # -1 means that it cannot spawn on this point

            possibleCoords = [] # these will be all the coords in which a cell could be spawn alright
            for i  in range(0, bloomHeight):
                for j in range(0, bloomWidth):
                    if allCoords[i][j] != -1:
                        possibleCoords.append((i + bloomY, j + bloomX))

            newY, newX = rand.choice(possibleCoords) # chooses a random suitable position
            alga.setPos(newX, newY)

    def __init__(self, float_1, float_2, bloom1, bloom2, parent = None):
        super().__init__(0, 0, float_1, float_2, parent)
        self.setBrush(QtGui.QBrush(QtGui.QColor("darkseagreen")))
        self._bloom = None # the bloom in which the alga takes part; if it is set to None, it means that the Alga is currently not on the map
        self._selectInitPos(bloom1, bloom2)
        self.size = np.pi * (float_1 / 2) ** 2

        Alga.population += 1

    def _selectInitPos(self, bloom1, bloom2):
        whichBloom = rand.choice([bloom1, bloom2])
        # check if the chosen bloom is too big
        if bloom1 == whichBloom and self._bloomTooBig(bloom1):
            whichBloom = bloom2
        elif bloom2 == whichBloom and self._bloomTooBig(bloom2):
            whichBloom = bloom1
        
        # select a random position inside the Bloom
        xStart = int(whichBloom.x())
        xStop = int(whichBloom.x() + whichBloom.width())
        yStart = int(whichBloom.y())
        yStop = int(whichBloom.y() + whichBloom.height())
        xPos = rand.randrange(xStart, xStop)
        yPos = rand.randrange(yStart, yStop)

        self._bloom = whichBloom
        whichBloom.addAlga() # this increments the number of algae inside the Bloom
        self.setPos(xPos, yPos)

        
    # checks if the bloom is too big to accept any more algae
    def _bloomTooBig(self, bloom):
        return bloom.algae() == int(Alga.DESIRED_POP * 3 / 4)

    def bloom(self):
        return self._bloom

    def radius(self):
        return self.rect().height() / 2
    
    def die(self):
        self.scene().removeItem(self)
        del self