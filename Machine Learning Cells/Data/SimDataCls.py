

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

        ## a bunch of median values of the whole simulation
        self._medianSimSize = 0 # the median size of cells throughout the simulation
        self._medianSimCarnSize = 0 # the median size of the carnivorous cells throughout the sim
        self._medianSimHerbSize = 0 # the median size of the herbivorous cells throughout the sim
        self._medianSimSecondsAlive = 0 # the median seconds alive of cells throughout the sim
        self._medianSimActFP = 0 # the median actual food preference of the cells in the sim
        self._medianSimInitFP = 0 # same as before but for initial fp
        self._medianSimSurv = 0 # the median survivability of the cells in the sim
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

        # update the median values
        self._updateSimSizeMed(genData)
        if genData.medianCarnSize() > 0: # if there were any carnivorous cells at all
            self._updateSimCarnSizeMed(genData)
        if genData.medianHerbSize() > 0: # if there were any herb cells at all
            self._updateSimHerbSizeMed(genData)
        self._updateSimSecAliveMedian(genData)
        self._updateSimActFPMed(genData)
        self._updateSimInitFPMed(genData)
        self._updateSimSurvMedian(genData)

    # some update methods
    def _updateSimSurvMedian(self, genData):
        self._medianSimSurv *= (len(self._gens) - 1)
        self._medianSimSurv += genData.medianSurvivability()
        self._medianSimSurv /= len(self._gens)
    def _updateSimSecAliveMedian(self, genData):
        self._medianSimSecondsAlive *= (len(self._gens) - 1)
        self._medianSimSecondsAlive += genData.medianSecondsAlive()
        self._medianSimSecondsAlive /= len(self._gens)
    def _updateSimActFPMed(self, genData):
        if genData.medianActualFoodPref() != -0: # if this gen's cells ate anything at all
            self._medianSimActFP *= (self._cellsAteSomething - 1)
            self._medianSimActFP += genData.medianActualFoodPref()
            self._medianSimActFP /= self._cellsAteSomething
        else:
            return
    def _updateSimInitFPMed(self, genData):
        self._medianSimInitFP *= (len(self._gens) - 1)
        self._medianSimInitFP += genData.medianInitFoodPref()
        self._medianSimInitFP /= len(self._gens)
    def _updateSimSizeMed(self, genData):
        self._medianSimSize *= (len(self._gens) - 1)
        self._medianSimSize += genData.medianSize()
        self._medianSimSize /= len(self._gens)
    def _updateSimCarnSizeMed(self, genData):
        self._medianSimCarnSize *= (self._carnCells - 1)
        self._medianSimCarnSize += genData.medianCarnSize()
        self._medianSimCarnSize /= self._carnCells
    def _updateSimHerbSizeMed(self, genData):
        self._medianSimHerbSize *= (self._herbCells - 1)
        self._medianSimHerbSize += genData.medianHerbSize()
        self._medianSimHerbSize /= self._herbCells

    # some methods that return various instance objects
    def gens(self):
        return self._gens
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
    def medianSimSize(self):
        return self._medianSimSize
    def medianSimCarnSize(self):
        return self._medianSimCarnSize
    def medianSimHerbSize(self):
        return self._medianSimHerbSize
    def medianSimSecondsAlive(self):
        return self._medianSimSecondsAlive
    def medianSimActFP(self):
        return self._medianSimActFP
    def medianSimInitFP(self):
        return self._medianSimInitFP
    def medianSimSurv(self):
        return self._medianSimSurv