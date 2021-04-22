import sys

from PySide2.QtWidgets import (QApplication, QMainWindow, QTabWidget)
from PySide2.QtCore import QCoreApplication, Slot

from PersistenceGUI.column_algo_tab_widget import ColumnAlgoTabWidget
from PersistenceGUI.filtration_tab_widget import FiltrationTabWidget
from PersistenceGUI.persistence_graphs_tab_widget import PersistenceGraphsTabWidget
from PersistenceGUI.setup_tab_widget import SetupTabWidget
from Algorithms.alphacomplexwrapper import AlphaComplexWrapper

#This is the main widget of a GUI that allows the user to generate point clouds and compute
#persistent homology on them. It is possible to visualize the filtration as well as the matrix
#reduction of the standard reduction scheme.

class PersistenceGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QTabWidget()
        self.setCentralWidget(self._main)
        self.setMinimumSize(800, 800)

        self.point_cloud = [[0.25, 0.4], [0.1, 0], [0, 0.9], [.2, .5]]
        self.alpha_complex = AlphaComplexWrapper(self.point_cloud)

        self.setup_tab = SetupTabWidget(self)
        self.persistence_graphs = PersistenceGraphsTabWidget(self)

        self._main.addTab(self.setup_tab, "Setup")
        self._main.addTab(self.persistence_graphs, "Persistence Graphs")

    def update_persistence_graphs(self):
        self.persistence_graphs.update()
        QCoreApplication.processEvents()

    def compute_alpha_complex(self):
        self.alpha_complex = AlphaComplexWrapper(self.point_cloud)
        self.persistence_graphs.update()

    @Slot()
    def generate_filtration_tab(self):
        filtration_tab = FiltrationTabWidget(self.alpha_complex)
        self._main.addTab(filtration_tab, "Filtration")

    @Slot()
    def generate_column_algo_tab(self):
        column_algo_tab = ColumnAlgoTabWidget(self.alpha_complex)
        self._main.addTab(column_algo_tab, "Column algo")

    @Slot()
    def set_point_cloud(self, points):
        self.point_cloud = points
        self.compute_alpha_complex()

        dim = len(points[0])
        if dim == 2:
            self.setup_tab.generate_filtration_vis.setEnabled(True)
        else:
            self.setup_tab.generate_filtration_vis.setEnabled(False)


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    app = PersistenceGUI()
    app.show()
    qapp.exec_()
