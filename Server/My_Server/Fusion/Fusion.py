'''
==============
Algoritmo de Fusion Sensorial
==============

Luis Lujano @lujano97
'''

"""
Descripcion:
El objetivo del algoritmo es tomar la mejor medida tomado por los sensores.
Para ello se parte de la medida del ultrasonido para un angulo theta (fijo, ya que se barre en phi) y un angulo phi, 
el cual fue previamente referenciado y calculado mediante:
alpha = np.arctan(dys / (dhs + distance_sensor))
phi= phi_motor-alpha (para el ultrasonido)


Es por ello entonces, una vez que si tienen los dos archivos finales de los datos adquiridos, se ordenan los datos por
el angulo theta.

Es decir, se analizaran las mediciones tomadas por los  dos sensores de distancia para el barrido realizado para un 
angulo theta constante (recuerde que el sistema deja constante el angulo theta, y mueve los motores en la direccion phi, 
hasta que termina el barrido en esa direccion y disminuye el angulo theta para realizar otro barrido hasta llegar al
angulo final theta_end).
Debido a que el ultrasonido empleado presenta dispersion en el pulso enviado para la medicion, en general se tendra una
medida de distancia de una superficie cercana y no de un punto en cuestion, se tomara la medicion del ultrasonido como 
referencia y se examinara en la medicion para le angulo phi mas cercano tomada por el infrarrojo, de tomar la mejor medida.
Para dicho analisis, se presentan tres casos:


"""


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pcl


# Read a .pcd file, just give the path to the file. The function will return the pointcloud as a numpy array.
def read_pcd_file(input_filename):
    return pcl.load(input_filename).to_array()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

pointcloud_Infra = np.loadtxt('../Data/Chiffon/adquisicionInfra_Mant.out')
pointcloud_Ultra = np.loadtxt('../Data/Chiffon/adquisicionUltra_Mant.out')


theta_columnI = pointcloud_Infra[:, 2] # tercera columna
theta_columnU = pointcloud_Ultra[:, 2]

theta1 = theta_columnU[0]
match, = np.where( theta1 < theta_columnI )
print(theta_columnI)
print(theta1)
if match.size == 0 : # matriz vacia
    print( "Not found")
else:
    print(match[1])


