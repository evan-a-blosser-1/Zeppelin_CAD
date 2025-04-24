import numpy as np  
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sympy as sp 




ex_r = np.array([5, 0, 0])

R = 3

p0x = 0.0
p0y = 0.0
p0z = 0.0

p1x = p0x 
p1y = p0y + R
p1z = p0z + R 

p2x = p0x 
p2y = p1y + R 
p2z = p0z

p3x = p0x 
p3y = p1y
p3z = p0z - R 


u = sp.symbols('u')
w = sp.symbols('w')

U = np.array([ u**2, u, 1])
M = np.array([[1, -2, 1], [-2, 2, 0], [1, 1, 0]])
p1 = np.array([[p0x, p0y, p0z],[p1x, p1y, p1z],[p2x, p2y, p2z]])
p2 = np.array([[p1x, p1y, p1z],[p2x, p2y, p2z],[p3x, p3y, p3z]])
p3 = np.array([[p2x, p2y, p2z],[p3x, p3y, p3z],[p0x, p0y, p0z]])
p4 = np.array([[p3x, p3y, p3z],[p0x, p0y, p0z],[p1x, p1y, p1z]])
P_u1 = U @ M @ p1 + ex_r*w
P_u2 = U @ M @ p2 + ex_r*w
P_u3 = U @ M @ p3 + ex_r*w
P_u4 = U @ M @ p4 + ex_r*w

print(P_u1.shape)
print(P_u2.shape)
print(P_u1[0])
print(P_u1[1])
print(P_u1[2])
print(P_u2)
print(P_u3)
print(P_u4)
# ################
N = 25
U = np.linspace(0, 1, N)
W = np.linspace(0, 1, N)

# w_val = np.linspace(0, 1, N)   
# ##############
# U, W = np.meshgrid(u_val, w_val)
# ####################### 
# from icecream import ic 
# ic(P)
# print(P.shape)
# print(P[0,0])
##############
X_eq1 = sp.lambdify(w, P_u1[0])
Y_eq1 = sp.lambdify(u, P_u1[1])
Z_eq1 = sp.lambdify(u, P_u1[2])

X_eq2 = sp.lambdify(w, P_u2[0])
Y_eq2 = sp.lambdify(u, P_u2[1])
Z_eq2 = sp.lambdify(u, P_u2[2])

X_eq3 = sp.lambdify(w, P_u3[0])
Y_eq3 = sp.lambdify(u, P_u3[1])
Z_eq3 = sp.lambdify(u, P_u3[2])

X_eq4 = sp.lambdify(w, P_u4[0])
Y_eq4 = sp.lambdify(u, P_u4[1])
Z_eq4 = sp.lambdify(u, P_u4[2])

#############
X_val1 = X_eq1(W)
Y_val1 = Y_eq1(U)
Z_val1 = Z_eq1(U)
#
X_val2 = X_eq2(W)
Y_val2 = Y_eq2(U)
Z_val2 = Z_eq2(U)
#
X_val3 = X_eq3(W)
Y_val3 = Y_eq3(U)
Z_val3 = Z_eq3(U) 
#
X_val4 = X_eq4(W)
Y_val4 = Y_eq4(U)
Z_val4 = Z_eq4(U)
#################

plt.plot(Y_val1, Z_val1, label='Curve 1', color='blue')
plt.plot(Y_val2, Z_val2, label='Curve 2', color='red')
plt.plot(Y_val3, Z_val3, label='Curve 3', color='green')
plt.plot(Y_val4, Z_val4, label='Curve 4', color='orange')


plt.show()


# Create combined mesh arrays
Px = np.vstack((X_val1, X_val2))
Py = np.vstack((Y_val1, Y_val2))
Pz = np.vstack((Z_val1, Z_val2))
vertices = np.stack((Px.flatten(), Py.flatten(), Pz.flatten()), axis=-1)
triangles = matplotlib.tri.Triangulation(vertices[:,0], vertices[:,1])
mesh = Poly3DCollection(vertices[triangles.triangles])

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.add_collection3d(mesh)
# Triangulated surface
ax.plot_trisurf(Px.flatten(), Py.flatten(), Pz.flatten(), alpha=0.5)

# Contour plot
ax.contour3D(Px, Py, Pz)

# Surface with color mapping
surf = ax.plot_surface(Px, Py, Pz, cmap='viridis', 
                      linewidth=0, antialiased=False)
fig.colorbar(surf)
# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()



# def draw_engine(main_window,shape,):
    
#     if shape == "Cylinder":
#         # TODO : Add cylinder drawing logic    
#         a = 1
#     elif shape == "Rectangle":
#         # TODO : Add rectangle drawing logic
        