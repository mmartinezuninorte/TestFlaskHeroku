from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length

class Login(FlaskForm):
    email = EmailField ('Correo :', validators=[
        DataRequired(message="Informacion indispensable")
    ])
    password = PasswordField ('Contraseña: ', validators=[
        DataRequired(message="Informacion indispensable")
    ])
    ingresar = SubmitField ('Iniciar Sesion')

class Registro(FlaskForm):
    name= StringField ('Nombre :', validators=[
        DataRequired(message="Informacion indispensable"),
        Length(min=3, message='Supere los 3 caracteres')
    ])
    username= StringField ('Username :', validators=[
        DataRequired(message="Informacion indispensable"),
        Length(min=3, message='Supere los 3 caracteres')
    ])
    email= EmailField ('Correo :', validators=[
        DataRequired(message="Informacion indispensable")
    ])
    password = PasswordField ('Contraseña: ', validators=[
        DataRequired(message="Informacion indispensable")
    ])
    registrar = SubmitField ('Registrar usuario')