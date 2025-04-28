import matplotlib.pyplot as plt
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
    

# def merge_meshes(main_window):
#     # List to store valid vertices and triangles
#     mesh_data = []
    
#     # Check and add each component's vertices and triangles if they exist
#     if main_window.env_tri is not None:
#         mesh_data.append((main_window.env_verts, main_window.env_tri))
#     if main_window.gond_tri is not None:
#         mesh_data.append((main_window.gond_verts, main_window.gond_tri))
#     if main_window.eng_tri is not None:
#         mesh_data.append((main_window.eng_verts, main_window.eng_tri))
#     if main_window.fin_tri is not None:
#         mesh_data.append((main_window.fin_verts, main_window.fin_tri))
        
#     if not mesh_data:
#         main_window.logback.append("No meshes to merge!")
#         return


#     # Combine meshes
#     all_vertices = []
#     all_triangles = []
#     vertex_offset = 0
    
#     for vertices, triangles in mesh_data:
#         all_vertices.append(vertices)
#         # Get triangle indices and adjust with offset
#         tri_indices = triangles.triangles  # Access the triangle indices
#         current_triangles = tri_indices + vertex_offset
#         all_triangles.append(triangles.triangles)
#         vertex_offset += len(vertices)
    
#     # Combine all vertices and triangles
#     combined_vertices = np.vstack(all_vertices)
#     combined_triangles = np.vstack(all_triangles)
    
#     # Create final mesh
#     main_window.combined_mesh = Poly3DCollection(combined_vertices[combined_triangles])
    
#     # Clear plot and add combined mesh
#     clear_plot(main_window)
#     main_window.plot_canvas.axis.add_collection3d(main_window.combined_mesh)
#     main_window.plot_canvas.draw()
#     main_window.logback.append("Meshes merged successfully!")

def save_as_stl(self):
    try:
        # Combine all vertices and faces from wireframes
        combined_vertices = []
        combined_faces = []
        vertex_offset = 0
        
        # Add envelope mesh if it exists
        if hasattr(self, 'env_verts') and self.env_verts is not None:
            combined_vertices.extend(self.env_verts)
            if hasattr(self, 'env_tri') and self.env_tri is not None:
                # Convert triangulation to array and add offset
                tri_array = np.array(self.env_tri.triangles)
                combined_faces.extend(tri_array + vertex_offset)
            vertex_offset += len(self.env_verts)
        
        # Add gondola mesh if it exists
        if hasattr(self, 'gond_verts') and self.gond_verts is not None:
            combined_vertices.extend(self.gond_verts)
            if hasattr(self, 'gond_tri') and self.gond_tri is not None:
                tri_array = np.array(self.gond_tri.triangles)
                combined_faces.extend(tri_array + vertex_offset)
            vertex_offset += len(self.gond_verts)
            
        # Convert to numpy arrays
        vertices = np.array(combined_vertices)
        faces = np.array(combined_faces)
        
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