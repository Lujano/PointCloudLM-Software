import pcl
from mayavi import mlab
import numpy as np


# Read a .pcd file, just give the path to the file. The function will return the pointcloud as a numpy array.
def read_pcd_file(input_filename):
    return pcl.load(input_filename).to_array()


# Save your pointcloud as a .pcd file in order to use it in other # programs (cloudcompare for example).
def write_pcd_file(pointcloud, output_path):
    output_pointcloud = pcl.PointCloud()
    output_pointcloud.from_array(np.float32(pointcloud))
    output_pointcloud.to_file(output_path)
    return


# To visualize the passed pointcloud.
def viewer_pointcloud(pointcloud):
    mlab.figure(bgcolor=(1, 1, 1))
    mlab.points3d(pointcloud[:, 0], pointcloud[:, 1], pointcloud[:, 2], color=(0, 0, 0), mode='point')
    mlab.show()
    return


def viewer_pointcloud2(pointcloud):
    mlab.figure(bgcolor=(1 ,1, 1) )
    x = pointcloud[:, 0]
    y =pointcloud[:, 1]
    z =  pointcloud[:, 2]
    mlab.points3d(x,y,z , color=(0, 1, 0), mode='sphere', scale_factor = 0.1)
    sensor = np.array([[0 ,0, 0]])
    #mlab.points3d(sensor[:, 0], sensor[:, 1], sensor[:, 2], color=(1, 0, 0), mode='sphere', scale_factor=0.5)
   # mlab.axes(xlabel='x', ylabel='y', zlabel='z', ranges=( np.min(pointcloud[:, 0]), np.max(pointcloud[:, 0]), np.min(pointcloud[:, 1]), np.max(pointcloud[:, 1]), np.min(pointcloud[:, 2]), np.max(pointcloud[:, 2])), nb_labels=10)
   # mlab.axes(color=(1, 0, 1), xlabel='x', ylabel='y', zlabel='z', ranges=(np.min(x),np.max(x), np.min(y), np.max(y), np.min(z), np.max(z)), nb_labels = 5)

    mlab.show()
    return


def main():
    p = pcl.PointCloud()
    p.from_file("../Data/adquisicion5.pcd")
    fil = p.make_statistical_outlier_filter()
    fil.set_mean_k(5)
    fil.set_std_dev_mul_thresh(0.5)
    fil.filter().to_file("../Data/inliers.pcd")

    pointcloud1 = read_pcd_file("../Data/adquisicion5.pcd")
    pointcloud2 = read_pcd_file("../Data/inliers.pcd")
    mlab.figure(bgcolor=(1, 1, 1))
    mlab.points3d(pointcloud1[:, 0], pointcloud1[:, 1], pointcloud1[:, 2], color=(0, 0, 0), mode='sphere', scale_factor = 0.1)

    mlab.figure(bgcolor=(1, 1, 1))
    mlab.points3d(pointcloud2[:, 0], pointcloud2[:, 1], pointcloud2[:, 2], color=(0, 0, 0), mode='sphere', scale_factor = 0.1)
    mlab.show()




if __name__ == '__main__':
    main()