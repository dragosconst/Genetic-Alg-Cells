# This is the main program source file.

# here we import standard libraries\modules
import sys

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

    # this function adds a new graph plot and navbar to the tab widget
    def addNewPlot(self, fig):
        _newTab = QtWidgets.QWidget(self.status, objectName = "Canvas " + str(self.status.count())) # creating a new tab
        self.status.addTab(_newTab, "Canvas " + str(self.status.count())) # adding it to the status tab widget
        self.status.setCurrentWidget(self.status.findChild(QtWidgets.QWidget, "Canvas " + str(self.status.count() - 1))) # setting the current widget(tab) to this tab

        self.tabLayouts.append(QtWidgets.QVBoxLayout(self.status.currentWidget())) # here I add a new vertical layout to the current tab widget
        self.plots.append(FigureCanvas(fig)) # adds a new widget to the plots list, constructed with the fig parameter
        currentIndex = self.status.count() - 1 # I substract 1 because the index for the lists start at 0
        self.tabLayouts[currentIndex].addWidget(self.plots[currentIndex])
        self.navtbs.append(NavToolbar(self.plots[currentIndex], self.status.currentWidget(), coordinates = True)) # adds a nav toolbar under the graph
        self.tabLayouts[currentIndex].addWidget(self.navtbs[currentIndex])

if __name__ == '__main__': # yeah i guess we have to use this

    fig1, fig2 = Figure(), Figure() # some testing code
    axes1 = fig1.add_subplot(111)
    axes2 = fig2.add_subplot(111)
    axes1.plot(np.random.rand(50))
    axes2.plot(np.random.rand(50))

    app = QtWidgets.QApplication(sys.argv)
    qtApp = MLCellApp()
    qtApp.addNewPlot(fig1)
    qtApp.addNewPlot(fig2)
    qtApp.show()
    sys.exit(app.exec_())