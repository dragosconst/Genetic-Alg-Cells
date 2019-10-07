
from PyQt5 import QtCore

# this class will handle saving generations
class SaveSim():
    def __init__(self, simObj, savePath):
        self._simObj = simObj
        self._simData = simObj.simData()
        self._savePath = savePath

    # creates a string that contains all the relevant data of a simulation
    def createSaveString(self):
        saveStr = "Simulation CRAFS"
        # add the sim stats
        saveStr += "\ncells in sim: " + str(self._simData.cells())
        saveStr += "\ncarn cells in sim: " + str(self._simData.carnCells())
        saveStr += "\nherb cells in sim: " + str(self._simData.herbCells())
        saveStr += "\ncells killed in sim: " + str(self._simData.cellsKilled())
        saveStr += "\nalgae eaten in sim: " + str(self._simData.algaeEaten())
        saveStr += "\ncells dead from hunger in sim: " + str(self._simData.deadFromHunger())
        saveStr += "\ncells that ate sth in sim: " + str(self._simData.cellsAteSomething())
        saveStr += "\naverage sim cell size: " + str(self._simData.averageSimSize())
        saveStr += "\naverage sim carn cell size: " + str(self._simData.averageSimCarnSize())
        saveStr += "\naverage sim herb cell size: " + str(self._simData.averageSimHerbSize())
        saveStr += "\naverage sim secs alive: " + str(self._simData.averageSimSecondsAlive())
        saveStr += "\naverage sim actual FP: " + str(self._simData.averageSimActFP())
        saveStr += "\naverage sim init FP: " + str(self._simData.averageSimInitFP())
        saveStr += "\naverage survivability: " + str(self._simData.averageSimInitFP())

        # add generations
        saveStr += "\nthere are " + str(len(self._simData.gens())) + "generations: "
        allGens = len(self._simData.gens())
        # add every generation
        for i in range(allGens):
            thisGen = self._simData.gens()[i]
            # general data about the generation
            saveStr += "\n\tgen no " + str(i)
            saveStr += "\n\talgae eaten in this gen: " + str(thisGen.algaeEaten())  
            saveStr += "\n\tcells killed in this gen: " + str(thisGen.cellsKilled())  
            saveStr += "\n\tcarn cells in this gen: " + str(thisGen.carnCells())  
            saveStr += "\n\therb cells in this gen: " + str(thisGen.herbCells())  
            saveStr += "\n\tcells dead from hunger in this gen: " + str(thisGen.deadFromHunger())  
            saveStr += "\n\tcells that ate sth in this gen: " + str(thisGen.cellsAteSomething())  
            saveStr += "\n\taverage survivability in this gen: " + str(thisGen.averageSurvivability())  
            saveStr += "\n\taverage secs alive in this gen: " + str(thisGen.averageSecondsAlive())  
            saveStr += "\n\taverage actual FP in this gen: " + str(thisGen.averageActualFoodPref())  
            saveStr += "\n\taverage init FP in this gen: " + str(thisGen.averageInitFoodPref())  
            saveStr += "\n\taverage cell size in this gen: " + str(thisGen.averageSize())  
            saveStr += "\n\taverage carn cell size in this gen: " + str(thisGen.averageCarnSize())  
            saveStr += "\n\taverage herb cell size in this gen: " + str(thisGen.averageHerbSize())

            allCells = len(thisGen.cellsData())
            saveStr += "\n\tthere are " + str(allCells) + " cells in this gen: "
            for j in range(allCells):
                thisCell = thisGen.cellsData()[j]
                # general data about the cell
                saveStr += "\n\t\tcell no " + str(j) + " from gen no " + str(i)
                saveStr += "\n\t\tcell size: " + str(thisCell.data["size"])
                saveStr += "\n\t\tcell speed factor: " + str(thisCell.data["speedFactor"])
                saveStr += "\n\t\tcell seconds alive: " + str(thisCell.data["secondsAlive"])
                saveStr += "\n\t\tcell kills: " + str(thisCell.data["kills"])
                saveStr += "\n\t\tcell algae eaten: " + str(thisCell.data["algae"])
                saveStr += "\n\t\tcell survivanility: " + str(thisCell.data["survivability"])
                saveStr += "\n\t\tcell init food pref: " + str(thisCell.data["initFoodPref"])
                saveStr += "\n\t\tcell actual food pref: " + str(thisCell.data["actualFoodPref"])
            
                
        return saveStr

    # create the save file
    # this will create a file that contains a string with the sim data
    def saveSim(self):
        saveStr = self.createSaveString()
        saveFile = QtCore.QFile(self._savePath)
        if not saveFile.open(QtCore.QIODevice.ReadWrite):
            print("Error OOPSIE")
            return
        saveFile.write(QtCore.QByteArray().append(saveStr))