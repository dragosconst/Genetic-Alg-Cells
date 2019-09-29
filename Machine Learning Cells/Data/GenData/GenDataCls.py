


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
        ## some median values
        self._medianSurvivability = 0
        self._medianSecondsAlive = 0
        self._medianActualFoodPref = 0
        self._medianInitFoodPref = 0
        self._medianSize = 0
        self._medianCarnSize = 0
        self._medianHerbSize = 0
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
        if cellData["actualFoodPref"] != -1 and cellData["actualFoodPref"] >= 0.5:
            self._carnCells += 1
            self._updateCarnSizeMed(cellData)
        elif cellData["actualFoodPref"] != -1 and cellData["actualFoodPref"] < 0.5:
            self._herbCells += 1
            self._updateHerbSizeMed(cellData)

        # update the medians
        self._updateSurvMedian(cellData)
        self._updateSecAliveMedian(cellData)
        self._updateActFPMed(cellData)
        self._updateSizeMed(cellData)
    
    def setCellsData(self, cellsData):
        self._cellsData = cellsData

    # some methods for updating the median values
    def _updateSurvMedian(self, cellData):
        self._medianSurvivability *= (len(self._cellsData) - 1)
        self._medianSurvivability += cellData["survivability"]
        self._medianSurvivability /= len(self._cellsData)
    def _updateSecAliveMedian(self, cellData):
        self._medianSecondsAlive *= (len(self._cellsData) - 1)
        self._medianSecondsAlive += cellData["secondsAlive"]
        self._medianSecondsAlive /= len(self._cellsData)
    def _updateActFPMed(self, cellData):
        if cellData["actualFoodPref"] != -1: # if this cell ate anything at all
            self._medianActualFoodPref *= (self._cellsAteSomething - 1)
            self._medianActualFoodPref += cellData["actualFoodPref"]
            self._medianActualFoodPref /= self._cellsAteSomething
        else:
            return
    def _updateInitFPMed(self, cellData):
        self._medianInitFoodPref *= (len(self._cellsData) - 1)
        self._medianInitFoodPref += cellData["initFoodPref"]
        self._medianInitFoodPref /= len(self._cellsData)
    def _updateSizeMed(self, cellData):
        self._medianSize *= (len(self._cellsData) - 1)
        self._medianSize += cellData["size"]
        self._medianSize /= len(self._cellsData)
    def _updateCarnSizeMed(self, cellData):
        self._medianCarnSize *= (self._carnCells - 1)
        self._medianCarnSize += cellData["size"]
        self._medianCarnSize /= self._carnCells
    def _updateHerbSizeMed(self, cellData):
        self._medianHerbSize *= (self._herbCells - 1)
        self._medianHerbSize += cellData["size"]
        self._medianHerbSize /= self._herbCells

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
    def medianSurvivability(self):
        return self._medianSurvivability
    def medianSecondsAlive(self):
        return self._medianSecondsAlive
    def medianActualFoodPref(self):
        return self._medianActualFoodPref
    def medianInitFoodPref(self):
        return self._medianInitFoodPref
    def medianSize(self):
        return self._medianSize
    def medianCarnSize(self):
        return self._medianCarnSize
    def medianHerbSize(self):
        return self._medianHerbSize