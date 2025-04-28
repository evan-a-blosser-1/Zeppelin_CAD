import matplotlib.pyplot as plt
import matplotlib
from PySide6.QtWidgets import QMessageBox  
from PySide6 import QtWidgets
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import stl

def clear_plot(main_window):
    main_window.plot_canvas.axis.clear()
    main_window.plot_canvas.axis.set_xlabel('X (m)')
    main_window.plot_canvas.axis.set_ylabel('Y (m)')
    main_window.plot_canvas.axis.set_zlabel('Z (m)')
    main_window.plot_canvas.draw()
    

def merge_wireframes(self):
    """Merge all component wireframes stored as dictionaries"""
    if self.env_wf is None:
        QMessageBox.warning(self, "Merge Error", "Please draw the envelope first")
        return

    try:
        # Initialize arrays to store combined coordinates
        Px_combined = self.env_wf['Px']
        Py_combined = self.env_wf['Py']
        Pz_combined = self.env_wf['Pz']
        
        # Add other wireframes if they exist
        if self.gond_wf is not None:
            Px_combined = np.concatenate([Px_combined, self.gond_wf['Px']])
            Py_combined = np.concatenate([Py_combined, self.gond_wf['Py']])
            Pz_combined = np.concatenate([Pz_combined, self.gond_wf['Pz']])
            
        if self.eng_wf1 is not None:
            Px_combined = np.concatenate([Px_combined, self.eng_wf1['Px']])
            Py_combined = np.concatenate([Py_combined, self.eng_wf1['Py']])
            Pz_combined = np.concatenate([Pz_combined, self.eng_wf1['Pz']])
            
        if self.eng_wf2 is not None:
            Px_combined = np.concatenate([Px_combined, self.eng_wf2['Px']])
            Py_combined = np.concatenate([Py_combined, self.eng_wf2['Py']])
            Pz_combined = np.concatenate([Pz_combined, self.eng_wf2['Pz']])
            
        if self.fin_wf is not None:
            Px_combined = np.concatenate([Px_combined, self.fin_wf['Px']])
            Py_combined = np.concatenate([Py_combined, self.fin_wf['Py']])
            Pz_combined = np.concatenate([Pz_combined, self.fin_wf['Pz']])
            
            
        # Get envelope parameters
        L = float(self.E_len.text())
        R = float(self.E_rad.text())
        D1 = float(self.E_per.text())
        
        # Calculate radial distance for each point
        r = np.sqrt(Py_combined**2 + Pz_combined**2)
        x = Px_combined
        
        # Create masks for each section
        nose_mask = (x <= D1) & (r < R * (x/D1))
        tail_mask = (x >= (L-D1)) & (r < R * ((L-x)/D1))
        body_mask = (x > D1) & (x < (L-D1)) & (r < R)
        
        # Combine masks - True means point is inside
        interior_mask = nose_mask | tail_mask | body_mask
        
        # Invert mask to keep exterior points
        exterior_mask = ~interior_mask
        
        # Apply mask to keep only exterior points
        Px_filtered = Px_combined[exterior_mask]
        Py_filtered = Py_combined[exterior_mask]
        Pz_filtered = Pz_combined[exterior_mask]

        # Store filtered wireframe as dictionary
        self.combined_wf = {
            'Px': Px_filtered,
            'Py': Py_filtered,
            'Pz': Pz_filtered,
            'color': 'blue',
            'alpha': 0.5
        }

        # Update plot
        self.plot_canvas.axis.clear()
        self.plot_canvas.axis.plot_wireframe(Px_combined, Py_combined, Pz_combined, 
                               color=self.combined_wf['color'],
                               alpha=self.combined_wf['alpha'])
        self.plot_canvas.axis.set_xlabel('X')
        self.plot_canvas.axis.set_ylabel('Y')
        self.plot_canvas.axis.set_zlabel('Z')
        self.plot_canvas.draw()
        
        self.logback.append("Wireframes merged successfully")
        
    except Exception as e:
        self.logback.append(f"Error merging wireframes: {str(e)}")
        QMessageBox.critical(self, "Merge Error", str(e))
        
        

def save_as_stl(self):
    try:
        # Combine all wireframe meshes
        if not hasattr(self, 'wfrm'):
            QMessageBox.warning(self, "STL Export Error", "No wireframe data available")
            return
            
        # Get points from wireframe
        Px = self.wfrm['Px'].flatten()
        Py = self.wfrm['Py'].flatten()
        Pz = self.wfrm['Pz'].flatten()
        
        # Combine into vertices array
        vertices = np.vstack((Px, Py, Pz)).T
        
        # Create triangulation from points
        tri = matplotlib.tri.Triangulation(vertices[:,0], vertices[:,1])
        faces = tri.triangles
        
        # Create mesh data
        mesh_data = stl.mesh.Mesh(np.zeros(len(faces), dtype=stl.mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                mesh_data.vectors[i][j] = vertices[f[j]]
                
        # Save to file with default path
        default_path = "C:/Users/"
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            'Save STL File',
            default_path,
            'STL Files (*.stl)',
            options=QtWidgets.QFileDialog.DontUseNativeDialog
        )[0]
        
        if filename:
            if not filename.endswith('.stl'):
                filename += '.stl'
            mesh_data.save(filename)
            self.logback.append(f"Saved mesh to {filename}")
            
    except Exception as e:
        QMessageBox.critical(self, "STL Export Error", str(e))
        self.logback.append(f"STL export error: {e}")