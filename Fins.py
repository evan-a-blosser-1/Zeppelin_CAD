import numpy as np
import matplotlib.pyplot as plt 
import matplotlib
import sympy as sp
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

### basic Fin Calculations
# R = int(input("Enter the radius of the Main Envelope:")) # max radius of the envelope (SET FORM OTHER PARAMETERS)

# h = int(input("Enter the height of the fin (from centerline) > envelope radius or 0:"))

# ##sanity check "h" inputs
# if h < 0:
#     print("Height cannot be negative")
#     h = int(input("Enter the height of the fin (from centerline) > envelope radius or 0:"))
# elif h <= R:
#     print ("Height is equal to envelope radius.")
#     height_checkinput = input("Proceed? (y/n): ")
#     if height_checkinput != 'n':
#         h = R   
#         print("Height set to inital entry.")
#     else:
#         h = int(input("Enter the height of the fin (from centerline) > envelope radius or 0:"))
# else:
#     print ("Fin height is good!")

# ##rest of parameters for the fin
# b = int(input("Enter the base of the fin > 0:"))
# t = int(input("Enter the length of the fin tip > 0 or base: "))
# offset = int(input("Enter the distance from the nose of the zeppelin (UNITS):"))
# theta_deg = int(input("Enter the angle of the fin (degrees): "))

def Ro_x(theta, Px, Py, Pz): # rotation of a point around the x-axis
    Ro_x = np.array([[1,0,0],[0, np.cos(theta), -np.sin(theta)],[0, np.sin(theta), np.cos(theta)]])
    P_rotated = np.matmul(Ro_x, np.array([Px, Py, Pz]))
    return P_rotated
### Create NACA 0012 airfoil points/spline

