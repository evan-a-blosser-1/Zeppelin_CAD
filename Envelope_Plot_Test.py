import numpy as np
import matplotlib.pyplot as plt 
import sympy as sp


# Length envelope
L  = 15 
R  = 5
D1 = 3
l  = 5
D2 = l + D1 
######
p1x = 0
p1y = 0
p1z = 0
#
p2x = D1
p2y = 0
p2z = R
#
p3x = D2 
p3y = 0
p3z = R
#
p4x = L
p4y = 0
p4z = 0
#########
p_i = np.array([[p1x,p1y,p1z],[p2x,p2y,p2z],[p3x,p3y,p3z],[p4x,p4y,p4z]])
##############
u = sp.symbols('u')
U = np.array([[u**3, u**2, u, 1]])
M = np.array([[-9/2 ,27/2, -27/2, 9/2],[9, -45/2, 18, -9/2],[-11/2, 9, -9/2, 1], [1, 0 ,0 ,0 ]])
# M = np.array([[-1 , 3, -3, 1],[3, -6, 3, 0],[-3, 3, 0, 0], [1, 0, 0,0 ]])
print(M)
print(p_i)
print(M@p_i)
P = U@M@p_i
######
N = 25
u_val = np.linspace(0, 1, N)
w_val = np.linspace(0, 2*np.pi, N)   
##############
U, W = np.meshgrid(u_val, w_val)
####################### 
from icecream import ic 
ic(P)
print(P.shape)
print(P[0,0])
#############
X_eq = sp.lambdify(u, P[0,0])
Z_eq = sp.lambdify(u, P[0,2])
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
Py = Y_val*np.cos(W)
Pz = Z_val*np.sin(W)
##################
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.plot(X_val, Y_val, Z_val, label='B-spline curve')
ax.plot_surface(Px, Py, Pz, alpha=0.5, color='blue')
ax.plot_wireframe(Px, Py, Pz, color='blue', alpha=0.5)

ax.scatter(p_i[:,0], p_i[:,1], p_i[:,2], color='red', label='Control points')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_title('B-spline Curve')
ax.legend()
plt.show()