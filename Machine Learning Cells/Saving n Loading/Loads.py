import re

from PySide2 import QtCore

from GenDataCls import GenData, CellData
from SimDataCls import SimData
import Sims
import Generations
from NewSimDia import ComboIndexes

# this class will handle loading data from a save file
class LoadSim():
    
    def __init__(self, simPath, scene, mlWindow):
        self._simPath = simPath
        self._scene = scene
        self._mlWindow = mlWindow

    # this will return a sim obj created from the .sim file
    def loadSim(self):
        simFile = QtCore.QFile(self._simPath)
        if not simFile.open(QtCore.QIODevice.ReadOnly):
            print("Error OOPSIE")
            errMsg = simFile.errorString();
            err = simFile.error();
            print(err, errMsg)
            return
        # the readAll returns a string
        textStream = QtCore.QTextStream(simFile)
        saveStr = textStream.readAll()
        # separate the saveString in this way in order to simplify searching for values
        saveStr = re.split(": |\n|\t|\t\t", saveStr)
        simData = self._createSimDataFromStr(saveStr)
        cellNo = int(saveStr[saveStr.index("cell nr per gen") + 1])
        algaeNo = int(saveStr[saveStr.index("algae per gen") + 1])
        secsPerGen = float(saveStr[saveStr.index("secs per gen") + 1])
        # if there is no algae spread in the save file, it means it is a save file from an older version
        # in this case, assume the regular algae spread
        algaeSpread = 0
        try:
            algaeSpread = int(saveStr[saveStr.index("algae spread in sim") + 1])
        except ValueError:
            algaeSpread = ComboIndexes.RegularSpread.value
        # a similar thing is done for the cell_eat_threshold const
        cellThreshold = 0
        try:
            cellThreshold = int(saveStr[saveStr.index("cell eat threshold const") + 1])
        except ValueError:
            cellThreshold = 130
        # finally, create the simulation object
        simulation = Sims.Sim(self._scene, cellNo, algaeNo, secsPerGen, None, self._mlWindow, algaeSpread, cellThreshold)
        simulation.setSimData(simData)
        simulation.setGraphVals(*self._createGraphLists(saveStr))
        simulation.setCrGen([0] * len(simulation.simData().gens()))
        simulation.currentGen()[len(simulation.simData().gens()) - 1] = Generations.Gen(self._scene, cellNo, algaeNo, secsPerGen, None, simulation)
        return simulation

    
    # returns the graph values from the save string(they are all a bunch of lists that are not yet contained in the SimData obj)
    def _createGraphLists(self, saveStr):
        gensNo = int(saveStr[saveStr.index("there are") + 1])
        lastGenIndex = saveStr.index("gen no") + 1
        l_avgSize = []
        l_avgCarnSize = []
        l_avgHerbSize = []
        l_avgSecs = []
        l_avgActFP = []
        l_avgInitFP = []
        l_avgSurv = []
        for i in range(gensNo):
            avgSize = float(saveStr[saveStr[lastGenIndex:].index("average sim cell size in gen") + 1 + lastGenIndex])
            l_avgSize.append(avgSize)
            avgCarnSize = float(saveStr[saveStr[lastGenIndex:].index("average sim carn cells size in gen") + 1 + lastGenIndex])
            l_avgCarnSize.append(avgCarnSize)
            avgHerbSize = float(saveStr[saveStr[lastGenIndex:].index("average sim herb cells size in gen") + 1 + lastGenIndex])
            l_avgHerbSize.append(avgHerbSize)
            avgSecs = float(saveStr[saveStr[lastGenIndex:].index("average sim secs alive in gen") + 1 + lastGenIndex])
            l_avgSecs.append(avgSecs)
            avgActFP = float(saveStr[saveStr[lastGenIndex:].index("average sim actual FP in gen") + 1 + lastGenIndex])
            l_avgActFP.append(avgActFP)
            avgInitFP = float(saveStr[saveStr[lastGenIndex:].index("average sim init FP in gen") + 1 + lastGenIndex])
            l_avgInitFP.append(avgInitFP)
            avgSurv = float(saveStr[saveStr[lastGenIndex:].index("average survivability in gen") + 1 + lastGenIndex])
            l_avgSurv.append(avgSurv)

            if i != gensNo - 2:
                lastGenIndex = saveStr[lastGenIndex:].index("gen no") + 1 + lastGenIndex

        return l_avgSize, l_avgCarnSize, l_avgHerbSize, l_avgSecs, l_avgActFP, l_avgInitFP, l_avgSurv

    # returns a SimData object created from given string
    def _createSimDataFromStr(self, saveStr):
        simData = SimData()
        # set the simulation-scope variables
        cellNo = float(saveStr[saveStr.index("cells in sim") + 1])
        simData.setCells(cellNo)
        carnCellNo = float(saveStr[saveStr.index("carn cells in sim") + 1])
        simData.setCarnCells(carnCellNo)
        herbCellNo = float(saveStr[saveStr.index("herb cells in sim") + 1])
        simData.setHerbCells(herbCellNo)
        cellsKilled = float(saveStr[saveStr.index("cells killed in sim") + 1])
        simData.setCellsKilled(cellsKilled)
        algaeEaten = float(saveStr[saveStr.index("algae eaten in sim") + 1])
        simData.setAlgaeEaten(algaeEaten)
        deadFromHunger = float(saveStr[saveStr.index("cells dead from hunger in sim") + 1])
        simData.setDeadFromHunger(deadFromHunger)
        cellsAteSomething = float(saveStr[saveStr.index("cells that ate sth in sim") + 1])
        simData.setCellsAteSomething(cellsAteSomething)
        averageSimSize = float(saveStr[saveStr.index("average sim cell size") + 1])
        simData.setAverageSimSize(averageSimSize)
        averageSimCarnSize = float(saveStr[saveStr.index("average sim carn cells size") + 1])
        simData.setAverageSimCarnSize(averageSimCarnSize)
        averageSimHerbSize = float(saveStr[saveStr.index("average sim herb cells size") + 1])
        simData.setAverageSimHerbSize(averageSimHerbSize)
        averageSimSecs = float(saveStr[saveStr.index("average sim secs alive") + 1])
        simData.setAverageSimSecondsAlive(averageSimSecs)
        averageSimActFP = float(saveStr[saveStr.index("average sim actual FP") + 1])
        simData.setAverageSimActFP(averageSimActFP)
        averageSimInitFP = float(saveStr[saveStr.index("average sim init FP") + 1])
        simData.setAverageSimInitFP(averageSimInitFP)
        averageSurv = float(saveStr[saveStr.index("average survivability") + 1])
        simData.setAverageSimSurv(averageSurv)
        genCarns = int(saveStr[saveStr.index("gens with carns") + 1])
        simData.setGensCarn(genCarns)
        genHerbs = int(saveStr[saveStr.index("gens with herbs") + 1])
        simData.setGensHerb(genHerbs)
        genActFP = int(saveStr[saveStr.index("gens with act FP") + 1])
        simData.setGensActFP(genActFP)

        oldGensData = [] # this list will contain all the gens data from the save file and will be used for setting the _gens list of the SimData obj
        gensNo = int(saveStr[saveStr.index("there are") + 1])
        lastGenIndex = saveStr.index("gen no") + 1
        while gensNo > 0:
            currGen = GenData()
            # set the generation-scope variables
            algaeEaten = float(saveStr[saveStr[lastGenIndex:].index("algae eaten in this gen") + 1 + lastGenIndex])
            currGen.setAlgaeEaten(algaeEaten)
            cellsKilled = float(saveStr[saveStr[lastGenIndex:].index("cells killed in this gen") + 1 + lastGenIndex])
            currGen.setCellsKilled(cellsKilled)
            carnCellNo = float(saveStr[saveStr[lastGenIndex:].index("carn cells in this gen") + 1 + lastGenIndex])
            currGen.setCarnCells(carnCellNo)
            herbCellNo = float(saveStr[saveStr[lastGenIndex:].index("herb cells in this gen") + 1 + lastGenIndex])
            currGen.setHerbCells(herbCellNo)
            deadFromHunger = float(saveStr[saveStr[lastGenIndex:].index("cells dead from hunger in this gen") + 1 + lastGenIndex])
            currGen.setDeadFromHunger(deadFromHunger)
            cellsAteSomething = float(saveStr[saveStr[lastGenIndex:].index("cells that ate sth in this gen") + 1 + lastGenIndex])
            currGen.setCellsAteSomething(cellsAteSomething)
            averageSurv = float(saveStr[saveStr[lastGenIndex:].index("average survivability in this gen") + 1 + lastGenIndex])
            currGen.setAverageSurvivability(averageSurv)
            averageSecs = float(saveStr[saveStr[lastGenIndex:].index("average secs alive in this gen") + 1 + lastGenIndex])
            currGen.setAverageSecondsAlive(averageSecs)
            averageActFP = float(saveStr[saveStr[lastGenIndex:].index("average actual FP in this gen") + 1 + lastGenIndex])
            currGen.setAverageActualFoodPref(averageActFP)
            averageInitFP = float(saveStr[saveStr[lastGenIndex:].index("average init FP in this gen") + 1 + lastGenIndex])
            currGen.setAverageInitFoodPref(averageInitFP)
            averageSize = float(saveStr[saveStr[lastGenIndex:].index("average cells size in this gen") + 1 + lastGenIndex])
            currGen.setAverageSize(averageSize)
            averageCarnSize = float(saveStr[saveStr[lastGenIndex:].index("average carn cells size in this gen") + 1 + lastGenIndex])
            currGen.setAverageCarnSize(averageCarnSize)
            averageHerbSize = float(saveStr[saveStr[lastGenIndex:].index("average herb cells size in this gen") + 1 + lastGenIndex])
            currGen.setAverageHerbSize(averageHerbSize)

            # find the cell no in this gen
            cellNo = float(saveStr[saveStr[lastGenIndex:].index("there are") + 1 + lastGenIndex])

            lastCellIndex = saveStr[lastGenIndex:].index("cell no") + 1 + lastGenIndex
            genCellsData = [] # the list that contains all the CellData objs of the current gen
            while cellNo > 0:
                currCell = CellData()
                # set the cell values
                cellSize = float(saveStr[saveStr[lastCellIndex:].index("cell size") + 1 + lastCellIndex])
                cellSpeedFactor = float(saveStr[saveStr[lastCellIndex:].index("cell speed factor") + 1 + lastCellIndex])
                cellSecsAlive = float(saveStr[saveStr[lastCellIndex:].index("cell seconds alive") + 1 + lastCellIndex])
                cellKills = float(saveStr[saveStr[lastCellIndex:].index("cell kills") + 1 + lastCellIndex])
                cellAlgae = float(saveStr[saveStr[lastCellIndex:].index("cell algae eaten") + 1 + lastCellIndex])
                cellSurv = float(saveStr[saveStr[lastCellIndex:].index("cell survivability") + 1 + lastCellIndex])
                cellInitFP = float(saveStr[saveStr[lastCellIndex:].index("cell init food pref") + 1 + lastCellIndex])
                cellActFP = float(saveStr[saveStr[lastCellIndex:].index("cell actual food pref") + 1 + lastCellIndex])
                currCell.setData(cellSize, cellSpeedFactor, cellSecsAlive, cellKills, cellAlgae, cellSurv, cellInitFP, cellActFP)

                # update the genCells list
                genCellsData.append(currCell)

                # update the lastCellIndex
                cellNo -= 1
                if cellNo > 0:
                    lastCellIndex = saveStr[lastCellIndex:].index("cell no") + 1 + lastCellIndex

            # update the oldGens list
            currGen.setCellsData(genCellsData)
            oldGensData.append(currGen)
            # update the gen loop
            gensNo -= 1
            if gensNo > 0:
                lastGenIndex = saveStr[lastGenIndex:].index("gen no") + 1 + lastGenIndex

        # complete the SimData obj
        simData.setGens(oldGensData)
        return simData



 