import numpy as np
import matplotlib.pyplot as plt 
import matplotlib
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


N = 20 
U = np.linspace(0, -1.5, N) 
W = np.linspace(0, np.pi, N) 
u,w = np.meshgrid(U, W)

Px = np.cos(u)*np.sin(w) 
Py = np.cos(u)*np.cos(w)
Pz = np.sin(u)


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
vertices = np.stack((Px.flatten(), Py.flatten(), Pz.flatten()), axis=-1)
triangles = matplotlib.tri.Triangulation(vertices[:,0], vertices[:,1])
mesh = Poly3DCollection(vertices[triangles.triangles])

##################
# ax.plot(X_val, Y_val, Z_val, label='B-spline curve')
# ax.plot_surface(Px, Py, Pz, alpha=0.5, color='blue')
ax.add_collection3d(mesh)
ax.plot_wireframe(Px, Py, Pz, color='black', alpha=0.5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()