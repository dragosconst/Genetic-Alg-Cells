# This is the main program source file.

# here we import standard libraries\modules
import sys
from enum import Enum

# here we import third party libraries\modules
from PyQt5 import QtCore, QtGui, QtWidgets
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

# this enum class is used for encoding the tabs
class Tabs(Enum):
    SimSurvTab = 1
    SimSurvTitle = "Sim Median Survivability over Gens"
    SimSizeTab = 2
    SimSizeTitle= "Sim Median Size over Gens"
    SimCarnSizeTab = 3
    SimHerbSizeTab = 4
    SimSecAliveTab = 5
    SimActFPTab = 6
    SimInitFPTab = 7

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

        self.actionNew_simulation.triggered.connect(lambda: self._newSimDia()) # when the "New gen" menu option is clicked


    # opens a dialog for creating a new generation
    def _newSimDia(self):
        newSimDialog = NewSimDia(self)
        newSimDialog.exec_()

    # clears the old scene, should a new simulation be created
    def _clearScene(self):
        scene = self.mapScene
        for item in scene.items():
            scene.removeItem(item)
            del item

    # removes all items from the previous scene and clears all lists
    def _delOldSim(self):
        # kill the simulation
        self._currentSim.killSim()
        self._currentSim = None

        # remove items from scene
        self._clearScene()

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
    def updateTab(self, index, fig, axis, xVals, yVals, title=""):
        if index > len(self._plots): # if the update method is called on a non existent tab
            self.addTab(fig, axis, title)
            return
        index -= 1 # the index used will be greater with one than the index of the tab in order to correctly add a new
                   # tab if this tab doesn't already exist

        print(index, xVals, yVals)
        currAxis = self._axes[index]
        oldFig = self._figs[index]
        currAxis.cla()
        currAxis.plot(xVals, yVals)
        oldFig.canvas.draw()
        

    # this functions deletes the tab specified by the index
    def removeTab(self, index):
        toDelete = self.graphs.findChild(QtWidgets.QWidget, "Canvas" + str(index))
        self.graphs.removeTab(index) # this only removes the tab from the tab widget, it doesn't actually delete the widget used for the tab
        del self._plots[index] # removes the objects associated with this tab
        del self._navtbs[index]
        del self._timers[index]
        del toDelete # not sure if manual deletion is necessary, doing it anyway

if __name__ == '__main__': # yeah i guess we have to use this
    app = QtWidgets.QApplication(sys.argv)
    qtApp = MLCellWindow()
    qtApp.show()

    
    sys.exit(app.exec_())

