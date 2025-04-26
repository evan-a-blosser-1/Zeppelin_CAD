import numpy as np
from math import comb, cos, sin, pi
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

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
                  nose_sharp, tail_sharp, plateau_scale):
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
