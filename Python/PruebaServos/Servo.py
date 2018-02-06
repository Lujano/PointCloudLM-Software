import serial
import time

def open_port():
    ser = serial.Serial('COM12', 9600)

    return ser


def close_port(port):
    port.close()


def servo1_send(port, posicion): # el servo que controla phi (plano xy)
    direccion = 0 # conector del driver al que esta conectado el motor
    port.write(bytes(255, direccion, posicion))

def servo2_send(port, posicion): # el servo que controla theta (respecto al eje z)
    direccion = 1 # conector del driver al que esta conectado el motor
    port.write(bytes(255, direccion, posicion))

def main():

    port = open_port()
    i = 0
    for step1 in range (0, 254):
        servo1_send(port, step1)
        if i == 0:
            for step2 in range(100, 254, 2 ):
                servo2_send(port, step2)
                time.sleep(0.03) # delay en segundos
            i == 1
        else:
            for step2 in range(253, 100, -2 ):
                servo2_send(port, step2)
                time.sleep(0.03) # delay en segundos
            i == 0

    close_port(port)



if __name__ == "__main__": main()