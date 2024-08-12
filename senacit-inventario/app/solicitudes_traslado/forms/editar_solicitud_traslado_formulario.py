from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField,\
TextAreaField
from wtforms.validators import DataRequired,NumberRange


class EditarSolicitudTrasladoFormulario(FlaskForm):
    #nombre_solicitante = StringField('Nombre del Solicitante', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', format='%Y-%m-%d')
    fecha_final = DateField('Fecha de Solicitud', format='%Y-%m-%d')
    lugar = StringField('Lugar', validators=[DataRequired()])
    justificacion_traslado = TextAreaField('Justifición de Traslado')
    numero_identidad = IntegerField('Número de Identidad',
                                     validators=[DataRequired(),NumberRange(min=1)])
    puesto = StringField('Puesto', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    serie = StringField('Serie', validators=[DataRequired()])
    descripcion_bien = StringField('Descripción del Bien', validators=[DataRequired()])
    numero_inventario = StringField('Número de Inventario', validators=[DataRequired()])
    #diagnostico = StringField('Diagnóstico', validators=[DataRequired()])
    modelo = StringField('Modelo', validators=[DataRequired()])
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
                                        ('Investigación Científica Desarrollo Tecnologíco','Investigación Científica Desarrollo Tecnologíco'),
                                        ('Servicios Generales (Mantenimiento)','Servicios Generales (Mantenimiento)'),
                                        ('Servicios Generales (Aseo)', 'Servicios Generales (Aseo)'),
                                        ('Servicios Generales (Seguridad)', 'Servicios Generales (Seguridad)'),
                                        ('Servicios Generales (Transporte)', 'Servicios Generales (Transporte)')], 
                                        validators=[DataRequired()])

    
   
                                                               


