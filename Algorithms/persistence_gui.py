import sys

from PySide2.QtWidgets import (QApplication, QMainWindow, QTabWidget)
from PySide2.QtCore import QCoreApplication, Slot

from CustomQWidgets.filtration_tab_widget import FiltrationTabWidget
from CustomQWidgets.persistence_graphs_tab_widget import PersistenceGraphsTabWidget
from CustomQWidgets.setup_tab_widget import SetupTabWidget
from Algorithms.alpha_complex_wrapper import alpha_complex_wrapper
import Algorithms.point_cloud_generator


class PlotSliderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QTabWidget()
        self.setCentralWidget(self._main)
        self.setMinimumSize(800,800)

        self.point_cloud = [[0.25,0.4],[0.1,0],[0,0.9], [.2,.5]]
        self.alpha_complex = alpha_complex_wrapper(self.point_cloud)

        self.setup_tab = SetupTabWidget(self)
        self.persistence_graphs = PersistenceGraphsTabWidget(self)

        self._main.addTab(self.setup_tab, "Setup")
        self._main.addTab(self.persistence_graphs, "Persistence Graphs")


    @Slot()
    def generate_filtration_tab(self):
        filtration_tab = FiltrationTabWidget(self.alpha_complex)
        self._main.addTab(filtration_tab, "Filtration")

    def update_persistence_graphs(self):
        self.persistence_graphs.update()
        QCoreApplication.processEvents()

    def compute_alpha_complex(self):
        self.alpha_complex = alpha_complex_wrapper(self.point_cloud)
        self.persistence_graphs.update()

    @Slot()
    def set_point_cloud(self, points):
        self.point_cloud = points
        self.compute_alpha_complex()

        dim = len(points[0])
        if dim ==2:
            self.setup_tab.generate_filtration_vis.setEnabled(True)
        else:
            self.setup_tab.generate_filtration_vis.setEnabled(False)

if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    app = PlotSliderWindow()
    app.show()
    qapp.exec_()
