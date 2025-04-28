import numpy as np
from math import comb, cos, sin, pi
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
'''
def bezier_curve(control_points, num_points=100):
    """
    Generate a Bezier curve of arbitrary degree from control_points.
    Returns (num_points,2) array of [x,z]
    """
    m = len(control_points)
    n = m - 1
    u = np.linspace(0.0, 1.0, num_points)
    B = np.zeros((num_points, m), dtype=float)
    for i in range(m):
        B[:, i] = comb(n, i) * (u**i) * ((1 - u)**(n - i))
    return B.dot(control_points)


def draw_gondola(main_window, length, width, height,
                  nose_sharp=2.0, tail_sharp=2.0, plateau_scale=1.0):
    """
    Draws the gondola by revolving a 2D Bezier profile around the X-axis.
    - length: longitudinal extent
    - width: lateral (max diameter)
    - height: vertical profile height
    - nose_sharp, tail_sharp >1 make the ends sharper
    - plateau_scale between 0–1 scales midsection
    """
    # define fractions along length
    r_frac = 0.2 * (nose_sharp / (nose_sharp + 1.0))
    t_frac = 1.0 - 0.2 * (tail_sharp / (tail_sharp + 1.0))
    p = plateau_scale

    # control points [x,z]
    ctrl = np.array([
        [0.0,          0.0       ],  # nose tip
        [r_frac*length, p*height ],  # nose shoulder
        [0.5*length,    p*height ],  # mid plateau
        [t_frac*length, p*height ],  # tail shoulder
        [length,       0.0       ]   # tail tip
    ])

    # sample profile
    profile = bezier_curve(ctrl, num_points=150)
    X2d = profile[:,0]
    Z2d = profile[:,1]

    # revolve
    verts = []
    angles = np.linspace(0, 2*pi, 60)
    for i in range(len(X2d)-1):
        for j in range(len(angles)-1):
            # radius scales to width
            r0 = (Z2d[i]/height)*(width/2.0)
            r1 = (Z2d[i+1]/height)*(width/2.0)
            x0, x1 = X2d[i], X2d[i+1]
            w0, w1 = angles[j], angles[j+1]
            verts.append([
                [x0, r0*cos(w0),  r0*sin(w0)],
                [x1, r1*cos(w0),  r1*sin(w0)],
                [x1, r1*cos(w1),  r1*sin(w1)],
                [x0, r0*cos(w1),  r0*sin(w1)]
            ])

    # alignment: keep top of gondola at envelope low point
    lp = np.atleast_1d(main_window.low_pnt)[0]
    base_x, base_y, base_z = lp
    # vertical translation so profile height matches envelope
    for quad in verts:
        for v in quad:
            v[0] += base_x - length/2.0
            v[1] += base_y
            v[2] += base_z  # keep top center fixed

    # render
    ax = main_window.plot_canvas.axis
    poly = Poly3DCollection(verts, facecolor='gray', alpha=0.8, linewidths=0.02)
    ax.add_collection3d(poly)
    # ax.set_xlim(base_x - length/2, base_x + length/2)
    # ax.set_ylim(base_y - width/2,  base_y + width/2)
    # ax.set_zlim(base_z - width/2,  base_z + width/2)
    main_window.plot_canvas.draw()

    verts_arr = np.array(verts).reshape(-1,3)
    return verts_arr, verts
'''




# Option 2

# -----------------------
# Gondola Function
# -----------------------
# gondola.py

import numpy as np
import matplotlib.pyplot as plt
from math import comb, cos, sin, pi

# ----------------------------- 0. Your original Bézier loft body -----------------------------
def bezier_curve(control_points, num_points=150):
    m = len(control_points)
    n = m - 1
    u = np.linspace(0.0, 1.0, num_points)
    B = np.zeros((num_points, m), dtype=float)
    for i in range(m):
        B[:, i] = comb(n, i) * (u**i) * ((1 - u)**(n - i))
    return B @ np.array(control_points)

def draw_gondola_body(length, width, height):
    # front and rear Bézier control nets in 3D:
    r_frac = 0.2
    t_frac = 0.8
    ctrl_front = np.array([
        [0.0,           -width/2,  0.0],
        [0.0,           -width*r_frac, -height],
        [0.0,            0.0,      -height],
        [0.0,            width*r_frac, -height],
        [0.0,            width/2,   0.0]
    ])
    ctrl_rear = ctrl_front.copy()
    ctrl_rear[:,0] += length

    front_curve = bezier_curve(ctrl_front)
    rear_curve  = bezier_curve(ctrl_rear)
    return front_curve, rear_curve

def loft_gondola(front_curve, rear_curve, num_slices=30):
    us = np.linspace(0,1,num_slices)
    slices = []
    for u in us:
        slices.append((1-u)*front_curve + u*rear_curve)
    return np.stack(slices)

# ----------------------------- 1. Quarter-circle cap profile -----------------------------
def create_cap_profile(length_cap, radius_max, num_points=30):
    """
    Returns (num_points,2) of [x, r] from (length_cap,0) to (0,radius_max)
    """
    t = np.linspace(0, np.pi/2, num_points)
    x = length_cap * np.cos(t)
    r = radius_max  * np.sin(t)
    return np.column_stack((x, r))

# ----------------------------- 2. Loft that profile into a single point -----------------------------
def loft_cap(profile, center_x, num_slices=20):
    """
    profile: (N,2) [x,r] in X–r plane
    center_x: the X where the single point lives
    returns: (num_slices, N, 3) slices of [X,Y,Z]
    """
    us = np.linspace(0,1,num_slices)
    theta = np.linspace(0,2*np.pi, profile.shape[0])
    slices = []
    # precompute profile sampling positions
    base_u = np.linspace(0,1, profile.shape[0])
    for u in us:
        # get one ring coords
        x_ring = np.interp(u, base_u, profile[:,0]) + center_x
        r_ring = np.interp(u, base_u, profile[:,1])
        # full circle
        Ys = r_ring * np.cos(theta)
        Zs = r_ring * np.sin(theta)
        Xs = np.full_like(theta, x_ring)
        # now linearly loft toward the single point (center_x,0,0)
        lam = 1-u
        Xs = lam*Xs + (1-lam)*center_x
        Ys = lam*Ys
        Zs = lam*Zs
        slices.append(np.column_stack((Xs,Ys,Zs)))
    return np.stack(slices)

# ----------------------------- 3. Main test & plot -----------------------------
if __name__=="__main__":
    # parameters
    L = 40.0
    W = 15.0
    H =  5.0
    cap_len = 5.0
    cap_rad = W/2

    # build body
    front, rear = draw_gondola_body(L,W,H)
    body = loft_gondola(front, rear, num_slices=40)

    # build caps
    prof = create_cap_profile(cap_len, cap_rad, num_points=50)
    nose = loft_cap(prof, center_x=-cap_len, num_slices=20)
    tail = loft_cap(prof, center_x=   L, num_slices=20)

    # plot
    fig = plt.figure(figsize=(12,8))
    ax  = fig.add_subplot(111, projection='3d')

    # body slices
    for s in body:
        ax.plot(s[:,0], s[:,1], s[:,2], color='gray', alpha=0.6)
    # nose
    for s in nose:
        ax.plot(s[:,0], s[:,1], s[:,2], color='green')
    # tail
    for s in tail:
        ax.plot(s[:,0], s[:,1], s[:,2], color='red')

    ax.set_box_aspect([L+2*cap_len, W, W])
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    ax.set_title("Lofted Gondola Body + Bézier Caps (no revolve)")
    plt.show()







