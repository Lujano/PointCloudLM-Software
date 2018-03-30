import serial
import matplotlib.pyplot as plt
import numpy as np
import time

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
    port = open_port()
    T_Inicio = time.time()
    T_Final = time.time()
    Dif = T_Final-T_Inicio
    print("Start")
    port.write(bytearray([0xf1, 0x05, 0x05]))
    n_canales = detect_data(port)
    print(n_canales)
    data_in = port.read(2*n_canales)
    print(ord(data_in[0]))
    print(ord(data_in[1]))




if __name__ == "__main__": main()