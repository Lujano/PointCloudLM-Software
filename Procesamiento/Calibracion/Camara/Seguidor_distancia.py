import serial
import numpy as np
import time
import cv2
from Pixel_Fun import Pixel_Fun


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_Distance4_corr.avi',fourcc, 3.0, (640,480))

def open_port():
    ser = serial.Serial('COM12', 115200)

    return ser

def close_port(port):
    port.close()

def detect_data(port):
    #port.reset_input_buffer()
    flag = True

    while flag:
        anuncio = port.read(1)
        anuncio = ord(anuncio[0]) # convertir en entero

        if (anuncio & 0xf0)  == 0xf0:# Se detecta el byte de anuncio de trama
                n_canales = anuncio & 0x0f # Numero de canales a leer
                return  n_canales

def main():
    cap = cv2.VideoCapture(0)
    port = open_port()
    i = 0.00
    y = 0.00
    print("Inicio")
    Amplitud_matrix = np.array([])
    #Time_matrix = np.array([])
    T_Inicio = time.time()
    T_Final = time.time()
    Dif = T_Final-T_Inicio
    # Cargar polinomio calibrado al infrarrojo
    poly_infra = np.loadtxt('../Infrarrojo/Polinomio_Ajuste_Infra2.out')
    poly = np.poly1d(poly_infra)
    i = 0

    while(Dif < 1):
        T_Final = time.time()
        Dif = T_Final - T_Inicio

    T_Inicio = time.time()
    while (Dif < 60):

        n_canales = detect_data(port)
        i +=1
        ret, frame = cap.read()
        data1_in = port.read(2*n_canales)
        canal_n1 = (2 ** 15) * ord(data1_in[0]) + (2 ** 8) * ord(data1_in[1]) + (2 ** 7) * ord(data1_in[2]) + ord(data1_in[3])
        y = canal_n1*3.1/(2**12-1) # Escalamiento, el voltaje de ref de adc es 3.1
        y = y/16
        d_sensor = poly(y)
        print("Distancia cm = {}. {}".format(d_sensor, y))
        centerx, centery, w1, h1 = Pixel_Fun(d_sensor)
        cv2.rectangle(frame, (centerx - w1, centery - h1), (centerx + w1, centery + h1), (255, 0, 0), 3)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,"Distance = {0:0.2f} cm".format(d_sensor),(50, 50), font, 0.8, (0, 255, 0))
        out.write(frame)
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        T_Final = time.time()
        Dif = T_Final - T_Inicio

    cap.release()
    out.release()
    close_port(port)
    cv2.destroyAllWindows()



if __name__ == "__main__": main()