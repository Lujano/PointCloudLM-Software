from flask_wtf import FlaskForm
from wtforms import StringField, TextField, validators, Form
from wtforms.fields.html5 import  EmailField

class LoginForm(Form):
    username = StringField('Nombre de Usuario', [validators.length(min = 4, max = 25,
                                                                   message='Ingrese un nombre valido!.')])
    email = EmailField("Correo Electronico")
    comment = TextField('Comentario')
