# the objects of this class will be used to store relevant data for an entire simulation
class SimData():
    def __init__(self):
        self._gens = [] # a list of all GenData objects from this simulation

        ## some simple values that describe certain aspects of the simulation
        self._cells = 0 # how many cells lived through this simulation
        self._carnCells = 0 # how many cells were carnivorous
        self._herbCells = 0 # how many cells were herbivorous
        self._cellsKilled = 0 # how many cells were killed in the sim
        self._algaeEaten = 0 # how many algae were eaten in this sim
        self._deadFromHunger = 0 # how many cells died from hunger, without eating anything at all
        self._cellsAteSomething = 0 # how many cells actually ate something before dying
        self._totalTime = 0 # this is for how long the simulation has been going
        ##

        ## values that help with calculating the average values
        self._gensWithActualFP = 0
        self._gensWithCarn = 0
        self._gensWithHerb = 0
        ##

        ## a bunch of average values of the whole simulation
        self._averageSimSize = 0 # the average size of cells throughout the simulation
        self._averageSimCarnSize = 0 # the average size of the carnivorous cells throughout the sim
        self._averageSimHerbSize = 0 # the average size of the herbivorous cells throughout the sim
        self._averageSimSpeedFactor = 0
        self._averageSimSecondsAlive = 0 # the average seconds alive of cells throughout the sim
        self._averageSimActFP = 0 # the average actual food preference of the cells in the sim
        self._averageSimInitFP = 0 # same as before but for initial fp
        self._averageSimSurv = 0 # the average survivability of the cells in the sim
        ##

    # this is the method that has to be used for adding a new GenData object to the SimData, never directly append
    # elements to the _gens list !!!!!!!!
    def addGen(self, genData):
        self._gens.append(genData)

        # update the simple values
        self._cells += len(genData.cellsData())
        self._carnCells += genData.carnCells()
        self._herbCells += genData.herbCells()
        self._cellsKilled += genData.cellsKilled()
        self._algaeEaten += genData.algaeEaten()
        self._deadFromHunger += genData.deadFromHunger()
        self._cellsAteSomething += genData.cellsAteSomething()

        # update the average values
        self._updateSimSizeAvg(genData)
        if genData.averageCarnSize() > 0: # if there were any carnivorous cells at all
            self._gensWithCarn += 1
            self._updateSimCarnSizeAvg(genData)
        if genData.averageHerbSize() > 0: # if there were any herb cells at all
            self._gensWithHerb += 1
            self._updateSimHerbSizeAvg(genData)
        self._updateSimSecAliveAvg(genData)
        self._updateSimActFPAvg(genData)
        self._updateSimInitFPAvg(genData)
        self._updateSimSpeedFactor(genData)
        self._updateSimSurvAvg(genData)

    # some update methods
    def _updateSimSurvAvg(self, genData):
        self._averageSimSurv *= (len(self._gens) - 1)
        self._averageSimSurv += genData.averageSurvivability()
        self._averageSimSurv /= len(self._gens)
    def _updateSimSpeedFactor(self, genData):
        self._averageSimSpeedFactor *= (len(self._gens) - 1)
        self._averageSimSpeedFactor += genData.averageSpeedFactor()
        self._averageSimSpeedFactor /= len(self._gens)
    def _updateSimSecAliveAvg(self, genData):
        self._averageSimSecondsAlive *= (len(self._gens) - 1)
        self._averageSimSecondsAlive += genData.averageSecondsAlive()
        self._averageSimSecondsAlive /= len(self._gens)
    def _updateSimActFPAvg(self, genData):
        if genData.averageActualFoodPref() > 0: # if this gen's cells ate anything at all
            self._gensWithActualFP += 1
            self._averageSimActFP *= (self._gensWithActualFP - 1)
            self._averageSimActFP += genData.averageActualFoodPref()
            self._averageSimActFP /= self._gensWithActualFP
        else:
            return
    def _updateSimInitFPAvg(self, genData):
        self._averageSimInitFP *= (len(self._gens) - 1)
        self._averageSimInitFP += genData.averageInitFoodPref()
        self._averageSimInitFP /= len(self._gens)
    def _updateSimSizeAvg(self, genData):
        self._averageSimSize *= (len(self._gens) - 1)
        self._averageSimSize += genData.averageSize()
        self._averageSimSize /= len(self._gens)
    def _updateSimCarnSizeAvg(self, genData):
        self._averageSimCarnSize *= (self._gensWithCarn - 1)
        self._averageSimCarnSize += genData.averageCarnSize()
        self._averageSimCarnSize /= self._gensWithCarn
    def _updateSimHerbSizeAvg(self, genData):
        self._averageSimHerbSize *= (self._gensWithHerb - 1)
        self._averageSimHerbSize += genData.averageHerbSize()
        self._averageSimHerbSize /= self._gensWithHerb

    # some methods that return various instance objects
    def gens(self):
        return self._gens
    def currentGen(self):
        return self._gens[len(self._gens) - 1]
    def cells(self):
        return self._cells
    def carnCells(self):
        return self._carnCells
    def herbCells(self):
        return self._herbCells
    def cellsKilled(self):
        return self._cellsKilled
    def algaeEaten(self):
        return self._algaeEaten
    def deadFromHunger(self):
        return self._deadFromHunger
    def cellsAteSomething(self):
        return self._cellsAteSomething
    def totalTime(self):
        return self._totalTime
    def averageSimSize(self):
        return self._averageSimSize
    def averageSimCarnSize(self):
        return self._averageSimCarnSize
    def averageSimHerbSize(self):
        return self._averageSimHerbSize
    def averageSimSecondsAlive(self):
        return self._averageSimSecondsAlive
    def averageSimActFP(self):
        return self._averageSimActFP
    def averageSimInitFP(self):
        return self._averageSimInitFP
    def averageSimSpeedFactor(self):
        return self._averageSimSpeedFactor
    def averageSimSurv(self):
        return self._averageSimSurv
    def gensWithCarn(self):
        return self._gensWithCarn
    def gensWithHerb(self):
        return self._gensWithHerb
    def gensActFP(self):
        return self._gensWithActualFP
    
    # methods for directly setting these vars, needed for loading old sims
    def setGens(self, gens):
        self._gens = gens
    def setCells(self, cells):
        self._cells = cells
    def setCarnCells(self, carnCells):
        self._carnCells = carnCells
    def setHerbCells(self, herbCells):
        self._herbCells = herbCells
    def setCellsKilled(self, cellsKilled):
        self._cellsKilled = cellsKilled
    def setAlgaeEaten(self, algae):
        self._algaeEaten = algae
    def setDeadFromHunger(self, deadFromHunger):
        self._deadFromHunger = deadFromHunger
    def setCellsAteSomething(self, cellsAteSomething):
        self._cellsAteSomething = cellsAteSomething
    def setTotalTime(self, totalTime):
        self._totalTime = totalTime
    def setAverageSimSize(self, averageSimSize):
        self._averageSimSize = averageSimSize
    def setAverageSimCarnSize(self, averageSimCarnSize):
        self._averageSimCarnSize = averageSimCarnSize
    def setAverageSimHerbSize(self, averageSimHerbSize):
        self._averageSimHerbSize = averageSimHerbSize
    def setAverageSimSpeedFactor(self, averageSpeedFactor):
        self._averageSimSpeedFactor = averageSpeedFactor
    def setAverageSimSecondsAlive(self, averageSimSecondsAlive):
        self._averageSimSecondsAlive = averageSimSecondsAlive
    def setAverageSimActFP(self, averageSimActFP):
        self._averageSimActFP = averageSimActFP
    def setAverageSimInitFP(self, averageSimInitFP):
        self._averageSimInitFP = averageSimInitFP
    def setAverageSimSurv(self, averageSimSurv):
        self._averageSimSurv = averageSimSurv
    def setGensCarn(self, gensCarn):
        self._gensWithCarn = gensCarn
    def setGensHerb(self, gensHerb):
        self._gensWithHerb = gensHerb
    def setGensActFP(self, gensActFP):
        self._gensWithActualFP = gensActFP