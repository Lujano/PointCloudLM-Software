import numpy as np

pixel_x = np.loadtxt('../Procesamiento/Calibracion/Camara/Px.out')  # Polinomio calibrado para pixel x
px = np.poly1d(pixel_x)  # Funcion polinomica
pixel_y = np.loadtxt('../Procesamiento/Calibracion/Camara/Py.out')  # Polinomio calibrado para pixel y
py = np.poly1d(pixel_y)  # Funcion polinomica

def Pixel_Fun(distance_cm):
    """ Funcion que retorna la posicion en pixeles del punto a medir
    y el ancho y alto de la ventana a utilizar para extraer el calor"""


    if distance_cm <2.0:  #(cm)
        return 50, 370, 30, 30
    elif distance_cm >= 2.0 and distance_cm <10.0:
        return int(px(distance_cm)), int(py(distance_cm)), 30, 30
    elif distance_cm >= 10.0 and distance_cm <16.0:
        return int(px(distance_cm)), int(py(distance_cm)), 20, 20
    elif distance_cm >= 16.0 and distance_cm <24.0:
        return int(px(distance_cm)), int(py(distance_cm)), 15, 15

    elif distance_cm > 24.0 and distance_cm <35.0:
        return 305, 265, 15, 15
    else:       # Ventana mas peque#a, objetivo mas lejano
        return 315, 258, 5, 5


