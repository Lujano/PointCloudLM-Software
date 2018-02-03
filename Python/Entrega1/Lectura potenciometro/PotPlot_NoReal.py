import serial
import matplotlib.pyplot as plt
import numpy as np
import time


def open_port():
    ser = serial.Serial('COM12', 115200)

    return ser

def start_protocol(port):
    c = port.read(2)
    try:
        for m in c:
            print(ord(m))

    except:
        print("hola")

def close_port(port):
    port.close()

def detect_data(port):
    #port.reset_input_buffer()
    flag = True

    while flag:
        data_in = port.read(1)
        if ord(data_in[0]) == 241:
            flag = False
            return 1
        elif ord(data_in[0]) == 242:
            flag = False
            return 2







def main():
    plt.axis('auto')
    port = open_port()
    matrix = np.zeros((0, 1))
    t = np.zeros((0, 1))
    i = 0.00
    y = 0.00
    time_ini = time.time()
    time_final= time.time()
    timer = time_final- time_ini
    while(timer < 10):
        n_canales = detect_data(port)
        data_in = port.read(2*n_canales)
        port_value = (2**7)*(ord(data_in[0]) & 31)+ (ord(data_in[1]))
        i += 1
        y = port_value*3.2/(2**12-1)
        matrix = np.append(matrix, [y], )
        t = np.append(t, [i], )
        time_final = time.time()
        timer = time_final - time_ini

    port.close()
    plt.plot(t, matrix)
    plt.show()


if __name__ == "__main__": main()