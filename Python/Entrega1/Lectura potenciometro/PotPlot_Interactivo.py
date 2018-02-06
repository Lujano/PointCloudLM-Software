import serial
import matplotlib.pyplot as plt


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
        anuncio = port.read(1)
        anuncio = ord(anuncio[0]) # convertir en entero

        if (anuncio & 0xf0)  == 0xf0 # Se detecta el byte de anuncio de trama
                n_canales = anuncio & 0x0f # Numero de canales a leer
                return  n_canales

def main():
    plt.axis('auto')
    plt.ylim(0, 5)
    plt.ion()
    port = open_port()
    i = 0.00
    y = 0.00
    while(True):
        n_canales = detect_data(port)
        data_in = port.read(2*n_canales)
        canal_n1 = (2**7)*ord(data_in[0])+ord(data_in[1])
        y = canal_n1*3.2/(2**12-1) # Escalamiento
        i += 1
        plt.scatter(i, y)
        plt.pause(0.000005)


if __name__ == "__main__": main()