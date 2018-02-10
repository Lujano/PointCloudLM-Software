# Luis Roldao - Universidad Simon Bolivar
# 30-Nov-2017
# In order to create the environment for running this code, remember to run the
# following command in your Anaconda command line:
# --> conda create --name 3dclass --channel ccordoba12 python=2.7 pcl python-pcl numpy matplotlib mayavi

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
    mlab.points3d(pointcloud[:, 0], pointcloud[:, 1], pointcloud[:, 2], color=(0, 1, 0), mode='sphere', scale_factor = 0.025)
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


def normalize_vector(vector):
    return vector/np.linalg.norm(vector)


# --------------------------------------------------------------------------------------------------------------------
# This is the function to complete, it should receive a pointcloud (numpy array [x, y, z],[x, y, z]...),
# the number of iterations of the Ransac and the threshold to be used. It should return a new pointcloud
# numpy array with the points extracted by the Ransac and a numpy array with the variables of the plane
# (A, B, C, D) - Remember that the equation of the plane Ax+By+Cz+D=0 defines the plane itself.
def random_sampling_consensus(pointcloud, numb_iterations, threshold):

    # FILL THE FUNCTION --------------------------------

    # Return the requested variables
    N = pointcloud.shape[0]

    #
    ransac_pointcloud = np.zeros((0, 3))
    scoremax = 0
    for i in range(numb_iterations):
        points_inside = 0
        # Generar 3 puntos aleatorios
        #i1, i2, i3 = random.randrange(0, N), random.randrange(0, N), random.randrange(0, N)
        [i1, i2, i3] = np.random.choice(N, 3, replace= False)

        # Crear 2 vectores y verificar que no son coplanares
        p1, p2, p3 = pointcloud[i1], pointcloud[i2], pointcloud[i3]
        vector_p2p1 =p1-p2
        vector_p2p3 =p3-p2
        while (np.cross(vector_p2p1, vector_p2p3)[0] == 0) and (np.cross(vector_p2p1, vector_p2p3)[1] == 0) and (np.cross(vector_p2p1, vector_p2p3)[2] == 0) :
            # Generar 3 puntos aleatorios
            [i1, i2, i3] = np.random.choice(N, 3, replace=False)
            p1, p2, p3 = pointcloud[i1], pointcloud[i2], pointcloud[i3]

            # Crear 2 vectores y verificar que no son coplanares
            vector_p2p1 = p1 - p2
            vector_p2p3 = p3 - p2
            print('a')
        # Points
        [x1, y1, z1] = p1
        [x2, y2, z2] = p2
        [x3, y3, z3] = p3
        A = (y3-y2)*(z1-z2)-(z3-z2)*(y1-y2)
        B = (z3-z2)*(x1-x2)-(x3-x2)*(z1-z2)
        C = (x3-x2)*(y1-y2)-(y3-y2)*(x1-x2)
        D = -A*x1 -B*y1- C*z1

        # Calcular distancias sobre todos los puntos de los datos al plano

        for ip in range(N):
            [xi, yi, zi] = pointcloud[ip]
            d = abs(A*xi +B*yi+ C*zi+D)/np.sqrt(A**2+B**2+C**2)

            if d<threshold:
                points_inside += 1

        if points_inside >= scoremax:
            [rancA, rancB, rancC, rancD] = [A, B, C, D]
            scoremax = points_inside

    for ip in range(N):
        [xi, yi, zi] = pointcloud[ip]

        d = abs(rancA * xi + rancB * yi + rancC * zi + rancD) / np.sqrt(rancA ** 2 + rancB ** 2 + rancC ** 2)

        if d < threshold:
            ransac_pointcloud = np.vstack([ ransac_pointcloud,[ xi, yi, zi]] )

    return [ransac_pointcloud , [rancA, rancB, rancC, rancD]]






# --------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------
# Given 2 plane models, calculate the rotation matrix that fits both planes
def calculate_rotation_matrix(plane_model1, plane_model2):

    # FILL THE FUNCTION --------------------------------

    # Return the requested variables
    return transformation_matrix
# --------------------------------------------------------------------------------------------------------------------


def main():

    # Exercise 1 - Ransac to detect the Main Plane
    #pointcloud = read_pcd_file("../resources/pcl1exercise2.pcd")

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
    theta_step = 1.0  # un paso
    ni_theta = int(round((theta_90 - theta_0 + 1) / theta_step))  # numero de angulos theta

    data = np.zeros([0, 3])
    r = 5
    for theta in np.arange(0, 90, 90.0/(ni_theta/2)):
        for phi in np.arange (0, 180, 180.0/(ni_phi/2)):
            theta_prima = theta*np.pi/180
            phi_prima = phi*np.pi/180
            x = r*np.sin(theta_prima)*np.cos(phi_prima)
            y = r*np.sin(theta_prima)*np.sin(phi_prima)
            z = r*np.cos(theta_prima)
            data = np.append(data, [[x, y, z]], 0)
    pointcloud = data
    print("Numero de datos: {}".format(pointcloud.shape[0]))
    mlab.figure(bgcolor=(1, 1, 1))
    mlab.points3d(pointcloud[:, 0], pointcloud[:, 1], pointcloud[:, 2], color=(0, 1, 0), mode='sphere',
                  scale_factor=0.025)
    sensor = np.array([[0 ,0, 0]])
    mlab.points3d(sensor[:, 0], sensor[:, 1], sensor[:, 2], color=(1, 0, 0), mode='sphere',
                  scale_factor=0.5)



    mlab.show()


if __name__ == '__main__':
    main()