def build_fin(main_window, h, b, t, offset, theta_deg): # args are height, base, tip, and offset
    lines = 10 # number of lines for the surface plot
    u = sp.symbols('u')
    w = sp.symbols('w')
    # Create points for the surface path of the initial fin construction
    # four points for the corners of the fin
    P0 = np.array([0, 0, 0]) # origin
    P1 = np.array([b , 0, 0]) # base of the fin
    P2 = np.array([b , h, 0]) # height of the fin
    P3 = np.array([b-t , h, 0]) # tip of the fin

    ### Create points for the airfoil path of the fin
    ## NACA 0012 airfoil, with max camber of 12% at 30% chord length
    #Leading edge, max camber, trailing edge
    u_value = np.linspace(0, 1, 100) 
    P4 = P0 
    P5 = np.array([.3 * (b), 0, 0.12 * (b)]) # max camber at 30% chord length
    P6 = P1 

    P_airfoil = np.array([P4, P5, P6]) # airfoil points
    #move the airfoil points to the correct position down the envelope
    P4_offset = np.array([P4[0] + offset, P4[1], P4[2]]) # leading edge of the airfoil with offset
    P5_offset = np.array([P5[0] + offset, P5[1], P5[2]]) # max camber of the airfoil with offset
    P6_offset = np.array([P6[0] + offset, P6[1], P6[2]]) # trailing edge of the airfoil with offset
    #collect the points for the parametric equation calculation
    P_airfoil_offset = np.array([P4_offset, P5_offset, P6_offset]) # airfoil points with offset

    ## ROTATE THE POINTS!
    P4_rotate = Ro_x(np.deg2rad(theta_deg), P4_offset[0], P4_offset[1], P4_offset[2])
    P5_rotate = Ro_x(np.deg2rad(theta_deg), P5_offset[0], P5_offset[1], P5_offset[2])
    P6_rotate = Ro_x(np.deg2rad(theta_deg), P6_offset[0], P6_offset[1], P6_offset[2])

    P_airfoil_rotate_offset = np.array([P4_rotate, P5_rotate, P6_rotate]) # airfoil points with offset and rotation

    U_matrix = np.array([[u**2, u, 1]])
    N_s = np.array([[2,-4,2],[-3,4,-1],[1,0,0]])
    B_airfoil_s = np.matmul(U_matrix, N_s) # B-spline matrix for the airfoil points
    P_airfoil_s = np.matmul(B_airfoil_s, P_airfoil_rotate_offset)

    # print('B_airfoil_s: ',B_airfoil_s,'\n','P_airfoil_s: ',P_airfoil_s)

    foilbase_x = sp.lambdify(u, P_airfoil_s[0,0], modules='numpy')
    foilbase_x_values = foilbase_x(u_value) # x-coordinates of the airfoil path
    #print('foilbase_x: ',foilbase_x_values)
    foilbase_y_values = 0
    foilbase_z = sp.lambdify(u, P_airfoil_s[0,2], modules='numpy') 
    foilbase_z_values = foilbase_z(u_value) # z-coordinates of the airfoil path
    #print('foilbase_z: ',foilbase_z_values)


    ## Create points for tip of the fin by scaling the base airfoil points
    foil_scale = t/b # scale factor for the airfoil points
    # print('tip/root ratio:',foil_scale)
    P_airfoil_scale = np.array([[P4[0],P5[0],P6[0],1], [P4[1],P5[1],P6[1],1], [P4[2],P5[2],P6[2],1], [1,1,1,1]]) # scale the airfoil points
    Scale_matrix = np.array([[foil_scale,0,0,b-t],[0,foil_scale,0,h],[0,0,foil_scale,0],[0,0,0,foil_scale]])

    # print('P_airfoil_scale: \n',P_airfoil_scale)
    # print('Scale_matrix: \n',Scale_matrix)

    P_airfoil_tip = np.matmul(Scale_matrix,P_airfoil_scale)  # scale the airfoil points
    #print('P_airfoil_tip:\n', P_airfoil_tip)

    ## Create points for the top airfoil by using the scaled and translated airfoil points
    P7 = np.array([P_airfoil_tip[0,0], P_airfoil_tip[1,0], P_airfoil_tip[2,0]]) # leading edge of the airfoil
    P8 = np.array([P_airfoil_tip[0,1], P_airfoil_tip[1,1], P_airfoil_tip[2,1]]) # max camber of the airfoil
    P9 = np.array([P_airfoil_tip[0,2], P_airfoil_tip[1,2], P_airfoil_tip[2,2]]) # trailing edge of the airfoil

    P_airfoil_tip = np.array([P7, P8, P9]) # top airfoil points

    #move the airfoil points to the correct position down the envelope
    P7_offset = np.array([P7[0]+offset, P7[1], P7[2]]) 
    P8_offset = np.array([P8[0]+offset, P8[1], P8[2]])
    P9_offset = np.array([P9[0]+offset, P9[1], P9[2]])

    P_airfoil_tip_offset = np.array([P7_offset, P8_offset, P9_offset]) # top airfoil points with offset

    #ROTATE THE AIRFOIL
    P7_rotate = Ro_x(np.deg2rad(theta_deg), P7_offset[0], P7_offset[1], P7_offset[2])
    P8_rotate = Ro_x(np.deg2rad(theta_deg), P8_offset[0], P8_offset[1], P8_offset[2])
    P9_rotate = Ro_x(np.deg2rad(theta_deg), P9_offset[0], P9_offset[1], P9_offset[2])

    P_airfoil_tip_rotate_offset = np.array([P7_rotate, P8_rotate, P9_rotate]) # top airfoil points with offset and rotation

    P_airfoil_tip_u = np.matmul(B_airfoil_s, P_airfoil_tip_rotate_offset) # quadratic Parametric equation for the airfoil tip points

    ## fin tip airfoil converstion from P_u
    foiltip_x = sp.lambdify(u, P_airfoil_tip_u[0,0], modules='numpy')
    foiltip_x_values = foiltip_x(u_value) # x-coordinates of the airfoil path
    #print('foilbase_x: ',foilbase_x_values)
    foiltip_y_values = h
    foiltip_z = sp.lambdify(u, P_airfoil_tip_u[0,2], modules='numpy') 
    foiltip_z_values = foiltip_z(u_value) # z-coordinates of the airfoil path
    #print('foilbase_z: ',foilbase_z_values)

    #print('P_airfoil_tip_u: ',P_airfoil_tip_u)

    #### Surface plot of the fin

    S_uw_airfoil = (1-w)*P_airfoil_s + w*P_airfoil_tip_u # surface of the fin

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
    P11_rotate = Ro_x(-np.pi, P8[0], 0, P8[2]) # Underside Tip max camber point at axis

    P11_final = np.array([P11_rotate[0], h, P11_rotate[2]]) # Underside Tip max camber point at the actual tip of the fin
    # print('P5: ',P5, '\nP10: ',P10)
    # print('P8: ',P8, '\nP11: ',P11_final)

    P_mirror_base = np.array([P0, P10, P1])
    P_mirror_tip = np.array([P7, P11_final, P9])

    P10_offset = np.array([P10[0] + offset, P10[1], P10[2]]) 
    P11_final_offset = np.array([P11_final[0] + offset, P11_final[1], P11_final[2]]) 

    P_mirror_base_offset = np.array([P4_offset, P10_offset, P6_offset]) # mirrored base airfoil points with offset
    P_mirror_tip_offset = np.array([P7_offset, P11_final_offset, P9_offset]) # mirrored tip airfoil points with offset

    P10_rotate = Ro_x(np.deg2rad(theta_deg), P10_offset[0], P10_offset[1], P10_offset[2])
    P11_final_rotate = Ro_x(np.deg2rad(theta_deg), P11_final_offset[0], P11_final_offset[1], P11_final_offset[2])

    P_mirror_base_rotate_offset = np.array([P4_rotate, P10_rotate, P6_rotate]) # mirrored base airfoil points with offset and rotation
    P_mirror_tip_rotate_offset = np.array([P7_rotate, P11_final_rotate, P9_rotate]) # mirrored tip airfoil points with offset and rotation

    # parametric lines for base and tip mirrored airfoil curve
    P_mirror_base_u = np.matmul(B_airfoil_s, P_mirror_base_rotate_offset) # B-spline matrix for the mirrored base airfoil points
    P_mirror_tip_u = np.matmul(B_airfoil_s, P_mirror_tip_rotate_offset) # B-spline matrix for the mirrored tip airfoil points

    # print('P_mirror_base_u: ',P_mirror_base_u,'\n','P_mirror_tip_u: ',P_mirror_tip_u)

    ## fin mirrored airfoil converstion from P_u
    foilbase_mirrored_x = sp.lambdify(u, P_mirror_base_u[0,0], modules='numpy')
    foilbase_mirrored_x_values = foilbase_mirrored_x(u_value) # x-coordinates of the airfoil path
    foilbase_mirrored_y_values = 0
    foilbase_mirrored_z = sp.lambdify(u, P_mirror_base_u[0,2], modules='numpy') 
    foilbase_mirrored_z_values = foilbase_mirrored_z(u_value) # z-coordinates of the airfoil path

    ## fin tip mirrored airfoil converstion from P_u
    foiltip_mirrored_x = sp.lambdify(u, P_mirror_tip_u[0,0], modules='numpy')
    foiltip_mirrored_x_values = foiltip_mirrored_x(u_value) # x-coordinates of the airfoil path
    #print('foilbase_x: ',foilbase_x_values)
    foiltip_mirrored_y_values = h
    foiltip_mirrored_z = sp.lambdify(u, P_mirror_tip_u[0,2], modules='numpy') 
    foiltip_mirrored_z_values = foiltip_mirrored_z(u_value) # z-coordinates of the airfoil path
    #print('foilbase_z: ',foilbase_z_values)

    # bottom surface construction

    S_uw_airfoil_mirrored = (1-w)*P_mirror_base_u + w*P_mirror_tip_u # surface of the fin

    #print('S_uw_airfoil: ',S_uw_airfoil)

    S_surface_mirrored_x = sp.lambdify((u,w), S_uw_airfoil_mirrored[0,0], modules='numpy')
    S_surface_mirrored_y = sp.lambdify((u,w), S_uw_airfoil_mirrored[0,1], modules='numpy')
    S_surface_mirrored_z = sp.lambdify((u,w), S_uw_airfoil_mirrored[0,2], modules='numpy')
    u_value = np.linspace(0, 1, lines) # u values for the airfoil path
    w_value = np.linspace(0, 1, lines) # w values for the airfoil path

    S_surface_values_mirrored_x = np.zeros((len(u_value), len(w_value))) # initialize the surface values
    S_surface_values_mirrored_y = np.zeros((len(u_value), len(w_value))) # initialize the surface values
    S_surface_values_mirrored_z = np.zeros((len(u_value), len(w_value))) # initialize the surface values
    ribs_mirrored_x = np.zeros((len(u_value), len(w_value))) # initialize the ribs values
    ribs_mirrored_y = np.zeros((len(u_value), len(w_value))) # initialize the ribs values
    ribs_mirrored_z = np.zeros((len(u_value), len(w_value))) # initialize the ribs values

    for i in range(len(u_value)):
        for j in range(len(w_value)):
            S_surface_values_mirrored_x[i, j] = S_surface_mirrored_x(u_value[i], w_value[j]) # surface of the fin
            S_surface_values_mirrored_y[i, j] = S_surface_mirrored_y(u_value[i], w_value[j]) # surface of the fin
            S_surface_values_mirrored_z[i, j] = S_surface_mirrored_z(u_value[i], w_value[j]) # surface of the fin

            ribs_mirrored_x[i,j] = S_surface_mirrored_x(u_value[j], w_value[i])
            ribs_mirrored_y[i,j] = S_surface_mirrored_y(u_value[j], w_value[i])
            ribs_mirrored_z[i,j] = S_surface_mirrored_z(u_value[j], w_value[i])

    ax = main_window.plot_canvas.axis
    # Plot the surface lines of the airfoil
    for i in range(lines):
        main_window.plot_canvas.axis.plot(S_surface_values_x[i,:], S_surface_values_y[i,:], S_surface_values_z[i,:], color='black', alpha=0.5) # spanwise lines
        main_window.plot_canvas.axis.plot(ribs_x[i,:], ribs_y[i,:], ribs_z[i,:], color = 'black', alpha=0.5) # ribs of the airfoil fin
        main_window.plot_canvas.axis.plot(S_surface_values_mirrored_x[i,:], S_surface_values_mirrored_y[i,:], S_surface_values_mirrored_z[i,:], color = 'black', alpha=0.5) # spanwise lines
        main_window.plot_canvas.axis.plot(ribs_mirrored_x[i,:], ribs_mirrored_y[i,:], ribs_mirrored_z[i,:], color = 'black', alpha=0.5) # ribs of the airfoil fin
        # plt.plot(Surface_values_x2[i,:], Surface_values_y2[i,:], Surface_values_z2[i,:], label='S(u,w) fin2') # spanwise lines for fin2
        # plt.plot(ribs_x2[i,:], ribs_y2[i,:], ribs_z2[i,:], label='Ribs fin2') # ribs of the airfoil fin2
        # plt.plot(S_surface_values_mirrored_x2[i,:], S_surface_values_mirrored_y2[i,:], S_surface_values_mirrored_z2[i,:], label='S(u,w) fin2 mirrored') # spanwise lines for fin2 mirrored
        # plt.plot(ribs_mirrored_x2[i,:], ribs_mirrored_y2[i,:], ribs_mirrored_z2[i,:], label='Ribs fin2 mirrored') # ribs of the airfoil fin2 mirrored
        main_window.plot_canvas.draw()
    
    
    return S_surface_values_x, S_surface_values_y, S_surface_values_z, ribs_x, ribs_y, ribs_z, S_surface_values_mirrored_x, S_surface_values_mirrored_y, S_surface_values_mirrored_z, ribs_mirrored_x, ribs_mirrored_y, ribs_mirrored_z



