import sys
import numpy as np   
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QWidget, 
                              QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                              QComboBox, QGridLayout, QScrollArea, QMessageBox)
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtCore import Qt, QRectF


class MainWindow(QMainWindow):
    def __init__(self):  # Fixed method name from __int__ to __init__
        super().__init__()
        self.setWindowTitle("Mini CAD")
        self.setGeometry(100, 100, 1200, 800)

        # Create main central widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Left side placeholder for graph (you can replace this later)
        graph_placeholder = QWidget()
        graph_placeholder.setStyleSheet("background-color: white;")
        
        
        ##########################################################
        # Tab panel 
        #
        # Create left side panel with tabs (moved from right side)
        left_panel = QtWidgets.QTabWidget()
        left_panel.setFixedWidth(300)  # Set width of the side panel
        
        # Create tabs
        env_tab  = QWidget()
        gond_tab = QWidget()
        eng_tab  = QWidget()
        fin_tab  = QWidget()
        
        # Add tabs to the panel
        left_panel.addTab(env_tab,  "Main Envelope")
        left_panel.addTab(gond_tab, "Gondola")
        left_panel.addTab(eng_tab,  "Engine")
        left_panel.addTab(fin_tab,  "Fins")
        
        ##############################
        # Create layouts for each tab
        env_layout  = QVBoxLayout()
        gond_layout = QVBoxLayout()
        eng_layout  = QVBoxLayout()
        fin_layout  = QVBoxLayout()
        ##############################
        
        
        ###############################
        # Main Envelope Tab
        #
        env_layout.addWidget(QLabel("Shape:"))
        shape_combo = QComboBox()
        shape_combo.addItems(["Line", "spline"])
        env_layout.addWidget(shape_combo)
        env_layout.addStretch()
        
        
        ####################################
        # Gondola Tab
        gond_layout.addWidget(QLabel("Color:"))
        color_combo = QComboBox()
        color_combo.addItems(["Sweep","Loft","Revolve"])
        gond_layout.addWidget(color_combo)
        gond_layout.addStretch()
        
        
        ####################################
        # Engine
        eng_layout.addWidget(QLabel("Grid Size:"))
        eng_layout.addWidget(QLineEdit())
        eng_layout.addStretch()
        
        
        #####################################
        # Fins
        fin_layout.addWidget(QLabel("Number of Fins:"))
        fin_layout.addWidget(QLineEdit())
        fin_layout.addStretch()
        
        
        ######
        ######
        
        #########################
        # Set layouts for tabs
        env_tab.setLayout(env_layout)
        gond_tab.setLayout(gond_layout)
        eng_tab.setLayout(eng_layout)
        fin_tab.setLayout(fin_layout)
        
        #####################
        # Layout for panels # 
        #####################
        # Add widgets to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(graph_placeholder, stretch=2)
        
        
        # Set the main layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())