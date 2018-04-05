import serial


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


def main():
    port = open_port()
    start_protocol(port)
    close_port(port)

if __name__ == "__main__": main()