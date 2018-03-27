'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pcl


# Read a .pcd file, just give the path to the file. The function will return the pointcloud as a numpy array.
def read_pcd_file(input_filename):
    return pcl.load(input_filename).to_array()


def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].

# Exercise 1 - Ransac to detect the Main Plane
# pointcloud = read_pcd_file("../resources/pcl1exercise2.pcd")

# Datos de motores calibrados
phi_180 = 228
phi_0 = 36
phi_resol = (phi_180 - phi_0 + 1) / 180.0
phi_step = 1.0  # un paso
ni_phi = int(round((phi_180 - phi_0 + 1) / phi_step))  # numero de angulos phi

theta_90 = 245
theta_0 = 131
theta_min = 100  # minimo angulo sin que el motor choque con la base
theta_resol = (theta_90 - theta_0 + 1) / 90.0
theta_step = 10.0  # un paso
ni_theta = int(round((theta_90 - theta_0 + 1) / theta_step))  # numero de angulos theta

data = np.zeros([0, 3])
r = 1
for theta in np.arange(0, 90, 90.0 / (ni_theta / 2)):
    for phi in np.arange(0, 180, 180.0 / (ni_phi / 2)):
        theta_prima = theta * np.pi / 180
        phi_prima = phi * np.pi / 180
        x = r * np.sin(theta_prima) * np.cos(phi_prima)
        y = r * np.sin(theta_prima) * np.sin(phi_prima)
        z = r * np.cos(theta_prima)
        data = np.append(data, [[x, y, z]], 0)

pointcloud =read_pcd_file("../../Integracion/adquisicionInfra.pcd")
print("Numero de datos: {}".format(pointcloud.shape[0]))
xs = pointcloud[:, 0]
ys =  pointcloud[:, 1]
zs =  pointcloud[:, 2]
color = np.cos(zs)
ax.scatter(xs, ys, zs, c=color)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
