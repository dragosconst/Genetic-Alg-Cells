
from Cells import Cell
from AlgaeBloom import Bloom
from Algae import Alga
from GenDataCls import GenData
import util

class Gen():
    def __init__(self, scene, cellsNo, algaeNo, genSec, simDia = None):
        # basic generation values
        self._scene = scene
        self._cellsNo = cellsNo
        self._algaeNo = algaeNo
        self._genSec = genSec
        self._simDia = simDia

    # adds the specified cells number to the scene
    def _addCells(self):
        for i in range(0, self._cellsNo):
            self._scene.addItem(Cell())
    # adds the specified number of algae to the scene
    def _addAlgae(self):
        leftBloom = Bloom(100, 200, 300, 300)
        rightBloom = Bloom(600, 600, 300, 300)
        for i in range(0, self._algaeNo):
            self._scene.addItem(Alga(10, 10, leftBloom, rightBloom))


    # method for starting a generation
    def startGeneration(self):
        Alga.DESIRED_POP = self._algaeNo
        Alga.disjoint = 0
        Alga.population = 0
        self._addAlgae()
        Alga.resetAlgae(self._scene, self._simDia, self._algaeNo + self._cellsNo)

        Cell.CELL_GEN_POP = self._cellsNo
        Cell.cellDisjoint = 0
        self._addCells()
        Cell.resetCells(self._scene, self._simDia, self._algaeNo + self._cellsNo, self._algaeNo)
        Cell.startMoving(self._scene)

    def killGen(self):
        for item in self._scene.items():
            if util.getClassName(item) != "Wall": # dont delete the walls
                item.die() # the die method removes cells\algae from the scene and deletes their instances
    
