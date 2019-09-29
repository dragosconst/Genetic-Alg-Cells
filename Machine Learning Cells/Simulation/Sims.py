
from PyQt5 import QtCore

from Generations import Gen
from Walls import Wall

# this class will be used for containing an entire simulation
class Sim():
    def __init__(self, scene, cellsNo, algaeNo, genSec, simDia):
        self._scene = scene # basic simulation values
        self._cellsNo = cellsNo
        self._algaeNo = algaeNo
        self._genSec = genSec
        self._simDia = simDia

        self._currentGen = [] # the current generation

        self._genClock = QtCore.QTimer() # this will time each generation


    # add walls to the scene
    # this method is handled by this class, because the walls remain the same throughout all the generations
    # they are only barely tied to the current simulation
    def _addWalls(self):
        # add a wall for each side
        self._scene.addItem(Wall(1))
        self._scene.addItem(Wall(2))
        self._scene.addItem(Wall(3))
        self._scene.addItem(Wall(4))

    # call this to start the simulation
    def startSim(self):
        self._addWalls()
        self.startFirstGen()
        self._genClock.singleShot(self._genSec * 1000, lambda: self.killCurrGen())

    def startFirstGen(self):
        self._currentGen.append(Gen(self._scene, self._cellsNo, self._algaeNo, self._genSec, self._simDia))
        self._currentGen[len(self._currentGen) - 1].startGeneration()

    # call this to kill the current sim
    def killSim(self):
        self.killCurrGen()
        del self

    # call this to kill the ongoing generation
    def killCurrGen(self):
        self._currentGen[len(self._currentGen) - 1].killGen()

       
