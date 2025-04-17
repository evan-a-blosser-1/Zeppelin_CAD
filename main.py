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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

sys.dont_write_bytecode = True
from config import clear_plot


class MainWindow(QMainWindow):
    def __init__(self):  # Fixed method name from __int__ to __init__
        super().__init__()
        self.setWindowTitle("Zeppelin CAD")
        self.setWindowState(Qt.WindowMaximized)

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
        env_grid = QGridLayout()
        
        self.E_len_label = QLabel("Length:")
        self.E_len = QLineEdit("100")
        self.E_per_label = QLabel("Mid-Section (%):")
        self.E_per = QLineEdit("0.20")
        
        # Add widgets to grid layout
        env_grid.addWidget(self.E_len_label, 0, 0)
        env_grid.addWidget(self.E_len, 0, 1)
        env_grid.addWidget(self.E_per_label, 1, 0)
        env_grid.addWidget(self.E_per, 1, 1)
        
        # Create and add draw button
        self.draw_button = QPushButton("Draw Envelope")
        self.draw_button.clicked.connect(self.draw_envelope)
        
        # Add grid layout to main envelope layout
        env_layout.addLayout(env_grid)
        env_layout.addWidget(self.draw_button)
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
        
        
        
        #######################################################################
        #################
        # Bottom controls 
        # Create left side container
        left_container = QWidget()
        left_container_layout = QVBoxLayout()
        left_container.setLayout(left_container_layout)
        left_container.setFixedWidth(300)  # Match tab panel width
        
        # Create bottom control panel
        bottom_panel = QWidget()
        bottom_panel_layout = QVBoxLayout()
        bottom_panel.setLayout(bottom_panel_layout)
        bottom_panel.setStyleSheet("background-color: #f0f0f0; border: 1px solid #cccccc; margin-top: 10px;")
        
        # Add clear button to bottom panel
        self.clear_button = QPushButton("Clear Plot")
        self.clear_button.clicked.connect(lambda: clear_plot(self))
        bottom_panel_layout.addWidget(self.clear_button)
        
        # Add tab panel and bottom panel to left container
        left_container_layout.addWidget(left_panel)
        left_container_layout.addWidget(bottom_panel)
        
        
        
        
        #######################################################################
        ########################################################### Right Side
        # Graph Layout 
        graph_widget = QWidget()
        right_layout = QVBoxLayout()
        
        # Create figure and canvas
        self.fig = plt.figure()  # Changed from self.figure to self.fig to match config.py
        self.plot_canvas = FigureCanvas(self.fig)
        self.axis = self.fig.add_subplot(111, projection="3d")  # Changed to match config.py
        self.toolbar = NavigationToolbar(self.plot_canvas, self)
        
        # Add plot widgets to right layout
        right_layout.addWidget(self.toolbar)
        right_layout.addWidget(self.plot_canvas)
        graph_widget.setLayout(right_layout)
        
        # Apply canvas configuration
        # canvas_config(self) 
        # self.plot_canvas.draw()

        #####################
        # Layout for panels # 
        #####################
        # Add widgets to main layout
        main_layout.addWidget(left_container)
        main_layout.addWidget(graph_widget, stretch=2)
        
        
        
        ########################################
        # Set the main layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)



################################################################
############################################## Control Functions
    def draw_envelope(self):
        try:
            env_len = float(self.E_len.text())
            env_per = float(self.E_per.text())
            
            # TODO: Add your plotting logic here
            print(f"Drawing envelope with Length: {env_len} and percent: {env_per}")
            
            # Create example 3D plot
            x = np.linspace(0, env_len, 100)
            y = np.sin(x * env_per)
            z = np.zeros_like(x)
            
            
            self.axis.plot(x, y, z)
            
            self.plot_canvas.draw()
            
            
            
        except ValueError:
            QMessageBox.warning(self, "Invalid Input")








if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())