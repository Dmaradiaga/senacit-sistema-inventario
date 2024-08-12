from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField,\
TextAreaField
from wtforms.validators import DataRequired,NumberRange
from flask_wtf.file import MultipleFileField


class BodegaFormulario(FlaskForm):
    tipo_documento = StringField('Tipo de Documento', validators=[DataRequired()])
    fecha_documento = DateField('Fecha de Documento', format='%Y-%m-%d', validators=[DataRequired()])
    numero_documento = StringField('Número de Documento', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción',validators=[DataRequired()])
    numero_inventario = StringField('Número de Inventario', validators=[DataRequired()])
    modelo = StringField('Modelo', validators=[DataRequired()])
    marca = StringField('Marca', validators=[DataRequired()])
    serie = StringField('Serie', validators=[DataRequired()])
    placa = StringField('Placa (OPCIONAL)')
    motor = StringField('Motor (OPCIONAL)')
    numero_chasis = StringField('Número de Chasis (OPCIONAL)')
    color = StringField('Color', validators=[DataRequired()])
    departamento = SelectField('Departamento (OPCIONAL)', 
                               choices=[('',''),
                                   ('Atlántida', 'Atlántida'),
                                    ('Choluteca', 'Choluteca'),
                                    ('Colón', 'Colón'),
                                    ('Comayagua', 'Comayagua'),
                                    ('Copán', 'Copán'),
                                    ('Cortés', 'Cortés'),
                                    ('El Paraíso', 'El Paraíso'),
                                    ('Francisco Morazán', 'Francisco Morazán'),
                                    ('Gracias a Dios', 'Gracias a Dios'),
                                    ('Intibucá', 'Intibucá'),
                                    ('Islas de la Bahía', 'Islas de la Bahía'),
                                    ('La Paz', 'La Paz'),
                                    ('Lempira', 'Lempira'),
                                    ('Ocotepeque', 'Ocotepeque'),
                                    ('Olancho', 'Olancho'),
                                    ('Santa Bárbara', 'Santa Bárbara'),
                                    ('Valle', 'Valle'),
                                    ('Yoro', 'Yoro')])
    departamento_interno = SelectField('Departamento Interno (OPCIONAL)', 
                               choices=[('',''),
                                         ('Dirección', 'Dirección'),
                                        ('Subdirección', 'Subdirección'),
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
                                        ('Centro de Investigación de Ciudad Blanca,Olancho',
                                         'Centro de Investigación de Ciudad Blanca,Olancho'),
                                        ('Parque Tecnológico, Santa Ana',
                                         'Parque Tecnológico, Santa Ana'),
                                         ('Centro de Investigación Palacios, La Mosquitia',
                                         'Centro de Investigación Palacios, La Mosquitia'),
                                        ('Espacio Comunitario de Ciencia Tecnología e Innovación UTOPÍA COPINH,Intibuca',
                                         'Espacio Comunitario de Ciencia Tecnología e Innovación UTOPÍA COPINH,Intibuca'),
                                        ('Investigación Científica Desarrollo Tecnologíco','Investigación Científica Desarrollo Tecnologíco'),
                                        ('Servicios Generales(Mantenimiento)','Servicios Generales(Mantenimiento)'),
                                        ('Servicios Generales(Aseo)', 'Servicios Generales(Aseo)'),
                                        ('Servicios Generales(Seguridad)', 'Servicios Generales(Seguridad)'),
                                        ('Servicios Generales(Transporte)', 'Servicios Generales(Transporte)')], 
                                        )
    municipio = SelectField('Municipio (OPCIONAL)', choices=[('','')])                                         
    edificio = StringField('Edificio', validators=[DataRequired()])
    piso = StringField('Piso', validators=[DataRequired()])
    oficina = StringField('Oficina', validators=[DataRequired()])
    orden_compra = StringField('Orden de Compra (OPCIONAL)')
    fecha_ingreso = DateField('Fecha de Ingreso', format='%Y-%m-%d', validators=[DataRequired()])
    costo_adquisicion = IntegerField('Costo de Adquisición', validators=[DataRequired(),NumberRange(min=1)])
    modalidad_contratacion = SelectField('Modalidad de Contratación (OPCIONAL)', 
                                        
                                         choices=[('',''),
                                                  ('Contrato', 'Contrato'), 
                                                  ('Permanente', 'Permanente')])
   # dependencia = StringField('Dependencia', validators=[DataRequired()])
    numero_identidad = StringField('Número de Identidad')
   # cantidad_bienes = IntegerField('Cantidad de Bienes', validators=[DataRequired(),NumberRange(min=1)])
   # observacion_bien = TextAreaField('Observaciones del Bien',validators=[DataRequired()])
    fecha_ingreso_bien = DateField('Fecha de Ingreso del Bien', format='%Y-%m-%d', validators=[DataRequired()])
    comentario = TextAreaField('Comentario',validators=[DataRequired()])
    estado_bien = SelectField('Estado del Bien', validators=[DataRequired()],choices=[('',''),
                                                  ('Nuevo', 'Nuevo'), 
                                                  ('Buen Estado', 'Buen Estado'),
                                                  ('Regular', 'Regular'),
                                                  ('Malo', 'Malo')
                                                  ])
    imagen = MultipleFileField('Agregar Imágenes (Máximo 5)', validators=[DataRequired()])
                                                               
