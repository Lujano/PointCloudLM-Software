#!/usr/bin/env python
""" En este codigo se recibe la variable nm desde el cliente mediante metodos POST GET"""


from flask import Flask, render_template, Response, request
import time
from forms import PointCloudForm
from camera_opencv import Camera
import cv2

# Datos de motores calibrados
phi_0 = 228
phi_180 = 36
phi_resol = (phi_0-phi_180+1)/180.0

theta_0 = 245
theta_90 = 131
theta_max = 100  # minimo angulo sin que el motor choque con la base
theta_resol = (theta_0-theta_90 +1)/90.0 # pasos por angulo

#Variables globales
step1 = phi_0-97
step2 = theta_90+57
phi_start = phi_0
phi_end = phi_180
theta_start = theta_0
theta_end = theta_90
Ultra_data = 0
Infra_data = 0
ip_ESP8266 = "0.0.0.0"
ip_client1 = "0.0.0.0"
system_state = "ESP" # Sistema empieza en estado FREERUN


app = Flask(__name__)

T_Inicio = time.time()
T_Final = time.time()
Dif = T_Final - T_Inicio

band = 0

camera = cv2.VideoCapture(0)

def gen():
    """Video streaming generator function."""
    while True:
        time.sleep(0.01)
        _, img = camera.read()


        frame_encode = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_encode + b'\r\n')

@app.route("/")
def index():
    global system_state
    return render_template('index.html')

@app.route('/ESP8266', methods = ['POST', 'GET'])
def login():
    global ip_ESP8266, step1, step2, system_state, phi_start, phi_end, theta_start, theta_end, phi_0, theta_0, theta_resol, phi_resol
    if request.method == 'POST':
        param1 = request.form['param1']
        param2 = request.form['param2']
        Infra_data = int(param1) # Convertir string a entero
        Ultra_data = int (param2)
        print("Infra = {}, Ultra = {}, ip = {}".format(Infra_data, Ultra_data, ip_ESP8266))
        return "OK"

    else:
        ESPstate = request.args.get('ESPstate')
        param1 = request.args.get('param1')
        param2 = request.args.get('param2')
        param3 = request.args.get('param3')
        param4 = request.args.get('param4')
        if (system_state == "ESP"): # Esperando que se conecta la ESP
            if (ESPstate == "OK"):  # ESP8266 conectada
                ip_ESP8266 = request.remote_addr
                print("ESP8266 Connected, ip  = {}".format(ip_ESP8266))
                system_state = "FREERUN"
                return "OK"
            else:
                command = "RESET"
                system_state = "ESP"
                return command
        elif( system_state == "FREERUN" ):
            if(ESPstate == "FREERUN"): # Freerun
                command  = "FREERUN"
                return command +"&"+str(step1)+ "&" + str(step2)
            elif (ESPstate == "POINTCLOUD"): # cambiar a estado FREERUN el sistema
                step1 = phi_0 - 97  # Reiniciar posicion de los motores
                step2 = theta_90 + 57
                command  = "FREERUN"
                return command +"&"+str(step1)+ "&" + str(step2)
            elif (ESPstate == "OK"):
                command = "RESET"
                system_state = "ESP"
                return  command

        if (system_state == "POINTCLOUD"): #  si un cliente hizo la peticion de pointcloud
            if (ESPstate == "POINTCLOUD"):  #  si la ESP esta Pointcloud
                if (param1 != "FINISH" and param2 != "FINISH"): # si la nube de punto no ha terminado
                     Infra_data = int(param1)/16.0*3.1/(2**12-1)  # Convertir string a entero
                     Ultra_data = int(param2)/58.0
                     step11 = int(param3)*1.0
                     step22 = int(param4)*1.0
                     phi_prima = step11
                     theta_prima = step22
                     phi = phi_0 - phi_prima
                     theta = theta_0 - theta_prima
                     theta = theta / theta_resol
                     phi = phi/ phi_resol
                     print("Ultra_data = {0:0.2f}, Infra_data = {1:0.2f}, phi = {2:0.2f}, theta = {3:0.2f}".format(
                     Ultra_data, Infra_data, phi, theta))
                     return "OK"
                else: # PoinCloud terminada
                    step1 = phi_0 - 97  # reiniciar posicion de motor
                    step2 = theta_90 + 57
                    command = "FREERUN"
                    system_state = "FREERUN"
                    return command + "&" + str(step1) + "&" + str(step2)



            elif (ESPstate == "FREERUN"):
                command = "POINTCLOUD"
                return  command + "&" + str(phi_start) +"&"+str(phi_end)+"&"+str(theta_start) + "&"+str(theta_end)

            elif (ESPstate == "OK"):
                command = "RESET"
                system_state = "ESP"
                return command

            # si la ESP esta en FREERUN


@app.route('/HandTracking',methods = ['POST', 'GET'])
def HandTracking():
    global ip_ESP8266, ip_client1, step1, step2, band, system_state
    if request.method == 'POST':
        param1 = request.form['param2']
        param2 = request.form['param2']
        step1 = int(param1)
        step2  = int(param2)
        if (band == 0):
            print("Handtracking Started from ip  = {}".format(ip_client1))
            band = 1
        system_state = "FREERUN"
        return "OK"

    else:
        param1 = request.args.get('step1')
        param2 = request.args.get('step2')
        step1 = int(param1)
        step2  = int(param2)
        if (band == 0):
            ip_client1 = request.remote_addr
            print("Handtracking Started from ip  = {}".format(ip_client1))
            band = 1
        system_state = "FREERUN"
        print("Step1 = {}, Step2 = {}".format(step1, step2))
        return "OK"

@app.route('/PointCloud/Processing',  methods = ['GET', 'POST'])
def PointCloud():
    """Video streaming home page."""
    timeNow = time.asctime(time.localtime(time.time()))
    return render_template('PointCloudProcessing.html', time = timeNow)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/PointCloud/Form',  methods = ['GET', 'POST'])
def Form():
    global ip_ESP8266, step1, step2, system_state, phi_start, phi_end, theta_start, theta_end, phi_resol, theta_resol,phi_0, theta_0
    global system_state
    """Video streaming home page."""

    PointCloud_Form = PointCloudForm(request.form)
    timeNow = time.asctime(time.localtime(time.time()))



    if request.method == 'POST' and PointCloud_Form.validate():
        phi_start = phi_0 - int(round(int(PointCloud_Form.phi_start.data)*phi_resol))
        phi_end = phi_0 - int(round(int(PointCloud_Form.phi_end.data) * phi_resol))
        theta_start = theta_0 - int(round(int(PointCloud_Form.theta_start.data) * theta_resol))
        theta_end = theta_0- int(round(int(PointCloud_Form.theta_end.data)*theta_resol))

        print("PointCloudLM started")
        print("Phi_start = {}, Phi_end = {}, Theta_start = {}, Theta_end = {}".format(phi_start, phi_end, theta_start,
                                                                                      theta_end))
        system_state = "POINTCLOUD"
        return render_template('PointCloudProcessing.html', time=timeNow)
    return render_template('PointCloudForm.html', time = timeNow, form = PointCloud_Form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)

