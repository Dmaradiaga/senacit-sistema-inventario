from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SelectField, BooleanField
from wtforms.validators import DataRequired


class AgregarUsuarioFormulario(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    correo = StringField('Correo', validators=[DataRequired()])
    es_jefe_departamento = BooleanField('Jefe Departamento', default=False)
    es_tecnico = BooleanField('Es técnico', default=False)
    apellido = StringField('Apellido', validators=[DataRequired()])
    numero_identidad = StringField('Número de Identidad',
                                     validators=[DataRequired()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    rol_usuario = SelectField('Rol Usuario', validators=[DataRequired()],
                              choices=[('',''),('Usuario Normal', 'Usuario Normal'), 
                                        ('Administrador', 'Administrador')])
    departamento_interno = SelectField('Departamento Interno', 
                               choices=[('',''),('Dirección', 'Dirección'),
                                        ('Subdirección', 'Subdirección'),
                                        ('Realidad Virtual y Aumentada', 'Realidad Virtual y Aumentada'),
                                        ('Electrónica y Robótica', 'Electrónica y Robótica'),
                                        ('Impresión 3D', 'Impresión 3D'),
                                        ('Laboratorio de Prótesis', 'Laboratorio de Prótesis'),
                                        ('Compras', 'Compras'),
                                        ('Bienes', 'Bienes'),
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
                                        ('Servicios Generales(Mantenimiento)','Servicios Generales(Mantenimiento)'),
                                        ('Servicios Generales(Aseo)', 'Servicios Generales(Aseo)'),
                                        ('Servicios Generales(Seguridad)', 'Servicios Generales(Seguridad)'),
                                        ('Servicios Generales(Transporte)', 'Servicios Generales(Transporte)')], 
                                        validators=[DataRequired()])
    
   
                                                               


