import sys

from PySide2.QtWidgets import (QApplication, QMainWindow, QTabWidget)
from PySide2.QtCore import QCoreApplication

from CustomQWidgets.filtration_tab_widget import FiltrationTabWidget
from CustomQWidgets.persistence_graphs_tab_widget import PersistenceGraphsTabWidget
from CustomQWidgets.setup_tab_widget import SetupTabWidget
from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper
from GudhiExtension.point_cloud_generator import point_cloud_generator


class PlotSliderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QTabWidget()
        self.setCentralWidget(self._main)
        self.setMinimumSize(800,800)

        self.point_cloud = point_cloud_generator()
        self.alpha_complex = alpha_complex_wrapper()

        self.setup_tab = SetupTabWidget(self)
        self.persistence_graphs = PersistenceGraphsTabWidget(self)

        self._main.addTab(self.setup_tab, "Setup")
        self._main.addTab(self.persistence_graphs, "Persistence Graphs")


    def generate_filtration_tab(self):
        filtration_tab = FiltrationTabWidget(self.alpha_complex)
        self._main.addTab(filtration_tab, "Filtration")

    def update_persistence_graphs(self):
        self.persistence_graphs.update()
        QCoreApplication.processEvents()

if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    app = PlotSliderWindow()
    app.show()
    qapp.exec_()
