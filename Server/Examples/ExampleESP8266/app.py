#!/usr/bin/env python
""" En este codigo se recibe la variable nm desde el cliente mediante metodos POST GET"""
from flask import Flask, render_template, Response
from flask import request
import numpy as np

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


@app.route('/ESP8266',methods = ['POST', 'GET'])
def login():
    global ip_ESP8266
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
    if (param1 == "OK"):
        ip_ESP8266 = request.remote_addr
        print("ESP8266 Connected, ip  = {}".format(ip_ESP8266))
        return "OK"
    else:
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
    global ip_ESP8266, ip_client1
    if request.method == 'POST':
        param1 = request.form['param1']
        if (param1 == "WHERE_IS_ESP8266"):
            ip_client1 = request.remote_addr
            if ip_ESP8266 == "0.0.0.0":
                return "ESP8266_Is_No_Connected"
            else:
                print("Handtracking Started from ip  = {}".format(ip_client1))
                return ip_ESP8266
        elif (param1 == "PROCESS_END"):
            print("HandTracking Has Finished")
            bandera = 1
        else:
            return "Negative"
    else:
        param1 = request.args.get('param1')
        if (param1 == "WHERE_IS_ESP8266"):
            ip_client1 = request.remote_addr
            if ip_ESP8266 == "0.0.0.0":
                return "ESP8266_Is_No_Connected"
            else:
                print("Handtracking Started from ip  = {}".format(ip_client1))
                return ip_ESP8266
        elif (param1 == "PROCESS_END"):
                print("HandTracking Has Finished")
                bandera = 1
        else:
                return "Negative"
if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug= False, threaded=True, port= 80)

