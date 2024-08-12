from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField,\
TextAreaField
from wtforms.validators import DataRequired,NumberRange


class DescargoFormulario(FlaskForm):
   
    fecha_solicitud = DateField('Fecha de Solicitud', format='%Y-%m-%d', validators=[DataRequired()])
    lugar = StringField('Lugar', validators=[DataRequired()])
    justificacion_descargo = TextAreaField('Justifición del Descargo',validators=[DataRequired()])
    numero_identidad = IntegerField('Número de Identidad',
                                     validators=[DataRequired(),NumberRange(min=1)])
    puesto = StringField('Puesto', validators=[DataRequired()])
    marca = StringField('Marca', validators=[DataRequired()])
    serie = StringField('Serie', validators=[DataRequired()])
    numero_inventario = StringField('Número de Inventario', validators=[DataRequired()])
    modelo = StringField('Modelo', validators=[DataRequired()])
    departamento_interno = SelectField('Departamentos Institución', 
                               choices=[('',''),('Dirección', 'Dirección'),
                                        ('Subdirección', 'Subdirección'),
                                        ('Compras', 'Compras'),
                                        ('Preintervención', 'Preintervención'),
                                        ('Contabilidad', 'Contabilidad'),
                                        ('Presupuesto', 'Presupuesto'),
                                        ('Formación Académica', 'Formación Académica'),
                                        ('Recursos Humanos', 'Recursos Humanos'),
                                        ('Planificación Estratégica', 'Planificación Estratégica'),
                                        ('Infotecnología', 'Infotecnología'),
                                        ('Cooperación Internacional', 'Cooperación Internacional'),
                                        ('Comunicaciones', 'Comunicaciones'),
                                        ('Legal', 'Legal'),
                                        ('Centro de Investigación de Ciudad Blanca,Olancho',
                                         'Centro de Investigación de Ciudad Blanca,Olancho'),
                                        ('Espacio Comunitario de Ciencia Tecnología e Innovación UTOPÍA COPINH,Intibuca',
                                         'Espacio Comunitario de Ciencia Tecnología e Innovación UTOPÍA COPINH,Intibuca'),
                                        ('Investigación Científica Desarrollo Tecnologíco','Investigación Científica Desarrollo Tecnologíco'),
                                        ('Servicios Generales (Mantenimiento)','Servicios Generales (Mantenimiento)'),
                                        ('Servicios Generales (Aseo)', 'Servicios Generales (Aseo)'),
                                        ('Servicios Generales (Seguridad)', 'Servicios Generales (Seguridad)'),
                                        ('Servicios Generales (Transporte)', 'Servicios Generales (Transporte)')], 
                                        validators=[DataRequired()])

    
   
                                                               


