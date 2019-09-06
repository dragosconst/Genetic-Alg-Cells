# This is the main program source file.

# here we import standard libraries\modules
import sys
import functools

# here we import third party libraries\modules
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure # at this point, these are imported only for testing stuff, although they might prove to be useful later on
from matplotlib.backends.backend_qt5agg import(
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavToolbar)
import numpy as np

# here we import local modules
from GUI import MainWindow as mw

class MLCellApp(mw.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self): 
        super().__init__()
        self.setupUi(self)
        self.tabLayouts = [] # this list will contain every layout from every tab
        self.plots = [] # this list will contain every math plot from every tab
        self.navtbs = [] # this list will contain every nav toolbar from every tab
        self.timers = []

    # this function adds a new graph plot and navbar to the tab widget
    def addNewPlot(self, fig, axis, yVals):

        newTab = QtWidgets.QWidget(self.graphs, objectName = "Canvas " + str(self.graphs.count())) # creating a new tab
        self.graphs.addTab(newTab, newTab.objectName()) # adding it to the graphs tab widget
        self.graphs.setCurrentWidget(newTab) # setting the current widget(tab) to this tab

        self.tabLayouts.append(QtWidgets.QVBoxLayout(newTab)) # here I add a new vertical layout to the current tab widget
        self.plots.append(FigureCanvas(fig)) # adds a new widget to the plots list, constructed with the fig parameter
        currentIndex = self.graphs.count() - 1 # I substract 1 because the index for the lists start at 0
        self.tabLayouts[currentIndex].addWidget(self.plots[currentIndex])
        self.navtbs.append(NavToolbar(self.plots[currentIndex], newTab, coordinates = True)) # adds a nav toolbar under the graph
        self.tabLayouts[currentIndex].addWidget(self.navtbs[currentIndex])
        
        # add a QTimer
        self.timers.append(QtCore.QTimer())

        self.updateTab(currentIndex, fig, axis, yVals)

    # this function should change a tab's content with the newly given plot
    def updateTab(self, index, newPlot, axis, yVals):
        axis.cla() # clear the graph

        # following code is for making a real nice live update
        newYVals = yVals
        newYVals = np.delete(newYVals, range(1)) # deletes the first five elements of the array 
        newYVals = np.append(newYVals, np.random.rand(1)) # adds five elements to the end of the array
        axis.plot(newYVals) # plots the new functions
        newPlot.canvas.draw() # this redraws the plot
        
        time = self.timers[index]
        time.singleShot(1000, lambda: self.updateTab(index, newPlot, axis, newYVals)) # not using singleShot makes some weird problems, where there are multiple timers working at the same time, instead of just one(or how many tabs are open)
     
         

    # this function updates all the tab names(and objectNames) accordingly, it is a private function because I feel that, at the moment at least
    # there is no good reason for this to be called outside class functions
    # this function might also prove to be useless later on, since this tab naming is currently used just for testing
    def _updateTabNames(self):
        for i in range(self.graphs.count()):
            self.graphs.setCurrentIndex(i) # it opens the current tab
            currentTab = self.graphs.currentWidget() # objects are passed by reference(they are mutable), therefore any modifications done here change the widget for the current tab too
            currentTab.setObjectName("Canvas " + str(i))
            self.graphs.setTabText(i, "Canvas " + str(i))

    # this functions deletes the tab specified by the index
    def removeTab(self, index):
        toDelete = self.graphs.findChild(QtWidgets.QWidget, "Canvas" + str(index))
        self.graphs.removeTab(index) # this only removes the tab from the tab widget, it doesn't actually delete the widget used for the tab
        del self.plots[index] # removes the objects associated with this tab
        del self.navtbs[index]
        del self.timers[index]
        del toDelete # not sure if manual deletion is necessary, doing it anyway
        self._updateTabNames() # update the tab names

if __name__ == '__main__': # yeah i guess we have to use this

    fig1, fig2, fig3 = Figure(), Figure(), Figure() # some testing code
    axes1 = fig1.add_subplot(111)
    axes2 = fig2.add_subplot(111)
    yValues1 = np.random.rand(50)
    yValues2 = np.random.rand(50)
    axes1.plot(yValues1)
    axes2.plot(yValues2)

    app = QtWidgets.QApplication(sys.argv)
    qtApp = MLCellApp()
    qtApp.addNewPlot(fig1, axes1, yValues1)
    qtApp.addNewPlot(fig2, axes2, yValues2)
    qtApp.show()

    
    sys.exit(app.exec_())
