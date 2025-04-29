import numpy as np
from math import comb, cos, sin, pi
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

# --- Find intersection points between gondola and envelope
def find_intersection_curve(gondola_points, envelope_vertices, threshold=0.5):
    intersection_pts = []
    for gpt in gondola_points:
        dists = np.linalg.norm(envelope_vertices - gpt, axis=1)
        if np.min(dists) < threshold:
            intersection_pts.append(gpt)
    return np.array(intersection_pts)

# --- Trim gondola panels below intersection curve
def trim_gondola(body_verts, intersection_curve):
    if len(intersection_curve) == 0:
        return body_verts  # nothing to trim if no intersection found
    z_cutoff = np.mean(intersection_curve[:,2])

    trimmed_verts = []
    for quad in body_verts:
        z_vals = [v[2] for v in quad]
        if all(z > z_cutoff for z in z_vals):
            trimmed_verts.append(quad)
    return trimmed_verts

# --- MAIN FUNCTION to draw the full gondola
def draw_canoe_gondola(main_window, length=50, width=20, height=10):
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

    # --- CENTER the gondola vertically
    # Find highest Z of gondola
    all_z = []
    for quad in body_verts:
        for vertex in quad:
            all_z.append(vertex[2])
    gondola_max_z = max(all_z)

    # Get lowest point of envelope
    envelope_lowest_z = np.min(main_window.low_pnt[:,2])

    # Shift needed
    z_shift = envelope_lowest_z - gondola_max_z

    # Shift body
    for quad in body_verts:
        for v in quad:
            v[2] += z_shift
    # Shift caps
    Zf += z_shift
    Zb += z_shift

    # --- FIND INTERSECTION
    gondola_pts = np.vstack([
        np.array(body_verts).reshape(-1,3),
        np.column_stack((Xf.flatten(), Yf.flatten(), Zf.flatten())),
        np.column_stack((Xb.flatten(), Yb.flatten(), Zb.flatten()))
    ])
    intersection_curve = find_intersection_curve(gondola_pts, main_window.env_verts)

    # --- TRIM GONDOLA
    body_verts = trim_gondola(body_verts, intersection_curve)

    return body_verts, (Xf, Yf, Zf), (Xb, Yb, Zb), intersection_curve










