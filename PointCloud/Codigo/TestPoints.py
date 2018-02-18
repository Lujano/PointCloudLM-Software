import numpy as np
from mayavi import mlab

def test_points3d():
    t = np.linspace(0, 4 * np.pi, 200)
    cos = np.cos
    sin = np.sin

    x = sin(2 * t)
    y = cos(t)
    z = cos(2 * t)
    s = 2 + sin(t)

    return points3d(x, y, z, s, colormap="copper", scale_factor=.25)



if __name__ == "__main__":
    t = np.linspace(0, 4 * np.pi, 500)
    cos = np.cos
    sin = np.sin

    x = sin(2 * t)
    y = cos(t)
    z = cos(2 * t)
    s = 2 + sin(t)

    mlab.points3d(x, y, z, colormap="copper", scale_factor=.5)
    mlab.axes(xlabel='x', ylabel='y', zlabel='z', ranges=(0, np.max(x), 0, np.max(y), 0, np.max(z)), nb_labels=10)
    x, y, z = np.mgrid[-2:3, -2:3, -2:3]
    r = np.sqrt(x ** 2 + y ** 2 + z ** 4)
    u = y * np.sin(r) / (r + 0.001)
    v = -x * np.sin(r) / (r + 0.001)
    w = np.zeros_like(z)
    #obj = mlab.quiver3d(x, y, z, u, v, w, line_width=3, scale_factor=1)
    mlab.show()


