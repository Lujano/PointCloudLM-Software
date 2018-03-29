#!/usr/bin/env python

from flask import Flask, render_template, Response
from flask import request
app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/saluda')
def otro_saludo():
    return  'Otro saludito'

@app.route('/params')
def params():
    param = request.args.get('params1', 'no contiene este parametro')
    param2 = request.args.get('params2', 'no contiene este parametro 2')
    return  "el parametro1 es {}, y el 2 es {}".format(param, param2)


@app.route('/lujanoparamas')
@app.route('/lujanoparamas/<name>')
def params2(name = "Lujano"):
    return "Tu nombre es {}".format(name)

if __name__ == '__main__':
    app.run(host = '127.1.1.1', debug= True, threaded=True, port= 80)
