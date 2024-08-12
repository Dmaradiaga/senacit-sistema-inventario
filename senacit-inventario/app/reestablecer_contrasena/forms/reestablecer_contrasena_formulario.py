from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired



class ReestablecerContrasenaFormulario(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    verificar_contrasena = PasswordField('Verificar Contraseña', validators=[DataRequired()])
    correo = StringField('Correo', validators=[DataRequired()])
    