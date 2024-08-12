from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField,\
TextAreaField
from wtforms.validators import DataRequired,NumberRange


class TrasladoFormulario(FlaskForm):
    #nombre_solicitante = StringField('Nombre del Solicitante', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Solicitud', format='%Y-%m-%d', validators=[DataRequired()])
    fecha_final = DateField('Fecha de Finalización', format='%Y-%m-%d', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción',validators=[DataRequired()])
    lugar = StringField('Lugar', validators=[DataRequired()])
    justificacion_traslado = TextAreaField('Justifición Traslado',validators=[DataRequired()])
    numero_identidad_solicitante = IntegerField('Número de Identidad',
                                     validators=[DataRequired(),NumberRange(min=1)])
    serie = StringField('Serie', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    puesto = StringField('Puesto', validators=[DataRequired()])
    numero_inventario = StringField('Número Inventario', validators=[DataRequired()])
    departamentos_internos = SelectField('Departamentos Institución', 
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
    

