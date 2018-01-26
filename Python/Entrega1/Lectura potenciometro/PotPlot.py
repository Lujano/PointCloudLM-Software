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
        data_in = port.read(2)
        if ord(data_in[0]) == 255 and ord(data_in[1]) == 255:
            flag = False







def main():
    plt.axis('auto')
    plt.ylim(0, 5)
    plt.ion()
    port = open_port()
    i = 0.00
    y = 0.00
    while(True):
        detect_data(port)
        data_in = port.read(2)
        port_value = ord(data_in[0])+(2**8)*ord(data_in[1])
        i += 1
        y = port_value*3.2/(2**12-1)
        #plt.scatter(i, y)
        #
        print(y)
        plt.pause(0.000005)


if __name__ == "__main__": main()