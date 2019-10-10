# This is the main program source file.

# here we import standard libraries\modules
import sys
from enum import Enum

# here we import third party libraries\modules
from PySide2 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure # at this point, these are imported only for testing stuff, although they might prove to be useful later on
from matplotlib.backends.backend_qt5agg import(
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavToolbar)
import numpy as np

# here we import local modules
from Cells import Cell
from Walls import Wall
import util
import MainWindow as mw
from NewSimDia import NewSimDia
from Algae import Alga
from AlgaeBloom import Bloom
import Sims
import Saves
import Loads

# this enum class is used for encoding the tabs
class Tabs(Enum):
    SimSurvTab = 1
    SimSurvTitle = "Survivability"
    SimSizeTab = 2
    SimSizeTitle= "Size"
    SimCarnSizeTab = 3
    SimCarnSizeTitle = "Carn Size"
    SimHerbSizeTab = 4
    SimHerbSizeTitle = "Herb Size"
    SimSecAliveTab = 5
    SimSecAliveTitle = "Secs Alive"
    SimActFPTab = 6
    SimActFPTitle = "Actual FP"
    SimInitFPTab = 7
    SimInitFPTitle = "Init FP"

# this class contains the main window of the application
# its methods handle stuff directly related to the functionality of the main window AND JUST THAT
# all the classes and methods relevant to the evolutionary algorithm can be found in other files
class MLCellWindow(mw.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.mapScene = QtWidgets.QGraphicsScene() # create a graphics scene for drawing etc
        self.mapScene.setSceneRect(0, 0, 1000, 1000) # the painting area will be fixed to 1000 x 1000, the size of the map
        self.mapGView.setScene(self.mapScene)

        self._tabLayouts = [] # this list will contain every layout from every tab
        self._plots = [] # this list will contain every math plot from every tab
        self._axes = [] # the axis of the plots
        self._figs = [] # the figure objects
        self._navtbs = [] # this list will contain every nav toolbar from every tab

        self._currentSim = None # the current simulation

        self._savePath = None # this will be used for storing the current save path

        self.actionNew_simulation.triggered.connect(lambda: self._newSimDia()) # when the "New gen" menu option is clicked
        self.actionPause.triggered.connect(lambda: self._pauseApp())
        self.actionSavew.triggered.connect(lambda: self._saveSimulation())
        self.actionSave_as.triggered.connect(lambda: self._saveAsSimulation())
        self.actionOpen.triggered.connect(lambda: self._loadSim())

        self._isPaused = False # stores whether the current simulation is paused or not, in order to know what the pause button should do


    # load a simulation
    def _loadSim(self):
        if (self._currentSim is not None and self._currentSim.pauseability() == True) or self._currentSim == None: # dont load sims in pauses between generations of an ongoing sim
            if self._currentSim is not None:
                self._pauseApp() # pause the sim
            loadPath, _extension = QtWidgets.QFileDialog.getOpenFileName(self, "Select a Sim to load", "C://", "Sim Files (*.sim)")
            if _extension != "":
                if self._currentSim is not None: # if there was another sim running previous to this one
                    self._delOldSim()
                oldSim = Loads.LoadSim(loadPath, self.mapScene, self)
                self._currentSim = oldSim.loadSim()
                self._currentSim.startLoadSim()
            if self._currentSim is not None and self._isPaused == True:
                self._pauseApp() # unpause the sim

    # save a simulation
    def _saveSimulation(self):
        if self._currentSim is not None and self._currentSim.pauseability() == True: # only save when the sim can be paused, otherwise it's probably loading a generation and saving might corrupt data or something
            if self._savePath == None:
                self._saveAsSimulation()
            else:
                self._pauseApp() # pause before saving
                newSave = Saves.SaveSim(self._currentSim, self._savePath)
                newSave.saveSim()
                self._pauseApp() # unpause

    # for the save as action
    def _saveAsSimulation(self):
        if self._currentSim is not None and self._currentSim.pauseability() == True:
            self._pauseApp() # pause before savings
            print("pulicika ya")
            self._savePath, _extension = QtWidgets.QFileDialog.getSaveFileName(self, "Save Sim as", "C://", "Sim Files (*.sim)")
            if _extension != "":
                newSave = Saves.SaveSim(self._currentSim, self._savePath)
                newSave.saveSim()
            self._pauseApp() # unpause

    def _pauseApp(self):
        if self._currentSim is not None and self._currentSim.pauseability() == True:
            if self._isPaused == False:
                self._currentSim.pauseSim()
                self.actionPause.setText("Unpause")
                self._isPaused = True
            else:
                self._currentSim.restartSim()
                self.actionPause.setText("Pause")
                self._isPaused = False

    # opens a dialog for creating a new generation
    def _newSimDia(self):
        if self._currentSim is not None:
            self._currentSim.pauseSim()
        newSimDialog = NewSimDia(self)
        newSimDialog.exec_()

    # clears the old scene, should a new simulation be created
    def _clearScene(self):
        scene = self.mapScene
        for item in scene.items():
            scene.removeItem(item)
            del item

    # removes all items from the previous scene and clears all lists
    # also clears the graphs
    def _delOldSim(self):
        # kill the simulation
        self._currentSim.killSim()
        self._currentSim = None

        # remove items from scene
        self._clearScene()

        # remove the graphs
        for axis in self._axes:
            axis.cla()
        self._axes.clear()
        self._figs.clear()
        self.removeTabs()
        self._plots.clear()
        self._navtbs.clear()
        self._tabLayouts.clear()

    # starts a new simulation
    def _startNewSim(self, simDia, cellNo, secs, algaNo):
        if self._currentSim is not None: # if there was another sim running previous to this one
            self._delOldSim()
        self._currentSim = Sims.Sim(self.mapScene, cellNo, int(cellNo / 2) if algaNo == 0 else algaNo, secs, simDia, self)
        self._currentSim.startSim()

    # this function adds a new graph plot and navbar to the tab widget
    def addTab(self, fig, axis, title=""):

        newTab = QtWidgets.QWidget(self.graphs, objectName = title) # creating a new tab
        self._axes.append(axis)
        self._figs.append(fig)
        self.graphs.addTab(newTab, newTab.objectName()) # adding it to the graphs tab widget
        self.graphs.setCurrentWidget(newTab) # setting the current widget(tab) to this tab

        self._tabLayouts.append(QtWidgets.QVBoxLayout(newTab)) # here I add a new vertical layout to the current tab widget
        self._plots.append(FigureCanvas(fig)) # adds a new widget to the plots list, constructed with the fig parameter
        currentIndex = self.graphs.count() - 1 # I subtract 1 because the index for the lists start at 0
        self._tabLayouts[currentIndex].addWidget(self._plots[currentIndex])
        self._navtbs.append(NavToolbar(self._plots[currentIndex], newTab, coordinates = True)) # adds a nav toolbar under the graph
        self._tabLayouts[currentIndex].addWidget(self._navtbs[currentIndex])

    # this function should change a tab's content with the newly given plot
    def updateTab(self, index, fig, axis, xVals, yVals, title="", col="blue"):
        if index > len(self._plots): # if the update method is called on a non existent tab
            self.addTab(fig, axis, title)
            return
        index -= 1 # the index used will be greater with one than the index of the tab in order to correctly add a new
                   # tab if this tab doesn't already exist

        currAxis = self._axes[index]
        oldFig = self._figs[index]
        currAxis.cla()
        currAxis.plot(xVals, yVals, color=col)
        oldFig.canvas.draw()

    # this functions deletes the tab specified by the index
    def removeTabs(self):
        tabNo = self.graphs.count()
        while tabNo >= 0:
            currWid = self.graphs.widget(tabNo)
            self.graphs.removeTab(tabNo)
            del currWid
            tabNo -= 1

    # functions that return stuff
    def currentSim(self):
        return self._currentSim


if __name__ == '__main__': # yeah i guess we have to use this
    app = QtWidgets.QApplication(sys.argv)
    qtApp = MLCellWindow()
    qtApp.show()


    sys.exit(app.exec_())

