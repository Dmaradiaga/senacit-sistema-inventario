from flask_wtf import FlaskForm
from wtforms import IntegerField,PasswordField
from wtforms.validators import DataRequired



class FormularioLogin(FlaskForm):
    numero_identidad = IntegerField('Número de Identidad', validators=[DataRequired()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])