
import time
import winsound
import requests
ip_server = "192.168.1.100"
#ip_server = "127.1.1.1"
port_server = "8000"



def delay_s(tiempo):
    T_Inicio = time.time()
    T_Final = time.time()
    Dif = T_Final - T_Inicio
    while(Dif < tiempo ):
        T_Final = time.time()
        Dif = T_Final - T_Inicio
    return

def open_port():
    url_request = "http://"+ip_server+":"+port_server+"/HandTracking?param1=WHERE_IS_ESP8266"
    response =  "Negative"
    ip_ESP8266 = "0.0.0.0"

    while response == "Negative" or response == "ESP8266_Is_No_Connected" :
        try :
            print("Connecting to Server")
            req = requests.get(url_request)
            response = req.content
            if response == "ESP8266_Is_No_Connected" or response == "Negative" :
                print(response)
                delay_s(10.0)
                print("Retrying")
            else:
                ip_ESP8266 = response
                print("HandTracking Started")
        except:
            print("Error connecting to Server")
            delay_s(5.0)
            print("Retrying")

    return ip_ESP8266


def close_port():
    url_request = "http://"+ip_server + ":" + port_server + "/HandTracking?param1=PROCESS_END"
    response = "Negative"

    while response == "Negative":
        try:
            print("Finishing the connection")
            req = requests.get(url_request)
            response = req.content
            if response == "Negative":
                print(response)
                delay_s(10.0)
                print("Retrying")
            else:
                print("Connection Has Finished")
        except:
            print("Error Finishing the connection")
            delay_s(5.0)
            print("Retrying")


    return

def ESP8266_send(ip, step1, step2): # el servo que controla phi (plano xy)
    url_FREERUN = "http://"+ ip +":"+ port_server+ "/HandTracking" + '?step1=' + str(step1) \
                  + '&step2=' + str(step2)

    try:
        T_Inicio = time.time()

        req = requests.get(url_FREERUN)
        response = req.content
        T_Final = time.time()
        Dif = T_Final - T_Inicio
        print(Dif)
        if response != "OK":
            print("Bad response ")
    except:
        print("Error Sending Data")




def main():
    ip_ESP8266 = ip_server

    print(ip_ESP8266)
    # Datos de motores calibrados
    phi_180 = 228
    phi_0 = 36
    phi_resol = (phi_180 - phi_0 + 1) / 180.0

    theta_90 = 245
    theta_0 = 131
    theta_min = 100  # minimo angulo sin que el motor choque con la base
    theta_resol = (theta_90 - theta_0 + 1) / 90.0

    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)  # beep lindo para empezar el movimiento

    time_inicial = time.time()

    i = 0
    step1 = phi_180
    step2 = theta_90
    for step2 in range(theta_0, theta_90, 4):
        ESP8266_send(ip_ESP8266, step1, step2)
        time.sleep(0.1)
        if i == 0:
            for step1 in range(phi_180, phi_0, -2):
                ESP8266_send(ip_ESP8266, step1, step2)
                time.sleep(0.1)  # delay en segundos
            i = 1
        else:
            for step1 in range(phi_0 + 1, phi_180, 2):
                ESP8266_send(ip_ESP8266, step1, step2)
                time.sleep(0.1)  # delay en segundos
            i = 0

    time_final = (time.time() - time_inicial) / 60
    print(time_final)
    #close_port()
    winsound.Beep(frequency, duration)  # beep lindo para terminar el movimiento


if __name__ == "__main__": main()
