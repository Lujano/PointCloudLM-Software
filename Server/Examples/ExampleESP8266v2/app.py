#!/usr/bin/env python
""" En este codigo se recibe la variable nm desde el cliente mediante metodos POST GET"""


from flask import Flask, render_template, Response, request
import time
from forms import PointCloudForm
from camera_opencv import Camera

# Datos de motores calibrados
phi_0 =228
phi_180 = 36
phi_resol = (phi_0-phi_180+1)/180.0

theta_0 = 245
theta_90 = 131
theta_max = 100  # minimo angulo sin que el motor choque con la base

theta_resol = (theta_0-theta_90 +1)/90.0

#Variables globales
step1 = 0
step2 = 0
Ultra_data = 0
Infra_data = 0
ip_ESP8266 = "0.0.0.0"
ip_client1 = "0.0.0.0"

app = Flask(__name__)

T_Inicio = time.time()
T_Final = time.time()
Dif = T_Final - T_Inicio

band = 0

@app.route("/")
def index():
        return render_template('index.html')
@app.route('/ESP8266', methods = ['POST', 'GET'])
def login():
    global ip_ESP8266, step1, step2
    if request.method == 'POST':
        param1 = request.form['param1']
        param2 = request.form['param2']
        Infra_data = int(param1) # Convertir string a entero
        Ultra_data = int (param2)
        print("Infra = {}, Ultra = {}, ip = {}".format(Infra_data, Ultra_data, ip_ESP8266))
        return "OK"

    else:
        param1 = request.args.get('param1')
        param2 = request.args.get('param2')
        param3 = request.args.get('param3')
        param4 = request.args.get('param4')

        if (param1 == "OK"):  # ESP8266 conectada
            ip_ESP8266 = request.remote_addr
            print("ESP8266 Connected, ip  = {}".format(ip_ESP8266))
            return "OK"
        elif (param1 == "FREERUN"): # Freerun
            command  = "FREERUN"
            return command +"&"+str(step1)+ "&" + str(step2)

        else:  # Pointcloud
             Infra_data = int(param1)/16.0*3.1/(2**12-1)  # Convertir string a entero
             Ultra_data = int(param2)/58.0
             step1 = int(param3)*1.0
             step2 = int(param4)*1.0
             phi_prima = step1
             theta_prima = step2
             phi = phi_0 - phi_prima
             theta = theta_0 - theta_prima
             theta = theta * theta_resol
             phi = phi * phi_resol
             print("phi = {}, theta = {}".format(phi, theta))
             return "OK"

@app.route('/HandTracking',methods = ['POST', 'GET'])
def HandTracking():
    global ip_ESP8266, ip_client1, step1, step2, band
    if request.method == 'POST':
        param1 = request.form['param2']
        param2 = request.form['param2']
        step1 = int(param1)
        step2  = int(param2)
        if (band == 0):
            print("Handtracking Started from ip  = {}".format(ip_client1))
            band = 1
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
        print("Step1 = {}, Step2 = {}".format(step1, step2))
        return "OK"

@app.route('/PointCloud',  methods = ['GET', 'POST'])
def PointCloud():
    """Video streaming home page."""
    PointCloud_Form = PointCloudForm(request.form)
    timeNow = time.asctime(time.localtime(time.time()))

    if request.method == 'POST' and PointCloud_Form.validate():
        print PointCloud_Form.phi_start.data
        print PointCloud_Form.phi_end.data
        print PointCloud_Form.theta_start.data
        print PointCloud_Form.theta_end.data
    return render_template('PointCloud.html', time = timeNow, form = PointCloud_Form)


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)

