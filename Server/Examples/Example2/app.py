#!/usr/bin/env python

from flask import Flask, render_template, Response
from flask import request
app = Flask(__name__)


@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return "Fine1"+user
   else:
      user = request.args.get('nm')
      return "Fine2"+user

if __name__ == '__main__':
    app.run(host = '127.1.1.1', debug= True, threaded=True, port= 80)