# fin_lines = np.zeros(12)

# fin_lines = build_fin(h, b, t, offset, theta_deg) # build the fin with the given parameters

# S_surface_values_x = fin_lines[0]
# S_surface_values_y = fin_lines[1]
# S_surface_values_z = fin_lines[2]
# ribs_x = fin_lines[3]
# ribs_y = fin_lines[4]
# ribs_z = fin_lines[5]
# S_surface_values_mirrored_x = fin_lines[6]
# S_surface_values_mirrored_y = fin_lines[7]
# S_surface_values_mirrored_z = fin_lines[8]
# ribs_mirrored_x = fin_lines[9]
# ribs_mirrored_y = fin_lines[10]
# ribs_mirrored_z = fin_lines[11]                   

# theta_deg2 = 135

# fin_lines2 = np.zeros(12)
# fin_lines2 = build_fin(h, b, t, offset, theta_deg2) # build the fin with the given parameters

# Surface_values_x2 = fin_lines2[0]
# Surface_values_y2 = fin_lines2[1]
# Surface_values_z2 = fin_lines2[2]
# ribs_x2 = fin_lines2[3]
# ribs_y2 = fin_lines2[4]
# ribs_z2 = fin_lines2[5]
# S_surface_values_mirrored_x2 = fin_lines2[6]
# S_surface_values_mirrored_y2 = fin_lines2[7]
# S_surface_values_mirrored_z2 = fin_lines2[8]
# ribs_mirrored_x2 = fin_lines2[9]
# ribs_mirrored_y2 = fin_lines2[10]
# ribs_mirrored_z2 = fin_lines2[11]

