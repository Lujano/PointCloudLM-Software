#!/usr/bin/env python
"""Para probar example 5 server de esp8266 arduino"""

import urllib2
import urllib
# response = urllib2.urlopen('http://127.1.1.1:80/params?params1=Jorge')
# print response.info()
# html = response.read()
# print html
# response.close()
# Datos de motores calibrados
phi_0 =228
phi_180 = 36
phi_resol = (phi_180-phi_0+1)/180.0

theta_0 = 245
theta_90 = 131
theta_max = 100  # minimo angulo sin que el motor choque con la base

theta_resol = (theta_90-theta_0 +1)/90.0

# Trama FREERUN
step1 = phi_0 # Step inicial
step2 = theta_90
phi_start = phi_0-75# 70 grados
phi_end = phi_0-118 # 110 grados
theta_start = theta_90 # 90 grados
theta_end = theta_90+40 # 80 grados

command = 0
url_FREERUN = "http://192.168.1.102:8000/Server"+'?step1='+ str(step1)\
              +'&step2='+str(step2)+'&commad=OK'
url_POINTCLOUD ="http://192.168.1.102:8000/Server"+'?phi_start='+ str(phi_start)\
                +'&phi_end='+str(phi_end)+'&commad=POINTCLOUD'+'&theta_start=' + str(theta_start)\
                +'&theta_end='+str(theta_end)
print("start")
req = urllib2.Request(url_FREERUN)
res = urllib2.urlopen(req)
data = res.read()
print(data)
print("end")
res.close()