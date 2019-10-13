import random as rand

from PySide2 import QtCore

from Cells import Cell
from AlgaeBloom import Bloom
from Algae import Alga
from GenDataCls import GenData
from NewSimDia import ComboIndexes
import util

class Gen():
    LIFETIME = 0 # this will be the amount of ms for which a generation lives

    def __init__(self, scene, cellsNo, algaeNo, genSec, simData, simObj, simDia = None, olderGen = None, genNumber = 1, nextGenBar = None, algaeSpread = -1, threshold = 130):
        Gen.LIFETIME = genSec * 1000

        # basic generation values
        self._scene = scene
        self._cellsNo = cellsNo
        self._algaeNo = algaeNo
        self._genSec = genSec
        self._simData = simData
        self._simDia = simDia
        if algaeSpread == -1:
            self._algaeSpread = self._simDia.algaeSpreadCombo.currentIndex() if self._simDia is not None else ComboIndexes.RegularSpread.value
        else:
            self._algaeSpread = algaeSpread
        self._threshold = threshold
        self._olderGen = olderGen
        self._genNumber = genNumber
        self._nextGenBar = nextGenBar
        self._genData = GenData()
        self.killed = False
        self._simObj = simObj
        self._paused = False
        self._pauseTimer = QtCore.QTime()
        self._pauseTimer.start()
        self._timePaused = 0 # this variable will store for how long a generation has been paused
        self._genLifeClock = QtCore.QTime()
        self._genLifeClock.start()

    # adds the specified cells number to the scene
    def _addCells(self):
        # the first generation simply makes some random cells
        if self._genNumber == 1:
            for i in range(0, self._cellsNo):
                self._scene.addItem(Cell(self._genData, None, None, self._simObj.window()))
        else:
            oneFifth = int(len(self._olderGen.cellsData()) / 5)
            parentsList = self._olderGen.cellsData()[:oneFifth]
            noParentedCells = (self._cellsNo / 2 - self._genNumber + 2) if self._cellsNo / 2 - self._genNumber + 2 >= 3 else 3 
            noParentedCells = int(noParentedCells)
            for i in range(0, self._cellsNo - noParentedCells): # + 2 because the first generation with parents is the second one
                self._scene.addItem(Cell(self._genData, self._genNumber, [rand.choice(parentsList), rand.choice(parentsList)], self._simObj.window()))
            for i in range(0, noParentedCells): # the rest are randomly generated
                self._scene.addItem(Cell(self._genData, None, None, self._simObj.window()))

    # adds the specified number of algae to the scene
    def _addAlgae(self):
        if self._algaeSpread == ComboIndexes.RegularSpread.value:
            leftBloom = Bloom(100, 200, 300, 300)
            rightBloom = Bloom(600, 600, 300, 300)
        elif self._algaeSpread == ComboIndexes.FullSpread.value:
            leftBloom = Bloom(100, 200, 750, 300)
            rightBloom = Bloom(100, 600, 750, 300)

        for i in range(0, self._algaeNo):
            self._scene.addItem(Alga(10, 10, leftBloom, rightBloom))


    # method for pausing a generation
    def pauseGen(self):
        self._paused = True
        self._pauseTimer.restart()
        for item in self._scene.items(): # pause all the cells
            if util.getClassName(item) == "Cell":
                item.pauseCell()

    # unpausing a generation
    def restartGen(self):
        self._paused = False
        self._timePaused += self._pauseTimer.elapsed()
        for item in self._scene.items(): # pause all the cells
            if util.getClassName(item) == "Cell":
                item.restartCell()

    # method for starting a generation
    def startGeneration(self):
        # set algae related values
        Alga.DESIRED_POP = self._algaeNo
        Alga.disjoint = 0
        Alga.population = 0
        self._addAlgae()
        Alga.resetAlgae(self._scene, self._simDia, self._algaeNo + self._cellsNo, 0, None if self._genNumber == 1 else self._nextGenBar)

        # set cell related values
        Cell.CELL_GEN_POP = self._cellsNo
        Cell.EAT_CELL_THRESHOLD = self._threshold
        Cell.cellDisjoint = 0
        self._addCells()
        Cell.resetCells(self._scene, self._simDia, self._algaeNo + self._cellsNo, self._algaeNo, None if self._genNumber == 1 else self._nextGenBar)
        Cell.startMoving(self._scene)
        self._checkIfAlive()
        if self._nextGenBar is not None:
            self._nextGenBar.setValue(0)

        # set the app to be pausable
        self._simObj.setPauseability(True)

    def _checkIfAlive(self):
        if self._paused == True: # if the generation is paused, there is no reason to check if the generation should be killed
            tempTimer = QtCore.QTimer()
            tempTimer.singleShot(1000, lambda: self._checkIfAlive())
            return

        dontKill = False
        totalTime = self._genLifeClock.elapsed() - self._timePaused
        for item in self._scene.items():
            if util.getClassName(item) == "Cell":
                dontKill = True
                break
        if totalTime >= Gen.LIFETIME:
            self.killGen()
            return
        if not dontKill:
            self.killGen()
            return
        tempTimer = QtCore.QTimer()
        tempTimer.singleShot(1000, lambda: self._checkIfAlive())

    def killGen(self, simDead = False):
        if self.killed == True:
            return
        self.killed = True
        for item in self._scene.items():
            if util.getClassName(item) != "Wall": # dont delete the walls
                item.die() # the die method removes cells\algae from the scene and deletes their instances
        self._genData.setCellsData(sorted(self._genData.cellsData(), key=lambda cellData: cellData.data["survivability"], reverse=True))
        self._simData.addGen(self._genData)
        # this checks if this gen should spawn another gen after its death
        # for instance, if a new sim is created on top of this one, this gen should not trigger the birth of another gen
        if not simDead:
            self._simObj.startAnotherGen()

        # set the app to not be pausable
        self._simObj.setPauseability(True)

    # methods for directly setting gen vals
    def setThreshold(self, thresh):
        self._threshold = thresh
