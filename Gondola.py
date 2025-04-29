import numpy as np
import matplotlib.pyplot as plt
from math import comb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# --- Bézier curve evaluator
def bezier_curve(control_points, num_points=150):
    m = len(control_points)
    n = m - 1
    u = np.linspace(0.0, 1.0, num_points)
    B = np.zeros((num_points, m), dtype=float)
    for i in range(m):
        B[:, i] = comb(n, i) * (u**i) * (1-u)**(n-i)
    return B @ np.array(control_points)

# --- Create body cross-section Bézier curve
def create_cross_section_curve(length, width, height, base_x):
    side_frac = 0.25
    ctrl_pts = np.array([
        [base_x, -width/2, 0.0],
        [base_x, -side_frac*width, -height],
        [base_x, 0.0, -height],
        [base_x, side_frac*width, -height],
        [base_x, width/2, 0.0]
    ])
    return bezier_curve(ctrl_pts, num_points=150), ctrl_pts

# --- Loft the body between two cross sections
def loft_cross_sections(front_curve, rear_curve, num_sections=30):
    w_vals = np.linspace(0, 1, num_sections)
    surface = []
    for w in w_vals:
        loft_slice = (1 - w) * front_curve + w * rear_curve
        surface.append(loft_slice)
        # print(loft_slice)
    return np.array(surface)

# --- Generate a cap surface matrix using Eqn 2.87
def generate_cap_surface(control_pts, base_x, sweep_angle=np.pi, num_curve=100, num_theta=100):
    curve = bezier_curve(control_pts, num_curve)
    P_y = curve[:,1]
    P_z = curve[:,2]

    u_vals = np.linspace(0, 1, num_curve)
    w_vals = np.linspace(0, sweep_angle, num_theta)
    U, W = np.meshgrid(u_vals, w_vals, indexing='ij')

    P_yu = np.interp(U, np.linspace(0,1,len(P_y)), P_y)
    P_zu = np.interp(U, np.linspace(0,1,len(P_z)), P_z)

    X = base_x + P_yu * np.cos(W)
    Y = P_yu * np.sin(W)
    Z = P_zu

    return X, Y, Z

# --- Main function to draw the full gondola
def draw_canoe_gondola(main_window=None, length=50, width=20, height=10, env_low_point=(100,0,0)):
    N_curve = 150
    N_sections = 30

    # Front and rear cross-section Bézier curves
    front_curve, ctrl_pts_front = create_cross_section_curve(length, width, height, base_x=0)
    rear_curve, ctrl_pts_rear  = create_cross_section_curve(length, width, height, base_x=length)

    # Lofted body
    lofted_surface = loft_cross_sections(front_curve, rear_curve, num_sections=N_sections)

    # BODY faces
    body_verts = []
    for i in range(N_sections-1):
        for j in range(N_curve-1):
            p0 = lofted_surface[i, j]
            p1 = lofted_surface[i+1, j]
            p2 = lofted_surface[i+1, j+1]
            p3 = lofted_surface[i, j+1]
            body_verts.append([p0.copy(), p1.copy(), p2.copy(), p3.copy()])



    # NOSE cap (front)
    Xf, Yf, Zf = generate_cap_surface(ctrl_pts_front, base_x=0, sweep_angle=np.pi, num_curve=100, num_theta=100)

    # TAIL cap (back)
    Xb, Yb, Zb = generate_cap_surface(ctrl_pts_rear, base_x=length, sweep_angle=np.pi, num_curve=100, num_theta=100)

    # --- Calculate gondola center and top
    all_x, all_y, all_z = [], [], []
    for quad in body_verts:
        for v in quad:
            all_x.append(v[0])
            all_y.append(v[1])
            all_z.append(v[2])

    gondola_center_x = (min(all_x) + max(all_x)) / 2
    gondola_center_y = (min(all_y) + max(all_y)) / 2
    gondola_top_z    = max(all_z)
    #main_window.logback.append(env_low_point[0])
    # --- Shift to match desired envelope low point
    env_x, env_y, env_z = env_low_point

    x_shift = env_x - gondola_center_x
    y_shift = env_y - gondola_center_y
    z_shift = env_z - gondola_top_z

    # --- Apply shifts to lofted_surface
    lofted_surface[:, :, 0] += x_shift  # Shift X-coordinates
    lofted_surface[:, :, 1] += y_shift  # Shift Y-coordinates
    lofted_surface[:, :, 2] += z_shift  # Shift Z-coordinates

    Xf += x_shift
    Yf += y_shift
    Zf += z_shift

    Xb += x_shift
    Yb += y_shift
    Zb += z_shift

    # --- Plot
    #print(body_verts)
    # Body
    #body_poly = Poly3DCollection(lofted_surface, facecolor='silver', alpha=0.9, linewidths=0.05)
    #ax.add_collection3d(body_poly)

    main_window.plot_canvas.axis.plot_wireframe(lofted_surface[:, :, 0], lofted_surface[:, :, 1], lofted_surface[:, :, 2],
                    color='black', alpha=0.9)

    # Nose Cap
    main_window.plot_canvas.axis.plot_wireframe(Xf, Yf, Zf, color='black',alpha=0.9)

    # Tail Cap
    main_window.plot_canvas.axis.plot_wireframe(Xb, Yb, Zb, color='black',alpha=0.9)

    return body_verts, (Xf,Yf,Zf), (Xb,Yb,Zb)














