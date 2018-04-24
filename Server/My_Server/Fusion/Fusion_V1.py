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
- Caso 1:
    Ambos sensores se encuentran en su rango de medicion, por lo que se toma la medicion
    del infrarrojo al ser mas precisa
- Caso 2:
    Si la medicion dada por el ultrasonido (r1) es menor que 10 cm o mayor a 48 cm, (lo cual indica que el infrarrojo
    esta fuera de alcance, se descarta la medicion del infrarrojo y se toma la del ultrasonido
- Caso 3: si r1 = 0 o r1 > 3m, (ultrasonido fuera de rango) se descartan ambas mediciones

Finalmente, aqui se presenta la implementacion de este algoritmo.
"""


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pcl


# Read a .pcd file, just give the path to the file. The function will return the pointcloud as a numpy array.
def read_pcd_file(input_filename):
    return pcl.load(input_filename).to_array()

def convert_row2spherical(rows):
    x, y , z = rows[0], rows[1], rows[2]
    # descartar data si radio es cero (sensor fuera de rango)
    radius = np.sqrt(x**2 + y**2 +z**2)
    if (radius != 0.0 ):
        theta = np.arccos(z/radius)
        phi = np.arctan2(y, x) # retorna arctan(y/x)
        return theta, phi, radius
    else:
        return 0.0, 0.0, 0.0

def convert2spherical(pointcloud_XYZ):
    pointcloud_ThetaPhiRadius = np.zeros([0, 3]) # Matriz vacia
    for rows in pointcloud_XYZ:
        theta, phi, radius = convert_row2spherical(rows)
        if(theta != 0.0 and phi != 0.0 and radius != 0.0):
            pointcloud_ThetaPhiRadius = np.append(pointcloud_ThetaPhiRadius , [[np.degrees(theta), np.degrees(phi), radius]], 0)


    return pointcloud_ThetaPhiRadius

def find_nearest(array,value, precision): # funcion que retorna el indice del elemento del array mas cercano a cierto valor
    diff = np.abs(array-value)
    idx = (diff.argmin())

    if diff[idx] <= precision: # la diferencia entre el valor a buscar y el hallado es menor que la precision dada
        print("Diferencia = {}".format(diff[idx]))
        return idx # returnar el indice donde ocurre el valor hallado
    else:
        return None # retornar nada


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# pensar concatenacion de enteros y flotantes
pointcloud_Infra = np.loadtxt("A.out")
pointcloud_Ultra = np.loadtxt('adquisicionUltra_Mant.out')

# Conversion coordenadas cartesianas a esfericas
pointcloud_Ultra = convert2spherical(pointcloud_Ultra)
pointcloud_Infra = convert2spherical(pointcloud_Infra)
print(pointcloud_Ultra)


theta_columnI = pointcloud_Infra[:, 0] # tercera columna
theta_columnU = pointcloud_Ultra[:, 0]

theta1 = theta_columnU[0]
match = find_nearest(theta_columnI, theta1, 6)
print(theta_columnI)
print(theta1)

if match == None : # matriz vacia
    print( "Not found")
else:
    print("Valor hallado = {}".format(theta_columnI[match]))



