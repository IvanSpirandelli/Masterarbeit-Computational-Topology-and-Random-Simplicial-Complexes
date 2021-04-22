from PySide2.QtWidgets import (QStackedWidget)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import Algorithms.column_algo.column_algorithm as ca
import Algorithms.column_algo.column_algo_outs as cao

#The Stack of plots that illustrate the computation steps of the standard reduction scheme
class ColumnAlgoStackWidget(QStackedWidget):
    def __init__(self, parent, filtration):
        super().__init__()
        self.setParent(parent)
        mat = ca.build_boundary_matrix_from_filtration(filtration, False, False)

        labels = [elem for elem in filtration ]

        static_canvas = FigureCanvas(Figure(figsize=(8, 8)))
        _static_ax = static_canvas.figure.subplots()
        cao.mat_visualization_for_gui(mat, _static_ax, labels, labels)
        self.addWidget(static_canvas)

        for _,_,step in ca.column_algorithm_iterator(mat):
            static_canvas = FigureCanvas(Figure(figsize=(8, 8)))
            _static_ax = static_canvas.figure.subplots()

            cao.mat_visualization_for_gui(step,_static_ax,labels,labels)

            self.addWidget(static_canvas)

        self.removeWidget(self.widget(self.count()))

