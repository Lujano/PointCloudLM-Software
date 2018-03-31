#!/usr/bin/env python
""" En este codigo se recibe la variable nm desde el cliente mediante metodos POST GET"""
from flask import Flask, render_template, Response
from flask import request
app = Flask(__name__)


@app.route('/ESP8266',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      param1 = request.form['param1']
      param2 = request.form['param2']
      print("Param1 = {}, Param2 = {}".format(param1, param2))
      return "Fine1"

   else:
      param1 = request.args.get('param1')
      param2 = request.args.get('param2')
      ip = request.remote_addr
      print("Param1 = {}, Param2 = {}, ip = {}".format(param1, param2, ip))
      return "Fine2"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug= False, threaded=True, port= 80)