# # Plot the surface lines of the airfoil
# for i in range(len(fin_lines[0])):
#     plt.plot(S_surface_values_x[i,:], S_surface_values_y[i,:], S_surface_values_z[i,:], label='S(u,w)') # spanwise lines
#     plt.plot(ribs_x[i,:], ribs_y[i,:], ribs_z[i,:], label='Ribs') # ribs of the airfoil fin
#     plt.plot(S_surface_values_mirrored_x[i,:], S_surface_values_mirrored_y[i,:], S_surface_values_mirrored_z[i,:], label='S(u,w)') # spanwise lines
#     plt.plot(ribs_mirrored_x[i,:], ribs_mirrored_y[i,:], ribs_mirrored_z[i,:], label='Ribs') # ribs of the airfoil fin
#     plt.plot(Surface_values_x2[i,:], Surface_values_y2[i,:], Surface_values_z2[i,:], label='S(u,w) fin2') # spanwise lines for fin2
#     plt.plot(ribs_x2[i,:], ribs_y2[i,:], ribs_z2[i,:], label='Ribs fin2') # ribs of the airfoil fin2
#     plt.plot(S_surface_values_mirrored_x2[i,:], S_surface_values_mirrored_y2[i,:], S_surface_values_mirrored_z2[i,:], label='S(u,w) fin2 mirrored') # spanwise lines for fin2 mirrored
#     plt.plot(ribs_mirrored_x2[i,:], ribs_mirrored_y2[i,:], ribs_mirrored_z2[i,:], label='Ribs fin2 mirrored') # ribs of the airfoil fin2 mirrored


