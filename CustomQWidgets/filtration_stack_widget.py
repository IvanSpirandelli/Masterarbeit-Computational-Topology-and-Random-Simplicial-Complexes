from PySide2.QtWidgets import (QStackedWidget)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Algorithms import sc_drawer


class FiltrationStackWidget(QStackedWidget):
    def __init__(self, parent, points, simplex_tree):
        super().__init__()
        self.setParent(parent)

        drawer = sc_drawer.sc_drawer(points, simplex_tree)

        last_dist = -1.0
        counter = 1

        while (True):
            static_canvas = FigureCanvas(Figure(figsize=(8, 8)))
            _static_ax = static_canvas.figure.subplots()
            current_dist = drawer.draw_filtration_2D(_static_ax, counter)

            if (current_dist == last_dist):
                break

            last_dist = current_dist
            counter += 1
            self.addWidget(static_canvas)

        self.removeWidget(self.widget(self.count()))

