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


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

pointcloud = np.loadtxt('Chiffon/adquisicionUltra_Mant.out')
color  = np.loadtxt('Chiffon/adquisicionColorUltra_Mant.out')
print("Numero de datos: {}".format(pointcloud.shape[0]))
xs = pointcloud[:, 0]
ys =  pointcloud[:, 1]
zs =  pointcloud[:, 2]
ax.scatter(xs, ys, zs, c=color)
ax.scatter(0, 0, 0, c = (0, 0, 0, 1) )

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
