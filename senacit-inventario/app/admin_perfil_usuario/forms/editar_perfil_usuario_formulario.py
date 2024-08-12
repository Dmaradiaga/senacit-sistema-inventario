from flask_wtf import FlaskForm
from wtforms import HiddenField,SelectField, BooleanField
from wtforms.validators import DataRequired

class EditarEstadoUsuarioFormulario(FlaskForm):
    estado_usuario = BooleanField('Estado Usuario', default=False)
    id_usuario = HiddenField('id_usuario')
    es_jefe_departamento = BooleanField('Jefe Departamento', default=False)
    es_tecnico = BooleanField('Es técnico', default=False)
    rol_usuario = SelectField('Rol Usuario', validators=[DataRequired()],
                              choices=[('',''),('Usuario Normal', 'Usuario Normal'), 
                                        ('Administrador', 'Administrador')])
    
   
                                                               


