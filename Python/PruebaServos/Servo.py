import serial
import time
import winsound

def open_port():
    ser = serial.Serial('COM12', 9600)

    return ser


def close_port(port):
    port.close()


def servo1_send(port, posicion): # el servo que controla phi (plano xy)
    direccion = 1 # conector del driver al que esta conectado el motor
    port.write(bytearray([255, direccion, posicion]))

def servo2_send(port, posicion): # el servo que controla theta (respecto al eje z)
    direccion = 2 # conector del driver al que esta conectado el motor
    port.write(bytearray([255, direccion, posicion]))

def main():

    port = open_port()
    i = 0

    phi_180 =228
    phi_0 = 36

    theta_90 = 245
    theta_45 = 131
    theta_min = 100


    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)
    time_inicial= time.time()
    for step2 in range (theta_90, theta_45, -2):
        servo2_send(port, step2)
        time.sleep(0.1)
        if i == 0:
            for step1 in range(phi_180, phi_0, -2 ):
                servo1_send(port, step1)
                time.sleep(0.25) # delay en segundos
            i = 1
        else:
            for step1 in range(phi_0+1, phi_180, 2):
                servo1_send(port, step1)
                time.sleep(0.25) # delay en segundos
            i = 0



    time_final = (time.time()-time_inicial)/60
    print(time_final)
    close_port(port)
    winsound.Beep(frequency, duration)

if __name__ == "__main__": main()