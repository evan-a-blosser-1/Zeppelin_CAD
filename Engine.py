import numpy as np  
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sympy as sp 


L  = 50
R  = 0.5
D1 = 11
D2 = L - D1*1.5
######
Pm  = np.array([0,0,0])
#
p1x = Pm[0] 
p1y = Pm[1]
p1z = Pm[2]
#
p2x = Pm[0] + D1
p2y = Pm[1]
p2z = Pm[2] + R
#
p3x = Pm[0] + D2 
p3y = Pm[1]
p3z = Pm[2] + R
#
p4x = Pm[0] + L
p4y = Pm[1]
p4z = Pm[2] 
###########
p_i = np.array([[p1x,p1y,p1z],[p2x,p2y,p2z],[p3x,p3y,p3z],[p4x,p4y,p4z]])

######
Mi = 0 
Ni = 0
Oi = 0
######
Pnt_0 = np.array([[p1x,p2x,p3x,p4x],[p1y,p2y,p3y,p4y],[p1z,p2z,p3z,p4z],[1, 1, 1, 1]])
T_t   = np.array([[1, 0, 0, Mi],[0,1,0,Ni],[0,0,1,Oi],[0,0,0,1]])

####
# Debugg take p2
#
# multiply the 4x4 with 1 control point and quantum vector
#
# Check that this point is correct with translation
# 
# Print before and after translation, to make sure 
# that the translation is correct
#
#
print('-----------------------')
print(p_i)
p_i = np.matmul(T_t,Pnt_0)
print(p_i[0,0])
print('-----------------------')
pi1x = p_i[0,0]
pi1y = p_i[1,0]
pi1z = p_i[2,0]
print(pi1x,pi1y,pi1z)
#
pi2x = p_i[0,1]
pi2y = p_i[1,1]
pi2z = p_i[2,1]
print(pi2x,pi2y,pi2z)
#
#
pi3x = p_i[0,2]
pi3y = p_i[1,2]
pi3z = p_i[2,2]
print(pi3x,pi3y,pi3z)
#
#
pi4x = p_i[0,3]
pi4y = p_i[1,3]
pi4z = p_i[2,3]
print(pi4x,pi4y,pi4z)



######



##############
u = sp.symbols('u')
U = np.array([[u**3, u**2, u, 1]])
M = np.array([[-1 ,3, -3, 1],[3, -6, 3, 0],[-3, 3, 0, 0], [1, 0 ,0 ,0 ]])
# M = np.array([[-9/2 ,27/2, -27/2, 9/2],[9, -45/2, 18, -9/2],[-11/2, 9, -9/2, 1], [1, 0 ,0 ,0 ]])
print(M)
print(p_i)
print(M@p_i)
basis = np.matmul(U,M)
P = np.matmul(basis,p_i)
##################
N = 25
u_val = np.linspace(0, 1, N)
w_val = np.linspace(0, 2*np.pi, N)   
##############
U, W = np.meshgrid(u_val, w_val)
####################### 
#############
X_eq = sp.lambdify(u, P[0,0])
Z_eq = sp.lambdify(u, P[0,2])
print(P)
#############
X_val = X_eq(U)
# Curve is drawn on the XZ-plane
Y_val = np.zeros_like(X_val)  
Z_val = Z_eq(U)
print(X_val.shape)
print(Y_val.shape)
print(Z_val.shape)
#############
Px = X_val
Py = Z_val*np.cos(W)
Pz = Z_val*np.sin(W)
print(Px.shape)
print(Py.shape)
print(Pz.shape)
##################



##################
vertices = np.stack((Px.flatten(), Py.flatten(), Pz.flatten()), axis=-1)
triangles = matplotlib.tri.Triangulation(vertices[:,0], vertices[:,1])
mesh = Poly3DCollection(vertices[triangles.triangles])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.add_collection3d(mesh)
ax.plot_wireframe(Px, Py, Pz, color='black', alpha=0.5)
# ax.plot(X_val, Y_val, Z_val, label='B-spline curve')
# ax.plot_surface(Px, Py, Pz, alpha=0.5, color='blue')

ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_title('3D Surface Plot')
plt.show()