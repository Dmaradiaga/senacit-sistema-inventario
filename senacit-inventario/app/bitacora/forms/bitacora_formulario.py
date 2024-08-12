from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.validators import DataRequired

class BitacoraFormulario(FlaskForm):
   
    numero_identidad_usuario = IntegerField('Buscar Usuario')
    nombre_tabla = SelectField('Seleccionar Tabla', 
                               choices=[
                                        ('',''),
                                        ('inventario', 'Inventario'),
                                        ('bodega', 'Bodega'),
                                        ('usuarios', 'Usuarios'),
                                        ('documentos', 'Documentos'),
                                        ('solicitud_traslado', 'Solicitud Traslado'),
                                        ('solicitud_descargo', 'Solicitud Descargo')], 
                                        )

    
   
                                                               


