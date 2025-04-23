import matplotlib.pyplot as plt
import trimesh
from PySide6.QtWidgets import QMessageBox  
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


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