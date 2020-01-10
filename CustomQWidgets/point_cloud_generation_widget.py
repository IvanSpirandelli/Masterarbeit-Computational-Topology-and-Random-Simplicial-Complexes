import random

import PySide2
import gudhi
from PySide2.QtGui import QIntValidator

from PySide2.QtWidgets import (QVBoxLayout, QWidget, QSlider, QGridLayout, QLineEdit, QLabel, QHBoxLayout, QCheckBox,
                               QPushButton)
from PySide2.QtCore import Slot, Qt, QSize

from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper
import GudhiExtension.point_cloud_generator as pcg


class PointCloudGenerationWidget(QWidget):
    def __init__(self, parent, point_cloud_generator, alpha_complex):
        super().__init__()
        self.parent = parent

        self.setWindowTitle("Point generation")


        input_fields = QWidget()
        input_layout = QVBoxLayout(input_fields)
        input_layout.setAlignment(Qt.AlignTop)


        input_layout.addWidget(QLabel("Number of points:"))
        self.num_of_points = QLineEdit()
        self.num_of_points.setValidator(QIntValidator(1,999999))
        self.num_of_points.setMaxLength(6)
        self.num_of_points.insert("3")
        input_layout.addWidget(self.num_of_points)

        input_layout.addWidget(QLabel("Dimension:"))
        self.dimension = QLineEdit()
        self.dimension.setValidator(QIntValidator(1,99))
        self.dimension.setMaxLength(2)
        self.dimension.insert("2")
        input_layout.addWidget(self.dimension)

        grid = QWidget()
        grid_layout = QHBoxLayout(grid)

        self.dilation = QLineEdit()
        self.dilation.setValidator(QIntValidator(1, 999999))
        self.dilation.setMaxLength(6)
        self.dilation.insert("50")

        self.grid_check = QCheckBox("Grid")
        self.grid_check.stateChanged.connect(self.grid_check_slot)
        self.grid_check.setChecked(True)
        grid_layout.addWidget(self.grid_check)

        grid_layout.addWidget(QLabel("Dilation:"))
        grid_layout.addWidget(self.dilation)
        input_layout.addWidget(grid)

        generate_points = QPushButton("Generate")
        generate_points.clicked.connect(self.generate_points_clicked)
        input_layout.addWidget(generate_points)

        self.main_layout = QGridLayout(self)
        self.main_layout.addWidget(input_fields,0,0)

    @Slot()
    def grid_check_slot(self):
        if(self.grid_check.isChecked()):
            self.dilation.setEnabled(True)
        else:
            self.dilation.setEnabled(False)

    @Slot()
    def generate_points_clicked(self):

        if(self.grid_check.isChecked()):
            points = pcg.generate_n_gridpoints_of_dim_with_dilation(
                int(self.num_of_points.text()),
                int(self.dimension.text()),
                int(self.dilation.text()))
            self.parent.main_ui.set_point_cloud(points)
            self.parent.main_ui.compute_alpha_complex()

        else:
            points = pcg.generate_n_points(
                int(self.num_of_points.text()),
                int(self.dimension.text()))
            self.parent.main_ui.set_point_cloud(points)
            self.parent.main_ui.compute_alpha_complex()

        self.parent.main_ui.update_persistence_graphs()
