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

pointcloud = np.loadtxt('../Data/Chiffon/adquisicionInfra_Mant.out')
pointcloud2 = np.loadtxt('../Data/Chiffon/adquisicionUltra_Mant.out')