## NO longer needed, but keeping for reference
# # Plot the airfoil base and tip curves for original and mirrored points for full airfoil
# # plt.plot(foilbase_x_values, foilbase_y_values, foilbase_z_values, color='black', label='Airfoil Path')  # Airfoil path
# # plt.plot(foiltip_x_values, foiltip_y_values, foiltip_z_values, color='black', label='Airfoil Top Path')  # Airfoil path
# # plt.plot(foiltip_mirrored_x_values, foiltip_mirrored_y_values, foiltip_mirrored_z_values, color='black', label='Airfoil Bottom Path')  # Airfoil path
# # plt.plot(foilbase_mirrored_x_values, foilbase_mirrored_y_values, foilbase_mirrored_z_values, color='black', label='Airfoil Bottom Path')  # Airfoil path



# ### Create a 3D plot

# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# ax = plt.axes(projection='3d')
# # Plot the edges of the fin and airfoil points by connecting the points
# # ax.plot([P0[0], P1[0]], [P0[1], P1[1]], [P0[2], P1[2]], color='blue', label='Base Edge')  # P0 to P1
# # ax.plot([P1[0], P2[0]], [P1[1], P2[1]], [P1[2], P2[2]], color='green', label='Height Edge')  # P1 to P2
# # ax.plot([P2[0], P3[0]], [P2[1], P3[1]], [P2[2], P3[2]], color='red', label='Tip Edge')  # P2 to P3
# # ax.plot([P3[0], P0[0]], [P3[1], P0[1]], [P3[2], P0[2]], color='purple', label='Diagonal Edge')  # P3 to P0
# # ax.plot([P4[0], P5[0]], [P4[1], P5[1]], [P4[2], P5[2]], color='orange', label='Airfoil Leading Edge')  # P4 to P5
# # ax.plot([P5[0], P6[0]], [P5[1], P6[1]], [P5[2], P6[2]], color='cyan', label='Airfoil Trailing Edge')  # P5 to P6
# # ax.plot([P7[0], P8[0]], [P7[1], P8[1]], [P7[2], P8[2]], color='yellow', label='Airfoil Top Leading Edge')  # P7 to P8
# # ax.plot([P0[0], P10[0]],[P0[1], P10[1]], [P0[1], P10[2]], color='magenta', label='Airfoil Top Trailing Edge')  # P0 to P10
# # ax.plot([P10[0], P1[0]],[P10[1], P1[1]], [P10[2], P1[2]], color='brown', label='Airfoil Bottom Trailing Edge')  # P10 to P1
# # ax.plot([P11_final[0], P3[0]],[P11_final[1], P3[1]], [P11_final[2], P3[2]], color='pink', label='Airfoil Bottom Leading Edge')  # P11 to P3
# # ax.plot([P11_final[0], P2[0]],[P11_final[1], P2[1]], [P11_final[2], P2[2]], color='grey', label='Airfoil Bottom Leading Edge')  # P11 to P8



# # Add a legend for clarity
# ax.legend(bbox_to_anchor = (1.1, 0.1))
# view_scale = int(input("set axis length for 3d plot:"))
# ax.set_zbound(0, view_scale) # set the z-axis limit for proper scale in the visualization
# ax.set_xbound(0, view_scale) # set the x-axis limit for proper scale in the visualization
# ax.set_ybound(0, view_scale) # set the y-axis limit for proper scale in the visualization
# plt.show()
### MERGE COMMENTS