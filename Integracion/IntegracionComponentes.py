
# In order to create the environment for running this code, remember to run the
# following command in your Anaconda command line:
# --> conda create --name 3dclass --channel ccordoba12 python=2.7 pcl python-pcl numpy matplotlib mayavi

import pcl
from mayavi import mlab
import numpy as np
import time
import serial


def open_port():
    ser = serial.Serial('COM27', 115200)

    return ser

def close_port(port):
    port.close()

def detect_data(port):
    #port.reset_input_buffer()
    flag = True

    while flag:
        anuncio = port.read(1)
        anuncio = ord(anuncio[0]) # convertir en entero

        if (anuncio & 0xf0)  == 0xf0: # Se detecta el byte de anuncio de trama
                n_canales = anuncio & 0x0f # Numero de canales a leer
                return  n_canales


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

# --------------------------------------------------------------------------------------------------------------------


def main():

    # Exercise 1 - Ransac to detect the Main Plane
    #pointcloud = read_pcd_file("../resources/pcl1exercise2.pcd")

    # Datos de motores calibrados
    phi_180 = 228
    phi_0 = 36
    phi_resol = 180.0/(phi_180 - phi_0 + 1)
    phi_step = 1.0  # un paso
    ni_phi = int(round((phi_180 - phi_0 + 1) / phi_step))  # numero de angulos phi

    theta_90 = 245
    theta_0 = 131
    theta_min = 100  # minimo angulo sin que el motor choque con la base
    theta_resol = 90.0/(theta_90 - theta_0 + 1)
    theta_step = 1.0  # un paso
    ni_theta = int(round((theta_90 - theta_0 + 1) / theta_step))  # numero de angulos theta

    port = open_port()
    # i = 0.00
    # y = 0.00
    # Amplitud_matrix = np.array([])
    # Time_matrix = np.array([])
    T_Inicio = time.time()
    T_Final = time.time()
    Dif = T_Final - T_Inicio

    # matriz de datos
    # Convertir data a nube de puntos
    data = np.zeros([0, 3])
    step2 = theta_0
    while (step2 <= theta_0+80):  # Contar 10 segundos
        n_canales = detect_data(port)
        data_in = port.read(2 * n_canales)
        canal_n1 = (2 ** 7) * ord(data_in[0]) + ord(data_in[1])
        echo = (2 ** 15) * ord(data_in[2]) + (2 ** 8) * ord(data_in[3]) + (2 ** 7) * ord(data_in[4]) + ord(data_in[5])
        step1 = (2 ** 7) * ord(data_in[6]) + ord(data_in[7])
        step2 = (2 ** 7) * ord(data_in[8]) + ord(data_in[9])

        phi_prima = step1
        theta_prima = step2
        phi = phi_180-phi_prima
        theta = theta_90 - theta_prima
        if (echo< 28000) :
            r = echo/580.0 #metros
            theta = theta *theta_resol*np.pi / 180.0
            phi = phi *phi_resol*np.pi / 180.0
            x = r * np.sin(theta) * np.cos(phi)
            y = r * np.sin(theta) * np.sin(phi)
            z = r * np.cos(theta)
            data = np.append(data, [[x, y, z]], 0)
            #y = canal_n1 * 3.2 / (2 ** 12 - 1)  # Escalamiento
            #i += 1
            # Amplitud_matrix = np.append(Amplitud_matrix, [y])
            # Time_matrix = np.append(Time_matrix, [i])
            T_Final = time.time()
            Dif = T_Final - T_Inicio
            print("distance = {}, theta = {}, phi = {}".format(echo / 58.0, theta*180.0/np.pi, phi*180/np.pi))

    close_port(port)
    # plt.plot(Time_matrix, Amplitud_matrix)
    # plt.show()
    # Graficar datos


    pointcloud = data
    print(data)
    print("Numero de datos: {}".format(pointcloud.shape[0]))
    mlab.figure(bgcolor=(1, 1, 1))
    mlab.points3d(pointcloud[:, 0], pointcloud[:, 1], pointcloud[:, 2], color=(0, 1, 0), mode='sphere',
                  scale_factor=0.025)
    sensor = np.array([[0 ,0, 0]])
    mlab.points3d(sensor[:, 0], sensor[:, 1], sensor[:, 2], color=(1, 0, 0), mode='sphere',
                  scale_factor=0.5)

    mlab.show()
    write_pcd_file(pointcloud, "adquisicion2.pcd")


if __name__ == '__main__': main()