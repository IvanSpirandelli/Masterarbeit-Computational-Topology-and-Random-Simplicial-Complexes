from PySide2.QtGui import QIntValidator

from PySide2.QtWidgets import (QVBoxLayout, QWidget, QGridLayout, QLineEdit, QLabel, QHBoxLayout, QCheckBox,
                               QPushButton)
from PySide2.QtCore import Slot, Qt

import Algorithms.point_cloud_generator as pcg

# Widget containing user input fields to generate point clouds
class PointCloudGenerationWidget(QWidget):
    def __init__(self, parent, alpha_complex):
        super().__init__()
        self.alpha_complex = alpha_complex
        self.parent = parent

        self.setWindowTitle("Point generation")

        input_fields = QWidget()
        input_layout = QVBoxLayout(input_fields)
        input_layout.setAlignment(Qt.AlignTop)

        num_of_points_widget = QWidget()
        num_of_points_layout = QGridLayout(num_of_points_widget)

        num_of_points_layout.addWidget(QLabel("Number of points:"), 0, 0)
        self.num_of_points = QLineEdit()
        self.num_of_points.setAlignment(Qt.AlignRight)
        self.num_of_points.setFixedWidth(50)
        self.num_of_points.setValidator(QIntValidator(1, 99999))
        self.num_of_points.setMaxLength(5)
        self.num_of_points.insert("3")
        num_of_points_layout.addWidget(self.num_of_points, 0, 1)
        input_layout.addWidget(num_of_points_widget)

        dimension_widget = QWidget()
        dimension_layout = QGridLayout(dimension_widget)

        dimension_layout.addWidget(QLabel("Dimension:"), 0, 0)
        self.dimension = QLineEdit()
        self.dimension.setAlignment(Qt.AlignRight)
        self.dimension.setFixedWidth(50)
        self.dimension.setValidator(QIntValidator(1, 99))
        self.dimension.setMaxLength(2)
        self.dimension.insert("2")
        dimension_layout.addWidget(self.dimension, 0, 1)

        input_layout.addWidget(dimension_widget)

        grid = QWidget()
        grid_layout = QHBoxLayout(grid)

        self.dilation = QLineEdit()
        self.dilation.setValidator(QIntValidator(1, 999999))
        self.dilation.setMaxLength(6)
        self.dilation.setEnabled(False)
        self.dilation.setAlignment(Qt.AlignRight)
        self.dilation.setFixedWidth(50)
        self.dilation.insert("1")

        self.grid_check = QCheckBox("Grid")
        self.grid_check.stateChanged.connect(self.grid_check_slot)
        self.grid_check.setChecked(False)
        grid_layout.addWidget(self.grid_check)

        grid_layout.addWidget(QLabel("Dilation:"))
        grid_layout.addWidget(self.dilation)
        input_layout.addWidget(grid)

        generate_points = QPushButton("Generate")
        generate_points.clicked.connect(self.generate_points_clicked)
        input_layout.addWidget(generate_points)

        self.main_layout = QGridLayout(self)
        self.main_layout.addWidget(input_fields, 0, 0)

    @Slot()
    def grid_check_slot(self):
        if self.grid_check.isChecked():
            self.dilation.setEnabled(True)
        else:
            self.dilation.setEnabled(False)

    @Slot()
    def generate_points_clicked(self):

        if self.grid_check.isChecked():
            points = pcg.generate_n_grid_points_of_dim_with_dilation(
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
