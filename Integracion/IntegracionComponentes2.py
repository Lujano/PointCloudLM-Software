"""
En este codigo ya se tiene calibrado el infrarrojo a traves de un ajuste polinomial
y se toman 16 medidas del valor del adc
Se a#ade la camara para obtener el color del punto bajo medicion
"""
import pcl
from mayavi import mlab
import numpy as np
import time
import serial
import winsound
import cv2
from Pixel_Fun import Pixel_Fun


def open_port():
    ser = serial.Serial('COM12', 9800)

    return ser

def close_port(port):
    port.close()

def detect_data1(port):
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
def viewer_original_vs_ransac_pointcloud_vs_plane(ransac_pcl, original_pqcl, plane_model):
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

def mean_color (image, centerx, centery, w1, h1):
    w, h = image.shape[1], image.shape[0]
    canvas = np.zeros((h, w, 3), dtype='uint8')
    cv2.rectangle(canvas, (centerx-w1, centery-h1), (centerx+w1, centery+h1), (255,255, 255), -1)
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)  # Cambiar a escala de grises la mascara de puntos
    img2 = cv2.bitwise_and(image, image, mask= gray_canvas) # And de la mascara con cuadra y la imagen original
    mean_color = cv2.mean(img2, mask = gray_canvas) # Color extraido

    return mean_color

def delay_s(tiempo):
    T_Inicio = time.time()
    T_Final = time.time()
    Dif = T_Final - T_Inicio
    while(Dif < tiempo ):
        T_Final = time.time()
        Dif = T_Final - T_Inicio
    return


def main():
    # Camara
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    # Datos de motores calibrados
    phi_0 = 228
    phi_180 = 36
    phi_resol = 180.0/(phi_0 - phi_180 + 1)
    phi_step = 1.0  # un paso
    ni_phi = int(round((phi_0 - phi_180 + 1) / phi_step))  # numero de angulos phi

    theta_0 = 245
    theta_90 = 131
    theta_min = 100  # minimo angulo sin que el motor choque con la base
    theta_resol = 90.0/(theta_0-theta_90 + 1)
    theta_step = 1.0  # un paso
    ni_theta = int(round((theta_0 - theta_90 + 1) / theta_step))  # numero de angulos theta

    #Serial COMM
    port = open_port()

    T_Inicio = time.time()
    T_Final = time.time()
    Dif = T_Final - T_Inicio

    # matriz de datos
    # Convertir data1 a nube de puntos
    data1 = np.zeros([0, 3])
    data2 = np.zeros([0, 3])
    color_infra = np.zeros([0, 4])
    step2 = theta_90

    # Cargar polinomio calibrado al infrarrojo
    poly_infra = np.loadtxt('../Procesamiento/Calibracion/Infrarrojo/Polinomio_Ajuste_Infra2.out')
    poly = np.poly1d(poly_infra)

    while (Dif < 1): # Esperar activacion de camara
        T_Final = time.time()
        Dif = T_Final - T_Inicio

    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)  # beep lindo para empezar el movimiento

    while (step2 <= theta_90+39):  # Condicion de finalizacion

        n_canales = detect_data1(port)
        ret, frame = cap.read() # Tomar foto
        data1_in = port.read(2 * n_canales)
        canal_n1 = (2 ** 15) * ord(data1_in[0]) + (2 ** 8) * ord(data1_in[1]) + (2 ** 7) * ord(data1_in[2]) + \
                   ord((data1_in[3]))
        canal_n1 = canal_n1 / 16.0 # promedio de 16 mediciones
        infrarrojo = canal_n1 *3.1/(2**12-1)  # Escalamiento
        if infrarrojo != 0.0:
            infra=poly(infrarrojo) # medida en cm
            if not (infra < 55.0 and infra> 0.0):
                infra = 0

        else:
            infra = 0
        echo = (2 ** 15) * ord(data1_in[4]) + (2 ** 8) * ord(data1_in[5]) + (2 ** 7) * ord(data1_in[6]) + ord(data1_in[7])
        step1 = (2 ** 7) * ord(data1_in[8]) + ord(data1_in[9])
        step2 = (2 ** 7) * ord(data1_in[10]) + ord(data1_in[11])

        phi_prima = step1
        theta_prima = step2
        phi = phi_0-phi_prima
        theta = theta_0 - theta_prima
        if (echo< 28000) :

            dhs = 2
            dys = 13
            r2 = np.sqrt( (infra+dys)**2+dhs**2)
            r1 = np.sqrt( (echo/58.0+dys)**2+dhs**2)  # +0.12#metros
            theta = theta *theta_resol*np.pi / 180.0
            phi = phi *phi_resol*np.pi / 180.0

            x1 = r1 * np.sin(theta) * np.cos(phi)
            y1 = r1 * np.sin(theta) * np.sin(phi)
            z1 = r1 * np.cos(theta)

            x2 = r2 * np.sin(theta) * np.cos(phi)
            y2 = r2 * np.sin(theta) * np.sin(phi)
            z2 = r2 * np.cos(theta)

            data1 = np.append(data1, [[x1, y1, z1]], 0)
            data2 = np.append(data2, [[x2, y2, z2]], 0)

            d_sensor = infra
            centerx, centery, w1, h1 = Pixel_Fun(d_sensor)
            color = mean_color(frame.copy(), centerx, centery, w1, h1 )
            (b, g, r, channel) = color
            color_infra = np.append(color_infra, [[r/255.0, g/255.0, b/255.0, 1]], 0)

            cv2.rectangle(frame, (centerx - w1, centery - h1), (centerx + w1, centery + h1), (255, 0, 0), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, "Distance = {0:0.2f} cm".format(d_sensor), (50, 50), font, 0.8, (0, 255, 0))
            cv2.imshow("Frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            print("distanceU = {0:0.2f}, distanceI = {0:0.2f}, theta = {0:0.2f}, phi = {0:0.2f}".format(echo / 58.0,infra, theta*180.0/np.pi, phi*180/np.pi))



    close_port(port)
    # plt.plot(Time_matrix, Amplitud_matrix)
    # plt.show()
    # Graficar datos


    pointcloud1 = data1
    pointcloud2 = data2
    # print(data1)
    # print("Numero de datos: {}".format(pointcloud1.shape[0]))
    # mlab.figure(bgcolor=(1, 1, 1))
    # mlab.points3d(pointcloud1[:, 0], pointcloud1[:, 1], pointcloud1[:, 2], color=(0, 1, 0), mode='sphere',
    #               scale_factor=0.025)
    # sensor = np.array([[0 ,0, 0]])
    # mlab.points3d(sensor[:, 0], sensor[:, 1], sensor[:, 2], color=(1, 0, 0), mode='sphere',
    #               scale_factor=0.5)

    # mlab.show()

    np.savetxt("adquisicionUltraOso2.out", pointcloud1, fmt='%1.8e')
    np.savetxt("adquisicionInfraOso2.out", pointcloud2, fmt='%1.8e')
    np.savetxt("adquisicionColorOso2.out", color_infra, fmt='%1.8e')


if __name__ == '__main__': main()