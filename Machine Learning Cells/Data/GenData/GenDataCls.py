


# this dictionary-class' objects will be used to hold relevant data for every cell in a generation
class CellData():
    def __init__(self):
        self.data = {
            "size": 0,
            "speedFactor": 0,
            "secondsAlive" : 0,
            "kills": 0,
            "algae": 0,
            "survivability": 0,
            "initFoodPref": 0,
            "actualFoodPref": 0
            }

    def setData(self, size, speedFactor, secondsAlive, kills, algae, survivability, initFoodPref, actualFoodPref):
        self.data["size"] = size
        self.data["speedFactor"] = speedFactor
        self.data["secondsAlive"] = secondsAlive
        self.data["kills"] = kills
        self.data["algae"] = algae
        self.data["survivability"] = survivability
        self.data["initFoodPref"] = initFoodPref
        self.data["actualFoodPref"] = actualFoodPref
        
    def data(self):
        return data

# this class will be used for storing relevant data about a generation
class GenData():
    def __init__(self):
        self._cellsData = [] # this will be a list of CellData objects
        ## some stats about cell eating behaviour in a certain gen
        self._algaeEaten = 0
        self._cellsKilled = 0
        self._carnCells = 0 # carnivorous cells
        self._herbCells = 0 # herbivorous cells
        self._deadFromHunger = 0 # how many cells died from hunger, without eating anything at all
        self._cellsAteSomething = 0 # how many cells actually ate something before dying
        ##
        ## some average values
        self._averageSurvivability = 0
        self._averageSecondsAlive = 0
        self._averageActualFoodPref = 0
        self._averageInitFoodPref = 0
        self._averageSize = 0
        self._averageCarnSize = 0
        self._averageHerbSize = 0
        ##

    # CellData objects should be added to the _cellsData list only through this method
    def addCellData(self, cellDataObj):
        self._cellsData.append(cellDataObj)

        cellData = cellDataObj.data
        # update some vars
        self._algaeEaten += cellData["algae"]
        self._cellsKilled += cellData["kills"]
        if cellData["actualFoodPref"] == -1: # this means that this specific cell didn't eat anything
            self._deadFromHunger += 1
        else:
            self._cellsAteSomething += 1
        if cellData["actualFoodPref"] != -1 and cellData["actualFoodPref"] > 0.5:
            self._carnCells += 1
            self._updateCarnSizeAvg(cellData)
        elif cellData["actualFoodPref"] != -1 and cellData["actualFoodPref"] < 0.5:
            self._herbCells += 1
            self._updateHerbSizeAvg(cellData)

        # update the averages
        self._updateSurvAvgian(cellData)
        self._updateSecAliveAvgian(cellData)
        self._updateActFPAvg(cellData)
        self._updateInitFPAvg(cellData)
        self._updateSizeAvg(cellData)
    
    def setCellsData(self, cellsData):
        self._cellsData = cellsData

    # some methods for updating the average values
    def _updateSurvAvgian(self, cellData):
        self._averageSurvivability *= (len(self._cellsData) - 1)
        self._averageSurvivability += cellData["survivability"]
        self._averageSurvivability /= len(self._cellsData)
    def _updateSecAliveAvgian(self, cellData):
        self._averageSecondsAlive *= (len(self._cellsData) - 1)
        self._averageSecondsAlive += cellData["secondsAlive"]
        self._averageSecondsAlive /= len(self._cellsData)
    def _updateActFPAvg(self, cellData):
        if cellData["actualFoodPref"] != -1: # if this cell ate anything at all
            self._averageActualFoodPref *= (self._cellsAteSomething - 1)
            self._averageActualFoodPref += cellData["actualFoodPref"]
            self._averageActualFoodPref /= self._cellsAteSomething
        else:
            return
    def _updateInitFPAvg(self, cellData):
        self._averageInitFoodPref *= (len(self._cellsData) - 1)
        self._averageInitFoodPref += cellData["initFoodPref"]
        self._averageInitFoodPref /= len(self._cellsData)
    def _updateSizeAvg(self, cellData):
        self._averageSize *= (len(self._cellsData) - 1)
        self._averageSize += cellData["size"]
        self._averageSize /= len(self._cellsData)
    def _updateCarnSizeAvg(self, cellData):
        self._averageCarnSize *= (self._carnCells - 1)
        self._averageCarnSize += cellData["size"]
        self._averageCarnSize /= self._carnCells
    def _updateHerbSizeAvg(self, cellData):
        self._averageHerbSize *= (self._herbCells - 1)
        self._averageHerbSize += cellData["size"]
        self._averageHerbSize /= self._herbCells

    # methods for getting object vars
    def cellsData(self):
        return self._cellsData
    def cellsKilled(self):
        return self._cellsKilled
    def algaeEaten(self):
        return self._algaeEaten
    def carnCells(self):
        return self._carnCells
    def herbCells(self):
        return self._herbCells
    def deadFromHunger(self):
        return self._deadFromHunger
    def cellsAteSomething(self):
        return self._cellsAteSomething
    def averageSurvivability(self):
        return self._averageSurvivability
    def averageSecondsAlive(self):
        return self._averageSecondsAlive
    def averageActualFoodPref(self):
        return self._averageActualFoodPref
    def averageInitFoodPref(self):
        return self._averageInitFoodPref
    def averageSize(self):
        return self._averageSize
    def averageCarnSize(self):
        return self._averageCarnSize
    def averageHerbSize(self):
        return self._averageHerbSize

    # methods for directly setting gen vars
    def setCellsData(self, cellsData):
        self._cellsData = cellsData
    def setCellsKilled(self, cellsKilled):
        self._cellsKilled = cellsKilled
    def setAlgaeEaten(self, algaeEaten):
        self._algaeEaten = algaeEaten
    def setCarnCells(self, carnCells):
        self._carnCells = carnCells
    def setHerbCells(self, herbCells):
        self._herbCells = herbCells
    def setDeadFromHunger(self, deadFromHunger):
        self._deadFromHunger = deadFromHunger
    def setCellsAteSomething(self, cellsAteSomething):
        self._cellsAteSomething = cellsAteSomething
    def setAverageSurvivability(self, averageSurvivability):
        self._averageSurvivability = averageSurvivability
    def setAverageSecondsAlive(self, averageSecondsAlive):
        self._averageSecondsAlive = averageSecondsAlive
    def setAverageActualFoodPref(self, averageActualFoodPref):
        self._averageActualFoodPref = averageActualFoodPref
    def setAverageInitFoodPref(self, averageInitFoodPref):
        self._averageInitFoodPref = averageInitFoodPref
    def setAverageSize(self, averageSize):
        self._averageSize = averageSize
    def setAverageCarnSize(self, averageCarnSize):
        self._averageCarnSize = averageCarnSize
    def setAverageHerbSize(self, averageHerbSize):
        self._averageHerbSize = averageHerbSize