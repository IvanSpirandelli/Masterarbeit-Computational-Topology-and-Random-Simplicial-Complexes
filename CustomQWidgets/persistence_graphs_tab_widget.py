import numpy
import gudhi

from PySide2.QtCore import Slot

from PySide2.QtWidgets import (QStackedWidget, QWidget, QVBoxLayout, QRadioButton, QHBoxLayout)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PersistenceGraphsTabWidget(QWidget):
    def __init__(self, main_ui):
        super().__init__()
        self.main_ui = main_ui

        buttons = QWidget()
        button_layout = QHBoxLayout()

        self.barcode_button = QRadioButton("Barcode")
        self.barcode_button.setChecked(True)
        self.barcode_button.clicked.connect(self.barcode_show)
        self.diagram_button = QRadioButton("Diagram")
        self.diagram_button.clicked.connect(self.diagram_show)
        self.density_button = QRadioButton("Density")
        self.density_button.clicked.connect(self.density_show)

        button_layout.addWidget(self.barcode_button)
        button_layout.addWidget(self.diagram_button)
        button_layout.addWidget(self.density_button)

        buttons.setLayout(button_layout)


        self.figures = QStackedWidget()

        self.add_diagram_widgets()

        self.figures.setCurrentIndex(0)

        layout = QVBoxLayout()
        layout.addWidget(buttons)
        layout.addWidget(self.figures)
        self.setLayout(layout)

    @Slot()
    def barcode_show(self):
        self.figures.setCurrentIndex(0)

    @Slot()
    def diagram_show(self):
        self.figures.setCurrentIndex(1)

    @Slot()
    def density_show(self):
        self.figures.setCurrentIndex(2)

    def add_diagram_widgets(self):
        plot = gudhi.plot_persistence_barcode(persistence=self.main_ui.alpha_complex.persistence, max_intervals = 1000,
                                              legend=False)
        barcode_canvas = FigureCanvas(plot.figure(1))
        plot.close()

        plot = gudhi.plot_persistence_diagram(persistence=self.main_ui.alpha_complex.persistence,
                                              legend=False)
        diagram_canvas = FigureCanvas(plot.figure(1))
        plot.close()

        density_canvas = FigureCanvas(plot.figure(1))
        try:
            plot = gudhi.plot_persistence_density(persistence=self.main_ui.alpha_complex.persistence,
                                              max_intervals=1000, dimension = 1,
                                          legend=True)
            plot.close()
        except:
            print("Density computation not possible")

        self.figures.addWidget(barcode_canvas)
        self.figures.addWidget(diagram_canvas)
        self.figures.addWidget(density_canvas)

    def update(self):
        self.figures.removeWidget(self.figures.currentWidget())
        self.figures.removeWidget(self.figures.currentWidget())
        self.figures.removeWidget(self.figures.currentWidget())
        self.add_diagram_widgets()




