
import pcl
from mayavi import mlab
import numpy as np
import time


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
    print(x)
    y =pointcloud[:, 1]
    z =  pointcloud[:, 2]
    mlab.points3d(x,y,z , color=(0, 1, 0), mode='sphere', scale_factor = 0.1)
    sensor = np.array([[0 ,0, 0]])
    mlab.points3d(sensor[:, 0], sensor[:, 1], sensor[:, 2], color=(1, 0, 0), mode='sphere', scale_factor=0.5)
   # mlab.axes(xlabel='x', ylabel='y', zlabel='z', ranges=( np.min(pointcloud[:, 0]), np.max(pointcloud[:, 0]), np.min(pointcloud[:, 1]), np.max(pointcloud[:, 1]), np.min(pointcloud[:, 2]), np.max(pointcloud[:, 2])), nb_labels=10)
   # mlab.axes(color=(1, 0, 1), xlabel='x', ylabel='y', zlabel='z', ranges=(np.min(x),np.max(x), np.min(y), np.max(y), np.min(z), np.max(z)), nb_labels = 5)

    mlab.show()
    return

# To visualize two pointclouds (The original one and the one obtained after the Ransac normally) and the
# plane obtained by the Ransac all together.
def viewer_original_vs_ransac_pointcloud_vs_plane(ransac_pcl, original_pcl, plane_model):
    sensor_range = 120.0
    mlab.figure(bgcolor=(1, 1, 1))
    x, y = np.ogrid[-sensor_range+50:sensor_range+50:1, -sensor_range:sensor_range:1]
    mlab.points3d(original_pcl[:, 0], original_pcl[:, 1], original_pcl[:, 2], color=(0, 0, 0), mode='point')
    mlab.points3d(ransac_pcl[:, 0], ransac_pcl[:, 1], ransac_pcl[:, 2], color=(1, 0, 0), mode='point')
    mlab.surf(x, y, (-plane_model[3] - (plane_model[0]*x) - (plane_model[1]*y)) / plane_model[2],
              color=(0.8, 0.8, 1), opacity=0.3)
    mlab.show()
    return


# To visualize two pointclouds in the viewer.
def viewer_pointcloud1_vs_pointcloud2(pointcloud1, pointcloud2):
    sensor_range = 120.0
    mlab.figure(bgcolor=(1, 1, 1))
    mlab.points3d(pointcloud1[:, 0], pointcloud1[:, 1], pointcloud1[:, 2], color=(0, 0, 0), mode='point')
    mlab.points3d(pointcloud2[:, 0], pointcloud2[:, 1], pointcloud2[:, 2], color=(1, 0, 0), mode='point')
    mlab.show()
    return


# Transform (rotate, translate) a PointCloud using the given transformation matrix.
def transform_pointcloud(transf_matrix, pointcloud):
    return np.delete(np.transpose(np.dot(transf_matrix,
                                         np.transpose(np.c_[pointcloud, np.ones(pointcloud.shape[0])]))), 3, axis=1)
# --------------------------------------------------------------------------------------------------------------------



def main():

    # Exercise 1 - Ransac to detect the Main Plane
    pointcloud = read_pcd_file("adquisicionUltra.pcd")
    print("numero de puntos = {}".format(pointcloud.shape[0]))
    viewer_pointcloud2(pointcloud)



if __name__ == '__main__':
    main()