
from PyQt5 import QtCore
from matplotlib.figure import Figure # at this point, these are imported only for testing stuff, although they might prove to be useful later on
from matplotlib.backends.backend_qt5agg import(
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavToolbar)

from Generations import Gen
from Walls import Wall
from SimDataCls import SimData
import util
import Main

# this class will be used for containing an entire simulation
class Sim():
    def __init__(self, scene, cellsNo, algaeNo, genSec, simDia, mlWindow):
        self._scene = scene # basic simulation values
        self._cellsNo = cellsNo
        self._algaeNo = algaeNo
        self._genSec = genSec
        self._simDia = simDia
        self._simData = SimData()
        self._mlWindow = mlWindow # this is the main window object

        self._currentGen = [] # the current generation
        self._medianSimSurvOverTime = [] # for drawing the graphs, the list will contain the median sim surv over generations
        self._medianSimSizeOverTime = [] # like the previous list, but for sizes

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

    def startFirstGen(self):
        self.updateGraphs()
        self._currentGen.append(Gen(self._scene, self._cellsNo, self._algaeNo, self._genSec, self._simData, self, self._simDia))
        self._currentGen[len(self._currentGen) - 1].startGeneration()

    # for generations starting from the second
    def startAnotherGen(self):
        self._medianSimSurvOverTime.append(self._simData.medianSimSurv())
        self._medianSimSizeOverTime.append(self._simData.medianSimSize())
        self.updateGraphs()
        olderGen = self._simData.gens()[len(self._simData.gens()) - 1]
       
        genNo = len(self._simData.gens()) + 1
        self._currentGen.append(Gen(self._scene, self._cellsNo, self._algaeNo, self._genSec, self._simData, self, None, 
                                    olderGen, genNo))
        self._currentGen[len(self._currentGen) - 1].startGeneration()

    # call this to kill the current sim
    def killSim(self):
        self.killCurrGen()
        del self

    # method that handles drawing graphs in between generations
    def updateGraphs(self):
        allGens = list(range(1, len(self._currentGen) + 1))
        figSurv, axSurv = util.createGraph(allGens, self._medianSimSurvOverTime)
        self._mlWindow.updateTab(Main.Tabs.SimSurvTab.value, figSurv, axSurv, allGens, self._medianSimSurvOverTime, Main.Tabs.SimSurvTitle.value)

        figSize, axSize = util.createGraph(allGens, self._medianSimSizeOverTime)
        self._mlWindow.updateTab(Main.Tabs.SimSizeTab.value, figSize, axSize, allGens, self._medianSimSizeOverTime, Main.Tabs.SimSizeTitle.value)

    # call this to kill the ongoing generation
    def killCurrGen(self):
        self._currentGen[len(self._currentGen) - 1].killGen()
        self.startAnotherGen()

       
