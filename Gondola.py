import numpy as np
from math import comb

# --- Bézier curve evaluator
def bezier_curve(control_points, num_points=150):
    m = len(control_points)
    n = m - 1
    u = np.linspace(0.0, 1.0, num_points)
    B = np.zeros((num_points, m), dtype=float)
    for i in range(m):
        B[:, i] = comb(n, i) * (u**i) * (1-u)**(n-i)
    return B @ np.array(control_points)

# --- Create cross-section curve for body
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

# --- Loft body between front and rear cross-sections
def loft_cross_sections(front_curve, rear_curve, num_sections=30):
    w_vals = np.linspace(0, 1, num_sections)
    surface = []
    for w in w_vals:
        loft_slice = (1 - w) * front_curve + w * rear_curve
        surface.append(loft_slice)
    return np.array(surface)

# --- Generate cap surfaces using Eqn 2.87
def generate_cap_surface(control_pts, base_x, sweep_angle=np.pi, num_curve=100, num_theta=100):
    # Step 1: Evaluate Bézier cross-section
    curve = bezier_curve(control_pts, num_curve)
    P_y = curve[:,1]  # y-values
    P_z = curve[:,2]  # z-values

    # Step 2: Create u-w grid
    u_vals = np.linspace(0, 1, num_curve)
    w_vals = np.linspace(0, sweep_angle, num_theta)
    U, W = np.meshgrid(u_vals, w_vals, indexing='ij')

    # Step 3: Expand P_y and P_z into (u,w) grids
    P_yu = np.interp(U, np.linspace(0,1,len(P_y)), P_y)
    P_zu = np.interp(U, np.linspace(0,1,len(P_z)), P_z)

    # Step 4: Apply surface revolution formula
    X = base_x + P_yu * np.cos(W)
    Y = P_yu * np.sin(W)
    Z = P_zu

    return X, Y, Z

# --- MAIN FUNCTION to draw the full gondola
def draw_canoe_gondola(length=50, width=20, height=10):
    N_curve = 150
    N_sections = 30

    # --- Create body cross-sections
    front_curve, ctrl_pts_front = create_cross_section_curve(length, width, height, base_x=0)
    rear_curve, ctrl_pts_rear = create_cross_section_curve(length, width, height, base_x=length)

    # --- Lofted body surface
    lofted_surface = loft_cross_sections(front_curve, rear_curve, num_sections=N_sections)

    # --- Build BODY faces (quads)
    body_verts = []
    for i in range(N_sections-1):
        for j in range(N_curve-1):
            p0 = lofted_surface[i, j]
            p1 = lofted_surface[i+1, j]
            p2 = lofted_surface[i+1, j+1]
            p3 = lofted_surface[i, j+1]
            body_verts.append([p0, p1, p2, p3])

    # --- Build NOSE CAP
    Xf, Yf, Zf = generate_cap_surface(ctrl_pts_front, base_x=0, sweep_angle=np.pi, num_curve=100, num_theta=100)

    # --- Build TAIL CAP
    Xb, Yb, Zb = generate_cap_surface(ctrl_pts_rear, base_x=length, sweep_angle=np.pi, num_curve=100, num_theta=100)

    return body_verts, (Xf, Yf, Zf), (Xb, Yb, Zb)









