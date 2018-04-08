from flask_wtf import FlaskForm
from wtforms import StringField, TextField, validators, Form
from wtforms.fields.html5 import  EmailField

class PointCloudForm(Form):
    phi_start = StringField('Phi Start', [validators.length(min = 1, max = 4, message='Ingrese un angulo valido!')])
    phi_end = StringField('Phi End', [validators.length(min = 1, max = 4, message='Ingrese un angulo valido!')])
    theta_start = StringField('Theta Start', [validators.length(min = 1, max = 4, message='Ingrese un angulo valido!')])
    theta_end = StringField('Theta End', [validators.length(min = 1, max = 4, message='Ingrese un angulo valido!')])

