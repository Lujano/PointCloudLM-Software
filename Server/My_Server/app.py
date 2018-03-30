#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
from camera_opencv import  Camera
# import camera driver
# if os.environ.get('opencv'):
#     Camera = import_module('camera_' + os.environ['opencv']).Camera
# else:
#     from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


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

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      print("ja")
      return "Fine2" + user
   else:
      user = request.args.get('nm')
      return "OK"

if __name__ == '__main__':
    app.run(host = '127.1.1.1', debug= True, threaded=True, port= 80)
