import random

import PySide2
import gudhi

from PySide2.QtWidgets import (QVBoxLayout, QWidget, QSlider, QPushButton, QHBoxLayout)
from PySide2.QtCore import Slot, Qt

from PersistenceGUI.filtration_stack_widget import FiltrationStackWidget

#Tab controlling the display of the FiltrationStackWidget
class FiltrationTabWidget(QWidget):
    def __init__(self, alpha_complex):
        super().__init__()
        self.alpha_complex = alpha_complex

        self.canvas_stack = FiltrationStackWidget(self, self.alpha_complex.points, self.alpha_complex.simplex_tree)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.canvas_stack.count()-1)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_button_clicked)

        bottom = QWidget()
        bottom_layout = QHBoxLayout(bottom)
        bottom_layout.addWidget(self.slider)
        bottom_layout.addWidget(delete_button)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas_stack)
        self.layout.addWidget(bottom)

        # Connecting the signal
        self.slider.valueChanged.connect(self.slide)

    @Slot()
    def slide(self):
        self.canvas_stack.setCurrentIndex(self.slider.value())

    @Slot()
    def delete_button_clicked(self):
        self.deleteLater()

    def keyPressEvent(self, event: PySide2.QtGui.QKeyEvent):
        if event.key() == Qt.Key_M:
            self.slider.setValue(self.slider.value() + 1)

        if event.key() == Qt.Key_N:
            self.slider.setValue(self.slider.value() - 1)