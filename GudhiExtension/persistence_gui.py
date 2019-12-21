import sys

from PySide2.QtWidgets import (QApplication, QMainWindow, QTabWidget)
from PySide2.QtCore import QCoreApplication

from CustomQWidgets.filtration_tab_widget import FiltrationTabWidget
from CustomQWidgets.persistence_graphs_tab_widget import PersistenceGraphsTabWidget
from CustomQWidgets.setup_tab_widget import SetupTabWidget
from GudhiExtension.computation_handler import computation_handler


class PlotSliderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QTabWidget()
        self.setCentralWidget(self._main)
        self.setMinimumSize(800,800)

        self.computation_handler = computation_handler(True)

        self.setup_tab = SetupTabWidget(self)
        self.persistence_graphs = PersistenceGraphsTabWidget(self)

        self._main.addTab(self.setup_tab, "Setup")
        self._main.addTab(self.persistence_graphs, "Persistence Graphs")


    def generate_filtration_tab(self):
        filtration_tab = FiltrationTabWidget(self.computation_handler)
        self._main.addTab(filtration_tab, "Filtration")

    def update_persistence_graphs(self):
        self.persistence_graphs.update()
        QCoreApplication.processEvents()

if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    app = PlotSliderWindow()
    app.show()
    qapp.exec_()
