
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
        self._averageSimSurvOverTime = [] # for drawing the graphs, the list will contain the average sim surv over generations
        self._averageSimSizeOverTime = [] # like the previous list, but for sizes
        self._averageSimCarnSizeOverTime = []
        self._averageSimHerbSizeOverTime = []
        self._averageSimSecAliveOverTime = []
        self._averageSimActFPOverTime = []
        self._averageInitFPOverTime = []

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

    # because this method starts the first generation, it does not need any data from previous generations(because they don't
    # exist)
    def startFirstGen(self):
        # this updateGraphs call will just draw some empty graphs on their reserved area of the screen
        # if the method is not called here, the window would look weird with a big empty white square on the bottom right corner
        self.updateGraphs()
        self._currentGen.append(Gen(self._scene, self._cellsNo, self._algaeNo, self._genSec, self._simData, self, self._mlWindow, self._simDia))
        self._currentGen[len(self._currentGen) - 1].startGeneration()

    # for generations starting from the second
    def startAnotherGen(self):
        # these lists are all related to graph drawing
        self._averageSimSurvOverTime.append(self._simData.averageSimSurv())
        self._averageSimSizeOverTime.append(self._simData.averageSimSize())
        self._averageSimCarnSizeOverTime.append(self._simData.averageSimCarnSize())
        self._averageSimHerbSizeOverTime.append(self._simData.averageSimHerbSize())
        self._averageSimSecAliveOverTime.append(self._simData.averageSimSecondsAlive())
        self._averageSimActFPOverTime.append(self._simData.averageSimActFP())
        self._averageInitFPOverTime.append(self._simData.averageSimInitFP())
        # here end the graph-related lists

        # update the graph drawings
        self.updateGraphs()

        # this is needed for creating a new generation(it must have data from the old generation)
        olderGen = self._simData.gens()[len(self._simData.gens()) - 1]
       
        genNo = len(self._simData.gens()) + 1
        self._currentGen.append(Gen(self._scene, self._cellsNo, self._algaeNo, self._genSec, self._simData, self, self._mlWindow, None, 
                                    olderGen, genNo))
        # finally, start the generation
        self._currentGen[len(self._currentGen) - 1].startGeneration()

    # call this to kill the current sim
    def killSim(self):
        self.killCurrGen()
        del self

    # method that handles drawing graphs in between generations
    def updateGraphs(self):
        allGens = list(range(1, len(self._currentGen) + 1))
        figSurv, axSurv = util.createGraph(allGens, self._averageSimSurvOverTime, "blue")
        self._mlWindow.updateTab(Main.Tabs.SimSurvTab.value, figSurv, axSurv, allGens, self._averageSimSurvOverTime, Main.Tabs.SimSurvTitle.value, "blue")

        figSize, axSize = util.createGraph(allGens, self._averageSimSizeOverTime, "olive")
        self._mlWindow.updateTab(Main.Tabs.SimSizeTab.value, figSize, axSize, allGens, self._averageSimSizeOverTime, Main.Tabs.SimSizeTitle.value, "olive")
        
        figCarnSize, axCarnSize = util.createGraph(allGens, self._averageSimCarnSizeOverTime, "darkred")
        self._mlWindow.updateTab(Main.Tabs.SimCarnSizeTab.value, figCarnSize, axCarnSize, allGens, self._averageSimCarnSizeOverTime, Main.Tabs.SimCarnSizeTitle.value, "darkred")

        figHerbSize, axHerbSize = util.createGraph(allGens, self._averageSimHerbSizeOverTime, "greenyellow")
        self._mlWindow.updateTab(Main.Tabs.SimHerbSizeTab.value, figHerbSize, axHerbSize, allGens, self._averageSimHerbSizeOverTime, Main.Tabs.SimHerbSizeTitle.value, "greenyellow")

        figSecs, axSecs = util.createGraph(allGens, self._averageSimSecAliveOverTime, "steelblue")
        self._mlWindow.updateTab(Main.Tabs.SimSecAliveTab.value, figSecs, axSecs, allGens, self._averageSimSecAliveOverTime, Main.Tabs.SimSecAliveTitle.value, "steelblue")

        figActFP, axActFP = util.createGraph(allGens, self._averageSimActFPOverTime, "crimson")
        self._mlWindow.updateTab(Main.Tabs.SimActFPTab.value, figActFP, axActFP, allGens, self._averageSimActFPOverTime, Main.Tabs.SimActFPTitle.value, "crimson")

        figInitFP, axInitFP = util.createGraph(allGens, self._averageInitFPOverTime, "darkmagenta")
        self._mlWindow.updateTab(Main.Tabs.SimInitFPTab.value, figInitFP, axInitFP, allGens, self._averageInitFPOverTime, Main.Tabs.SimInitFPTitle.value, "darkmagenta")

    # pause a simulation
    def pauseSim(self):
        self._currentGen[len(self._currentGen) - 1].pauseGen()
    # restart a simulation after a pause
    def restartSim(self):
        self._currentGen[len(self._currentGen) - 1].restartGen()

    # call this to kill the ongoing generation
    def killCurrGen(self):
        self._currentGen[len(self._currentGen) - 1].killGen()
        self.startAnotherGen()

    # methods that return stuff
    def simData(self):
        return self._simData

       
