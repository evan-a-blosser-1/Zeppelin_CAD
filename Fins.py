import numpy as np
import matplotlib.pyplot as plt 
import matplotlib
import sympy as sp
u = sp.symbols('u')
w = sp.symbols('w')
### basic Fin Calculations
R = int(input("Enter the radius of the Main Envelope:")) # max radius of the envelope (SET FORM OTHER PARAMETERS)

lines = 25


h = int(input("Enter the height of the fin (from centerline) > envelope radius or 0:"))
# a = input("Enter the angle of the fin (degrees): ")
b = int(input("Enter the base of the fin > 0:"))
t = int(input("Enter the length of the fin tip > 0 or base: "))


def Ro_x(theta, Px, Py, Pz): # rotation of a point around the x-axis
    Ro_x = np.array([[1,0,0],[0, np.cos(theta), -np.sin(theta)],[0, np.sin(theta), np.cos(theta)]])
    P_rotated = np.matmul(Ro_x, np.array([Px, Py, Pz]))
    return P_rotated

# sanity check the inputs
if h < 0:
    print("Height cannot be negative")
    h = input("Enter the height of the fin (from centerline) > envelope radius or 0:")
elif h <= R:
    print ("Height is equal to envelope radius.")
    height_checkinput = input("Proceed? (y/n): ")
    if height_checkinput != 'n':
        h = R   
        print("Height set to inital entry.")
    else:
        h = input("Enter the height of the fin (from centerline) > envelope radius or 0:")
else:
    print ("Fin height is good!")

##### TO DO: check if the fin tip is greater than the fin base

ax = plt.axes(projection='3d')
### Create points for the surface path of the initial fin construction
# four points for the corners of the fin
P0 = np.array([0, 0, 0]) # origin
P1 = np.array([b, 0, 0]) # base of the fin
P2 = np.array([b, h, 0]) # height of the fin
P3 = np.array([b-t, h, 0]) # tip of the fin

### Create points for the airfoil path of the fin
## NACA 0012 airfoil, with max camber of 12% at 30% chord length
#Leading edge, max camber, trailing edge
u_value = np.linspace(0, 1, 100) 
P4 = P0
P5 = np.array([.3 * (b), 0, 0.12 * (b)]) # max camber at 30% chord length
P6 = P1

P_airfoil = np.array([P4, P5, P6]) # airfoil points

U_matrix = np.array([[u**2, u, 1]])
N_s = np.array([[2,-4,2],[-3,4,-1],[1,0,0]])
B_airfoil_s = np.matmul(U_matrix, N_s) # B-spline matrix for the airfoil points
P_airfoil_s = np.matmul(B_airfoil_s, P_airfoil)

print('B_airfoil_s: ',B_airfoil_s,'\n','P_airfoil_s: ',P_airfoil_s)

foilbase_x = sp.lambdify(u, P_airfoil_s[0,0], modules='numpy')
foilbase_x_values = foilbase_x(u_value) # x-coordinates of the airfoil path
#print('foilbase_x: ',foilbase_x_values)
foilbase_y_values = 0
foilbase_z = sp.lambdify(u, P_airfoil_s[0,2], modules='numpy') 
foilbase_z_values = foilbase_z(u_value) # z-coordinates of the airfoil path
#print('foilbase_z: ',foilbase_z_values)


## Create points for tip of the fin by scaling the base airfoil points
foil_scale = t/b # scale factor for the airfoil points
print('tip/root ratio:',foil_scale)
P_airfoil_scale = np.array([[P4[0],P5[0],P6[0],1], [P4[1],P5[1],P6[1],1], [P4[2],P5[2],P6[2],1], [1,1,1,1]]) # scale the airfoil points
Scale_matrix = np.array([[foil_scale,0,0,b-t],[0,foil_scale,0,h],[0,0,foil_scale,0],[0,0,0,foil_scale]])

# print('P_airfoil_scale: \n',P_airfoil_scale)
print('Scale_matrix: \n',Scale_matrix)

P_airfoil_tip = np.matmul(Scale_matrix,P_airfoil_scale)  # scale the airfoil points
#print('P_airfoil_tip:\n', P_airfoil_tip)

## Create points for the top airfoil by using the scaled and translated airfoil points
P7 = np.array([P_airfoil_tip[0,0],P_airfoil_tip[1,0],P_airfoil_tip[2,0]]) # leading edge of the airfoil
P8 = np.array([P_airfoil_tip[0,1],P_airfoil_tip[1,1],P_airfoil_tip[2,1]]) # max camber of the airfoil
P9 = np.array([P_airfoil_tip[0,2],P_airfoil_tip[1,2],P_airfoil_tip[2,2]]) # trailing edge of the airfoil

P_airfoil_tip = np.array([P7, P8, P9]) # top airfoil points

P_airfoil_tip_s = np.matmul(B_airfoil_s, P_airfoil_tip) # B-spline matrix for the top airfoil points

## fin tip airfoil converstion from P_u
foiltip_x = sp.lambdify(u, P_airfoil_tip_s[0,0], modules='numpy')
foiltip_x_values = foiltip_x(u_value) # x-coordinates of the airfoil path
#print('foilbase_x: ',foilbase_x_values)
foiltip_y_values = h
foiltip_z = sp.lambdify(u, P_airfoil_tip_s[0,2], modules='numpy') 
foiltip_z_values = foiltip_z(u_value) # z-coordinates of the airfoil path
#print('foilbase_z: ',foilbase_z_values)

