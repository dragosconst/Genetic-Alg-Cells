
from Generations import Gen
from Walls import Wall
from SimDataCls import SimData
from NewSimDia import ComboIndexes
import util
import Main

# this class will be used for containing an entire simulation
class Sim():
    def __init__(self, scene, cellsNo, algaeNo, genSec, simDia, mlWindow, algaeSpread = -1, threshold = 130):
        self._scene = scene # basic simulation values
        self._cellsNo = cellsNo
        self._algaeNo = algaeNo
        self._genSec = genSec
        self._simDia = simDia
        self._simData = SimData()
        self._mlWindow = mlWindow # this is the main window object
        self._algaeSpread = 0
        if algaeSpread == -1:
            self._algaeSpread = self._simDia.algaeSpreadCombo.currentIndex() if self._simDia is not None else ComboIndexes.RegularSpread.value
        else:
            self._algaeSpread = algaeSpread
        self._threshold = threshold
        self._pausable = False

        self._allGens = [] # a list containing all the generation objects of the simulation
        self._currentGen = None # this will be the on-going generation
        self._averageSimSurvOverTime = [] # for drawing the graphs, the list will contain the average sim surv over generations
        self._averageSimSizeOverTime = [] # like the previous list, but for sizes
        self._averageSimCarnSizeOverTime = []
        self._averageSimSpeedFactOverTime = []
        self._averageSimHerbSizeOverTime = []
        self._averageSimSecAliveOverTime = []
        self._averageSimActFPOverTime = []
        self._averageInitFPOverTime = []

        self._averageGenSurvOverTime = [] # for drawing the graphs, the list will contain the average Gen surv for every gen
        self._averageGenSizeOverTime = [] # like the previous list, but for sizes
        self._averageGenCarnSizeOverTime = []
        self._averageGenSpeedFactOverTime = []
        self._averageGenHerbSizeOverTime = []
        self._averageGenSecAliveOverTime = []
        self._averageGenActFPOverTime = []
        self._averageGenInitFPOverTime = []

    # change pauseability value
    def setPauseability(self, val):
        self._pausable = val

    def pauseability(self):
        return self._pausable

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
        self._currentGen = Gen(self._scene, self._cellsNo, self._algaeNo, self._genSec, self._simData, self, self._simDia)
        # manually set the threshold
        self._currentGen.setThreshold(self._threshold)
        self._allGens.append(self._currentGen)
        self._allGens[len(self._allGens) - 1].startGeneration()

    # for generations starting from the second
    def startAnotherGen(self):
        # these lists are all related to graph drawing
        self._averageSimSurvOverTime.append(self._simData.averageSimSurv())
        self._averageSimSizeOverTime.append(self._simData.averageSimSize())
        self._averageSimSpeedFactOverTime.append(self._simData.averageSimSpeedFactor())
        self._averageSimCarnSizeOverTime.append(self._simData.averageSimCarnSize())
        self._averageSimHerbSizeOverTime.append(self._simData.averageSimHerbSize())
        self._averageSimSecAliveOverTime.append(self._simData.averageSimSecondsAlive())
        self._averageSimActFPOverTime.append(self._simData.averageSimActFP())
        self._averageInitFPOverTime.append(self._simData.averageSimInitFP())
        currGen = self._simData.currentGen()
        self._averageGenSurvOverTime.append(currGen.averageSurvivability())
        self._averageGenSizeOverTime.append(currGen.averageSize())
        self._averageGenSpeedFactOverTime.append(currGen.averageSpeedFactor())
        self._averageGenCarnSizeOverTime.append(currGen.averageCarnSize())
        self._averageGenHerbSizeOverTime.append(currGen.averageHerbSize())
        self._averageGenSecAliveOverTime.append(currGen.averageSecondsAlive())
        self._averageGenActFPOverTime.append(currGen.averageActualFoodPref())
        self._averageGenInitFPOverTime.append(currGen.averageInitFoodPref())
        # here end the graph-related lists
        # update the graph drawings
        self.updateGraphs()

        # this is needed for creating a new generation(it must have data from the old generation)
        olderGen = self._simData.gens()[len(self._simData.gens()) - 1]
       
        genNo = len(self._simData.gens()) + 1
        self._currentGen = Gen(self._scene, self._cellsNo, self._algaeNo, self._genSec, self._simData, self, None,
                                    olderGen, genNo, self._mlWindow.nextGenBar, self._algaeSpread, self._threshold)
        self._allGens.append(self._currentGen)
        # finally, start the generation
        self._allGens[len(self._allGens) - 1].startGeneration()


    # for loading a simulation
    def startLoadSim(self):
        self._addWalls()

        # update the graph drawings
        self.updateGraphs()

        # this is needed for creating a new generation(it must have data from the old generation)
        olderGen = self._simData.gens()[len(self._simData.gens()) - 1]

        genNo = len(self._simData.gens()) + 1
        self._currentGen = Gen(self._scene, self._cellsNo, self._algaeNo, self._genSec, self._simData, self, None,
                                    olderGen, genNo, self._mlWindow.nextGenBar, self._algaeSpread, self._threshold)
        self._allGens.append(self._currentGen)
        # finally, start the generation
        self._allGens[len(self._allGens) - 1].startGeneration()



    # call this to kill the current sim
    def killSim(self):
        self._currentGen.killGen(True)
        del self

    # method that handles drawing graphs in between generations
    def updateGraphs(self):
        allGens = list(range(1, len(self._allGens) + 1))
        figSurv, axSurv = util.createGraph(allGens, self._averageSimSurvOverTime, "blue")
        self._mlWindow.updateTab(Main.Tabs.SimSurvTab.value, figSurv, axSurv, allGens, self._averageSimSurvOverTime, Main.Tabs.SimSurvTitle.value, "blue")

        figSize, axSize = util.createGraph(allGens, self._averageSimSizeOverTime, "olive")
        self._mlWindow.updateTab(Main.Tabs.SimSizeTab.value, figSize, axSize, allGens, self._averageSimSizeOverTime, Main.Tabs.SimSizeTitle.value, "olive")
        
        figCarnSize, axCarnSize = util.createGraph(allGens, self._averageSimCarnSizeOverTime, "darkred")
        self._mlWindow.updateTab(Main.Tabs.SimCarnSizeTab.value, figCarnSize, axCarnSize, allGens, self._averageSimCarnSizeOverTime, Main.Tabs.SimCarnSizeTitle.value, "darkred")

        figHerbSize, axHerbSize = util.createGraph(allGens, self._averageSimHerbSizeOverTime, "greenyellow")
        self._mlWindow.updateTab(Main.Tabs.SimHerbSizeTab.value, figHerbSize, axHerbSize, allGens, self._averageSimHerbSizeOverTime, Main.Tabs.SimHerbSizeTitle.value, "greenyellow")

        figSP, axSP = util.createGraph(allGens, self._averageSimSpeedFactOverTime, "darkorchid")
        self._mlWindow.updateTab(Main.Tabs.SimSFTab.value, figSP, axSP, allGens, self._averageSimSpeedFactOverTime, Main.Tabs.SimSFTitle.value, "darkorchid")

        figSecs, axSecs = util.createGraph(allGens, self._averageSimSecAliveOverTime, "steelblue")
        self._mlWindow.updateTab(Main.Tabs.SimSecAliveTab.value, figSecs, axSecs, allGens, self._averageSimSecAliveOverTime, Main.Tabs.SimSecAliveTitle.value, "steelblue")

        figActFP, axActFP = util.createGraph(allGens, self._averageSimActFPOverTime, "crimson")
        self._mlWindow.updateTab(Main.Tabs.SimActFPTab.value, figActFP, axActFP, allGens, self._averageSimActFPOverTime, Main.Tabs.SimActFPTitle.value, "crimson")

        figInitFP, axInitFP = util.createGraph(allGens, self._averageInitFPOverTime, "darkmagenta")
        self._mlWindow.updateTab(Main.Tabs.SimInitFPTab.value, figInitFP, axInitFP, allGens, self._averageInitFPOverTime, Main.Tabs.SimInitFPTitle.value, "darkmagenta")

        figSurv, axSurv = util.createGraph(allGens, self._averageGenSurvOverTime, "cornflowerblue")
        self._mlWindow.updateTab(Main.Tabs.GenSurvTab.value, figSurv, axSurv, allGens, self._averageGenSurvOverTime, Main.Tabs.GenSurvTitle.value, "cornflowerblue")

        figSize, axSize = util.createGraph(allGens, self._averageGenSizeOverTime, "olivedrab")
        self._mlWindow.updateTab(Main.Tabs.GenSizeTab.value, figSize, axSize, allGens, self._averageGenSizeOverTime, Main.Tabs.GenSizeTitle.value, "olivedrab")

        figCarnSize, axCarnSize = util.createGraph(allGens, self._averageGenCarnSizeOverTime, "firebrick")
        self._mlWindow.updateTab(Main.Tabs.GenCarnSizeTab.value, figCarnSize, axCarnSize, allGens, self._averageGenCarnSizeOverTime, Main.Tabs.GenCarnSizeTitle.value, "firebrick")

        figHerbSize, axHerbSize = util.createGraph(allGens, self._averageGenHerbSizeOverTime, "limegreen")
        self._mlWindow.updateTab(Main.Tabs.GenHerbSizeTab.value, figHerbSize, axHerbSize, allGens, self._averageGenHerbSizeOverTime, Main.Tabs.GenHerbSizeTitle.value, "limegreen")

        figSP, axSP = util.createGraph(allGens, self._averageGenSpeedFactOverTime, "darkviolet")
        self._mlWindow.updateTab(Main.Tabs.GenSFTab.value, figSP, axSP, allGens, self._averageGenSpeedFactOverTime, Main.Tabs.GenSFTitle.value, "darkviolet")

        figSecs, axSecs = util.createGraph(allGens, self._averageGenSecAliveOverTime, "slategray")
        self._mlWindow.updateTab(Main.Tabs.GenSecAliveTab.value, figSecs, axSecs, allGens, self._averageGenSecAliveOverTime, Main.Tabs.GenSecAliveTitle.value, "slategray")

        figActFP, axActFP = util.createGraph(allGens, self._averageGenActFPOverTime, "brown")
        self._mlWindow.updateTab(Main.Tabs.GenActFPTab.value, figActFP, axActFP, allGens, self._averageGenActFPOverTime, Main.Tabs.GenActFPTitle.value, "brown")

        figInitFP, axInitFP = util.createGraph(allGens, self._averageGenInitFPOverTime, "purple")
        self._mlWindow.updateTab(Main.Tabs.GenInitFPTab.value, figInitFP, axInitFP, allGens, self._averageGenInitFPOverTime, Main.Tabs.GenInitFPTitle.value, "purple")

    # pause a simulation
    def pauseSim(self):
        self._currentGen.pauseGen()
    # restart a simulation after a pause
    def restartSim(self):
        self._currentGen.restartGen()

    # call this to kill the ongoing generation
    def killCurrGen(self):
        self._currentGen.killGen()
        self.startAnotherGen()

    # methods that return stuff
    def scene(self):
        return self._scene
    def window(self):
        return self._mlWindow
    def threshold(self):
        return self._threshold
    def simData(self):
        return self._simData
    def cellsNo(self):
        return self._cellsNo
    def algaeNo(self):
        return self._algaeNo
    def genSec(self):
        return self._genSec
    def averageSimSurvOverTime(self):
        return self._averageSimSurvOverTime
    def averageSimSizeOverTime(self):
        return self._averageSimSizeOverTime
    def averageSimCarnSizeOverTime(self):
        return self._averageSimCarnSizeOverTime
    def averageSimHerbSizeOverTime(self):
        return self._averageSimHerbSizeOverTime
    def averageSimSpeedFactor(self):
        return self._averageSimSpeedFactOverTime
    def averageSimSecAliveOverTime(self):
        return self._averageSimSecAliveOverTime
    def averageSimActFPOverTime(self):
        return self._averageSimActFPOverTime
    def averageInitFPOverTime(self):
        return self._averageInitFPOverTime
    def averageGenSurvOverTime(self):
        return self._averageGenSurvOverTime
    def averageGenSizeOverTime(self):
        return self._averageGenSizeOverTime
    def averageGenCarnSizeOverTime(self):
        return self._averageGenCarnSizeOverTime
    def averageGenHerbSizeOverTime(self):
        return self._averageGenHerbSizeOverTim
    def averageGenSpeedFactOverTime(self):
        return self._averageGenSpeedFactOverTime
    def averageGenSecAliveOverTime(self):
        return self._averageGenSecAliveOverTime
    def averageGenActFPOverTime(self):
        return self._averageGenActFPOverTime
    def averageGenInitFPOverTime(self):
        return self._averageGenInitFPOverTime
    def currentGen(self):
        return self._allGens

    # for setting the values directly
    def setGraphVals(self, size, csize, hsize, secs, actfp, inifp, surv, sf, GENsize, GENcsize, GENhsize, GENsecs, GENactfp, GENinifp, GENsurv, GENsf):
        self._averageSimSizeOverTime = size
        self._averageSimCarnSizeOverTime = csize
        self._averageSimHerbSizeOverTime = hsize
        self._averageSimSecAliveOverTime = secs
        self._averageSimActFPOverTime = actfp
        self._averageInitFPOverTime = inifp
        self._averageSimSurvOverTime = surv
        self._averageSimSpeedFactOverTime = sf
        self._averageGenSizeOverTime = GENsize
        self._averageGenCarnSizeOverTime = GENcsize
        self._averageGenHerbSizeOverTime = GENhsize
        self._averageGenSecAliveOverTime = GENsecs
        self._averageGenActFPOverTime = GENactfp
        self._averageGenInitFPOverTime = GENinifp
        self._averageGenSurvOverTime = GENsurv
        self._averageGenSpeedFactOverTime = GENsf
    def setCrGen(self, currGen):
        self._allGens = currGen
    def setSimData(self, simData):
        self._simData = simData
       
