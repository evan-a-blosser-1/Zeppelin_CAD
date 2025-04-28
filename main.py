import sys
import numpy as np   
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                               QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget,
                               QMenuBar, QComboBox, QScrollArea, QListView, QFileDialog, 
                               QFileSystemModel,QGridLayout, QSlider, QMessageBox)
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtCore import Qt, QRectF
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

sys.dont_write_bytecode = True
from config import clear_plot
from Envelope import draw_envelope
from Gondola import draw_gondola
from Fins import build_fin, Ro_x


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.axis = plt.subplots(subplot_kw={"projection": "3d"})
        super().__init__(self.fig)
        self.setParent(parent)
        


class MainWindow(QMainWindow):
    def __init__(self):  # Fixed method name from __int__ to __init__
        super().__init__()
        self.setWindowTitle("Zeppelin CAD")
        self.setWindowState(Qt.WindowMaximized)
        ######################################
        # Globals
        self.low_pnt = None
        self.env_tri = None
        self.env_verts = None
        self.gond_tri = None
        self.gond_verts = None
        self.eng_tri = None
        self.eng_verts = None
        self.fin_tri = None
        self.fin_verts = None
        self.combined_tri = None
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
        left_panel.addTab(env_tab,  "Envelope")
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
        # Global Variabels: used for gondola location
        #                   and completing full mesh
        #
        env_grid = QGridLayout()
        ###########################
        # User Inputs
        self.E_len_label = QLabel("Length: (m)")
        self.E_len = QLineEdit("175")
        self.E_rad_label = QLabel("Radius: (m)")
        self.E_rad = QLineEdit("50")
        self.E_per_label = QLabel("Nose-Length: (m)")
        self.E_per = QLineEdit("45")
        
        # Add widgets to grid layout
        env_grid.addWidget(self.E_len_label, 0, 0)
        env_grid.addWidget(self.E_len, 0, 1)
        env_grid.addWidget(self.E_rad_label, 1, 0)
        env_grid.addWidget(self.E_rad, 1, 1)
        env_grid.addWidget(self.E_per_label, 2, 0)
        env_grid.addWidget(self.E_per, 2, 1)
        
        # Create and add draw button
        self.draw_env_button = QPushButton("Draw Envelope")
        self.draw_env_button.clicked.connect(self.draw_envelope)
        
        # Add grid layout to main envelope layout
        env_layout.addLayout(env_grid)
        env_layout.addWidget(self.draw_env_button)
        env_layout.addStretch()
        
        
        
        
        # Gondola Tab Layout
        gond_layout = QVBoxLayout(gond_tab)
        gond_grid = QGridLayout()
        self.gondola_len = QLineEdit("50"); self.gondola_wid = QLineEdit("40"); self.gondola_height = QLineEdit("30")
        gond_grid.addWidget(QLabel("Length (m)"), 0,0); gond_grid.addWidget(self.gondola_len, 0,1)
        gond_grid.addWidget(QLabel("Width (m)"),  1,0); gond_grid.addWidget(self.gondola_wid, 1,1)
        gond_grid.addWidget(QLabel("Height (m)"), 2,0); gond_grid.addWidget(self.gondola_height,2,1)

        # Sliders for nose/tail sharpness & plateau
        self.ns_slider = QSlider(Qt.Horizontal); self.ns_slider.setRange(1,10); self.ns_slider.setValue(2)
        self.ts_slider = QSlider(Qt.Horizontal); self.ts_slider.setRange(1,10); self.ts_slider.setValue(2)
        self.ps_slider = QSlider(Qt.Horizontal); self.ps_slider.setRange(0,100); self.ps_slider.setValue(100)
        self.ns_label   = QLabel("Nose Sharpness: 2.0")
        self.ts_label   = QLabel("Tail Sharpness: 2.0")
        self.ps_label   = QLabel("Plateau Scale: 1.00")
        # Connect
        self.ns_slider.valueChanged.connect(lambda v: self.ns_label.setText(f"Nose Sharpness: {v/1.0:.1f}"))
        self.ts_slider.valueChanged.connect(lambda v: self.ts_label.setText(f"Tail Sharpness: {v/1.0:.1f}"))
        self.ps_slider.valueChanged.connect(lambda v: self.ps_label.setText(f"Plateau Scale: {v/100.0:.2f}"))

        self.draw_gond_button = QPushButton("Draw Gondola")
        self.draw_gond_button.clicked.connect(self.draw_gondola)

        gond_layout.addLayout(gond_grid)
        gond_layout.addWidget(self.ns_label); gond_layout.addWidget(self.ns_slider)
        gond_layout.addWidget(self.ts_label); gond_layout.addWidget(self.ts_slider)
        gond_layout.addWidget(self.ps_label); gond_layout.addWidget(self.ps_slider)
        gond_layout.addWidget(self.draw_gond_button)
        gond_layout.addStretch()
        
        
        ####################################
        # Engine
        eng_layout.addWidget(QLabel("Grid Size:"))
        eng_layout.addWidget(QLineEdit())
        eng_layout.addStretch()
        
        
        #####################################
        # Fins
        fin_grid = QGridLayout()
        self.fin_label = QLabel("Fin Base: (m)")
        self.fin_len = QLineEdit("3")
        self.fin_wid_label = QLabel("Fin Tip: (m)")
        self.fin_wid = QLineEdit("1")
        self.fin_height_label = QLabel("Fin Height: (m)")
        self.fin_height = QLineEdit("1")
        self.fin_dis_label = QLabel("Distance From Nose: (m)")
        self.fin_dis = QLineEdit("50")
        # 
        self.fin_num_label = QLabel("Number of Fins:")
        self.fin_num = QLineEdit("4")
        
        fin_grid.addWidget(self.fin_label, 0, 0)
        fin_grid.addWidget(self.fin_len, 0, 1)
        fin_grid.addWidget(self.fin_wid_label, 1, 0)
        fin_grid.addWidget(self.fin_wid, 1, 1)
        fin_grid.addWidget(self.fin_height_label, 2, 0)
        fin_grid.addWidget(self.fin_height, 2, 1)
        fin_grid.addWidget(self.fin_dis_label, 3, 0)
        fin_grid.addWidget(self.fin_dis, 3, 1)
        fin_grid.addWidget(self.fin_num_label, 4, 0)
        fin_grid.addWidget(self.fin_num, 4, 1)
        ########
        self.draw_fin_button = QPushButton("Draw Fins")
        self.draw_fin_button.clicked.connect(self.draw_fin)
        
        
        fin_layout.addLayout(fin_grid)
        fin_layout.addWidget(self.draw_fin_button)
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
        #################################################
        # Merge button
        # self.merge_button = QPushButton("Merge All Meshes")
        # self.merge_button.clicked.connect(lambda: merge_meshes(self))
        # bottom_panel_layout.addWidget(self.merge_button)
        
        
        # Add log output window
        self.logback = QTextEdit()
        self.logback.setReadOnly(True)  
        self.logback.setFixedHeight(500)  
        self.logback.setStyleSheet("background-color: white; font-family: Consolas;")
        bottom_panel_layout.addWidget(self.logback)
        
        # Add tab panel and bottom panel to left container
        left_container_layout.addWidget(left_panel)
        left_container_layout.addWidget(bottom_panel)
        
        
        
        
        #######################################################################
        ########################################################### Right Side
        # Graph Layout 
        graph_widget = QWidget()
        right_layout = QVBoxLayout()
        

        self.plot_canvas = PlotCanvas(self)
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
            L = float(self.E_len.text())
            R = float(self.E_rad.text())
            D1 = float(self.E_per.text())
            # TODO: idiot proof
            if L < 50:
                env_err_message = "Length too short"
                raise ValueError("Length too long")
            if R > 50:
                raise ValueError("Radius too long")
            if D1 > L:
                raise ValueError("Nose length too long")
            
            
            #############################################
            self.logback.append(f"Drawing envelope with:")
            
            # Create example 3D plot
            # x = np.linspace(0, env_len, 100)
            # y = np.sin(x * env_per)
            # z = np.zeros_like(x)
            # self.axis.plot(x, y, z)
            
            self.low_pnt, self.env_tri, self.env_verts = draw_envelope(self,L,R,D1)
            
            
            self.plot_canvas.draw()
            
            
            
        except ValueError:
            self.logback.append(f"Error: {env_err_message}")
            QMessageBox.warning(self, "Invalid Input")



    def draw_gondola(self):
        if self.low_pnt is None:
            QMessageBox.warning(self, "Gondola Error", "Please draw the envelope first")
            return

        L  = float(self.gondola_len.text())
        W  = float(self.gondola_wid.text())
        H  = float(self.gondola_height.text())
        ns = self.ns_slider.value()            # 1–10
        ts = self.ts_slider.value()            # 1–10
        ps = self.ps_slider.value() / 100.0    # 0.00–1.00

        self.logback.append(f"Gondola → L={L}, W={W}, H={H}, nose_sharp={ns}, tail_sharp={ts}, plateau={ps}")

        try:
            verts, _ = draw_gondola(self,
                                    length=L,
                                    width=W,
                                    height=H,
                                    nose_sharp=ns,
                                    tail_sharp=ts,
                                    plateau_scale=ps)
            self.gond_verts = verts
        except Exception as e:
            QMessageBox.critical(self, "Gondola Error", str(e))
            self.logback.append(f"Gondola error: {e}")






    def draw_fin(self):
        if self.low_pnt.any() == None:
            fin_err_message = "Please Build the Main Envelope First "
            self.logback.append(f"Error: {fin_err_message}")
            raise ValueError("Please Build the Main Envelope First ")

        try:
            L = float(self.fin_len.text()) ## fin base
            W = float(self.fin_wid.text())  ## fin tip
            H = float(self.fin_height.text()) ## fin height
            D = float(self.fin_dis.text())   ## distance from nose
            N = int(self.fin_num.text())     ## number of fins
            
            angle_start = 90
            angle_advance = 360 / N

            fin = np.zeros((N, 12))
            for i in range(N):
                angle = angle_start + angle_advance*i
                if angle > 360:
                    angle = angle - 360
                fin = build_fin(self, H, L, W, D, angle)
            
            self.logback.append(f"Drawing fins with:")

        except ValueError:
                    self.logback.append(f"Error: {fin_err_message}")
                    QMessageBox.warning(self, "Invalid Input")



###################################### 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())