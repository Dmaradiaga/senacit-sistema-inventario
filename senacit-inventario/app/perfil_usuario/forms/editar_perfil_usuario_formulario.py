from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SelectField,FileField
from wtforms.validators import DataRequired


class EditarPerfilUsuarioFormulario(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    correo = StringField('Correo', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    numero_identidad = StringField('Número de Identidad',
                                     validators=[DataRequired()])
    contrasena = PasswordField('Contraseña')
    departamento_interno = SelectField('Departamento Interno', 
                               choices=[('',''),('Dirección', 'Dirección'),
                                        ('Subdirección', 'Subdirección'),
                                        ("Bienes","Bienes"),
                                        ('Realidad Virtual y Aumentada', 'Realidad Virtual y Aumentada'),
                                        ('Electrónica y Robótica', 'Electrónica y Robótica'),
                                        ('Impresión 3D', 'Impresión 3D'),
                                        ('Laboratorio de Prótesis', 'Laboratorio de Prótesis'),
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
                                        ('Servicios Generales(Mantenimiento)','Servicios Generales(Mantenimiento)'),
                                        ('Servicios Generales(Aseo)', 'Servicios Generales(Aseo)'),
                                        ('Servicios Generales(Seguridad)', 'Servicios Generales(Seguridad)'),
                                        ('Servicios Generales(Transporte)', 'Servicios Generales(Transporte)')], 
                                        )
    imagen = FileField('Agregar Imagen')
                                                               