#print('P_airfoil_tip_s: ',P_airfoil_tip_s)

#### Surface plot of the fin

S_uw_airfoil = (1-w)*P_airfoil_s + w*P_airfoil_tip_s # surface of the fin

#print('S_uw_airfoil: ',S_uw_airfoil)

S_surface_x = sp.lambdify((u,w), S_uw_airfoil[0,0], modules='numpy')
S_surface_y = sp.lambdify((u,w), S_uw_airfoil[0,1], modules='numpy')
S_surface_z = sp.lambdify((u,w), S_uw_airfoil[0,2], modules='numpy')
u_value = np.linspace(0, 1, lines) # u values for the airfoil path
w_value = np.linspace(0, 1, lines) # w values for the airfoil path

S_surface_values_x = np.zeros((len(u_value), len(w_value))) # initialize the surface values
S_surface_values_y = np.zeros((len(u_value), len(w_value))) # initialize the surface values
S_surface_values_z = np.zeros((len(u_value), len(w_value))) # initialize the surface values
ribs_x = np.zeros((len(u_value), len(w_value))) # initialize the ribs values
ribs_y = np.zeros((len(u_value), len(w_value))) # initialize the ribs values
ribs_z = np.zeros((len(u_value), len(w_value))) # initialize the ribs values

for i in range(len(u_value)):
    for j in range(len(w_value)):
        S_surface_values_x[i, j] = S_surface_x(u_value[i], w_value[j]) # surface of the fin
        S_surface_values_y[i, j] = S_surface_y(u_value[i], w_value[j]) # surface of the fin
        S_surface_values_z[i, j] = S_surface_z(u_value[i], w_value[j]) # surface of the fin

        ribs_x[i,j] = S_surface_x(u_value[j], w_value[i])
        ribs_y[i,j] = S_surface_y(u_value[j], w_value[i])
        ribs_z[i,j] = S_surface_z(u_value[j], w_value[i])


## create points for the underside of the fin surface

P10 = Ro_x(-np.pi, P5[0], P5[1], P5[2]) # Underside Root max camber point
P11_rotate = Ro_x(-np.pi, P8[0], 0, P8[2]) # Underside Tip max camber point

P11_final = np.array([P11_rotate[0], h, P11_rotate[2]]) # Underside Tip max camber point
print('P5: ',P5, '\nP10: ',P10)
print('P8: ',P8, '\nP11: ',P11_final)




### Create a 3D plot

plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Plot the edges of the fin by connecting the points
ax.plot([P0[0], P1[0]], [P0[1], P1[1]], [P0[2], P1[2]], color='blue', label='Base Edge')  # P0 to P1
ax.plot([P1[0], P2[0]], [P1[1], P2[1]], [P1[2], P2[2]], color='green', label='Height Edge')  # P1 to P2
ax.plot([P2[0], P3[0]], [P2[1], P3[1]], [P2[2], P3[2]], color='red', label='Tip Edge')  # P2 to P3
ax.plot([P3[0], P0[0]], [P3[1], P0[1]], [P3[2], P0[2]], color='purple', label='Diagonal Edge')  # P3 to P0
ax.plot([P4[0], P5[0]], [P4[1], P5[1]], [P4[2], P5[2]], color='orange', label='Airfoil Leading Edge')  # P4 to P5
ax.plot([P5[0], P6[0]], [P5[1], P6[1]], [P5[2], P6[2]], color='cyan', label='Airfoil Trailing Edge')  # P5 to P6
ax.plot([P7[0], P8[0]], [P7[1], P8[1]], [P7[2], P8[2]], color='yellow', label='Airfoil Top Leading Edge')  # P7 to P8
ax.plot([P0[0], P10[0]],[P0[1], P10[1]], [P0[1], P10[2]], color='magenta', label='Airfoil Top Trailing Edge')  # P0 to P10
ax.plot([P10[0], P1[0]],[P10[1], P1[1]], [P10[2], P1[2]], color='brown', label='Airfoil Bottom Trailing Edge')  # P10 to P1
ax.plot([P11_final[0], P3[0]],[P11_final[1], P3[1]], [P11_final[2], P3[2]], color='pink', label='Airfoil Bottom Leading Edge')  # P11 to P3
ax.plot([P11_final[0], P2[0]],[P11_final[1], P2[1]], [P11_final[2], P2[2]], color='grey', label='Airfoil Bottom Leading Edge')  # P11 to P8

plt.plot(foilbase_x_values, foilbase_y_values, foilbase_z_values, color='black', label='Airfoil Path')  # Airfoil path
plt.plot(foiltip_x_values, foiltip_y_values, foiltip_z_values, color='black', label='Airfoil Top Path')  # Airfoil path

for i in range(len(u_value)):
    plt.plot(S_surface_values_x[i,:], S_surface_values_y[i,:], S_surface_values_z[i,:], label='S(u,w)')
    plt.plot(ribs_x[i,:], ribs_y[i,:], ribs_z[i,:], label='Ribs') # ribs of the fin

# Add a legend for clarity
ax.legend(bbox_to_anchor = (1.1, 0.1))
ax.set_zbound(0, 15) # set the z-axis limit for proper scale in the visualization
ax.set_xbound(0,15) # set the x-axis limit for proper scale in the visualization
ax.set_ybound(0,15) # set the y-axis limit for proper scale in the visualization
plt.show()
### MERGE COMMENTS

### Create NACA 0012 airfoil points/spline