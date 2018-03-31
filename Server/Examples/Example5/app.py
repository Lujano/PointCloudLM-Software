#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response, request
import time
from forms import PointCloudForm
from camera_opencv import Camera
import time



app = Flask(__name__)
app.secret_key = "Hola"
# Raspberry Pi camera module (requires picamera package)
# get data from DHT sensor
def getDHTdata():
    hum, temp = 1.0, 25.0

    if hum is not None and temp is not None:
        hum = round(hum)
        temp = round(temp, 1)
    return temp, hum


@app.route("/")
def index():
        timeNow = time.asctime(time.localtime(time.time()))
        temp, hum = getDHTdata()

        templateData = {
            'time': timeNow,
            'temp': temp,
            'hum': hum
        }
        return render_template('index.html', **templateData)


@app.route('/HandTracking')
def cam():
    """Video streaming home page."""
    timeNow = time.asctime(time.localtime(time.time()))
    templateData = {
        'time': timeNow
    }
    return render_template('HandTracking.html', **templateData)

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
    app.run(host='127.1.1.1', port=8000, debug=True, threaded=True)
