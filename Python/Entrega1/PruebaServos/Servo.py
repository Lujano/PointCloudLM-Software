import serial
import time

def open_port():
    ser = serial.Serial('COM12', 9600)

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





def main():

   # port = open_port()
    i = 0.00
    y = 0.00
    while(True):
        i += 1
        print(i)
        time.sleep(0.02) # delay en segundos


if __name__ == "__main__": main()