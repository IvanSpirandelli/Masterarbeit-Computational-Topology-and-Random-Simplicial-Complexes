import random

import PySide2
import gudhi

from PySide2.QtWidgets import (QVBoxLayout, QWidget, QSlider, QPushButton, QHBoxLayout)
from PySide2.QtCore import Slot, Qt

from CustomQWidgets.filtration_stack_widget import FiltrationStackWidget


class FiltrationTabWidget(QWidget):
    def __init__(self, comp_handler):
        super().__init__()
        self.comp_handler = comp_handler

        self.canvas_stack = FiltrationStackWidget(self, self.comp_handler.points, self.comp_handler.alpha.simplex_tree)

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