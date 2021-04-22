from PySide2.QtWidgets import (QVBoxLayout, QWidget, QPushButton, QGroupBox, QGridLayout, QLineEdit)
from PySide2.QtCore import Slot

from PersistenceGUI.point_cloud_generation_widget import PointCloudGenerationWidget

#Widget containing the layout and interactive elements of the user interactable setup
class SetupTabWidget(QWidget):
    def __init__(self, main_ui):
        super().__init__()
        self.layout = QGridLayout(self)
        self.main_ui = main_ui

        point_set_generation_box = QGroupBox("Point Set Generation")
        point_set_generation_layout = QVBoxLayout(point_set_generation_box)
        point_cloud_widget = PointCloudGenerationWidget(self, self.main_ui.alpha_complex)
        point_set_generation_layout.addWidget(point_cloud_widget)
        point_set_generation_box.setMaximumWidth(250)
        point_set_generation_box.setMaximumHeight(250)
        self.layout.addWidget(point_set_generation_box)

        point_set_pass_box = QGroupBox("Point Set Pass")
        point_set_pass_layout = QVBoxLayout(point_set_pass_box)
        point_set_pass_box.setMaximumWidth(250)
        point_set_pass_box.setMaximumHeight(150)
        self.in_field = QLineEdit()
        point_set_pass_layout.addWidget(self.in_field)
        pass_button = QPushButton("Set Point Set")

        pass_button.clicked.connect(self.pass_points)
        point_set_pass_layout.addWidget(pass_button)

        self.layout.addWidget(point_set_pass_box)

        self.generate_filtration_vis = QPushButton("Visualize Filtration")

        self.generate_filtration_vis.clicked.connect(self.main_ui.generate_filtration_tab)

        self.generate_algorithm_vis = QPushButton("Visualize Column Algorithm")

        self.generate_algorithm_vis.clicked.connect(self.main_ui.generate_column_algo_tab)

        self.layout.addWidget(self.generate_filtration_vis)
        self.layout.addWidget(self.generate_algorithm_vis)


    @Slot()
    def pass_points(self):
        points = eval(self.in_field.text())
        self.main_ui.set_point_cloud(points)