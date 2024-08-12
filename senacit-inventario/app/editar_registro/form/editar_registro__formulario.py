from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField,\
TextAreaField
from wtforms.validators import DataRequired,NumberRange,ValidationError
from flask_wtf.file import FileField

        
class EditarFormulario(FlaskForm):
    tipo_documento = StringField('Tipo de Documento', validators=[DataRequired()])
    fecha_documento = DateField('Fecha de Documento', format='%Y-%m-%d')
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
    departamento_interno = SelectField('Departamento Interno', 
                               choices=[('',' '),('Dirección', 'Dirección'),
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
                                        ('Centro de Investigación de Ciudad Blanca',
                                         'Centro de Investigación de Ciudad Blanca'),
                                        ('Espacio Comunitario de Ciencia Tecnología e Innovación UTOPÍA COPINH',
                                         'Espacio Comunitario de Ciencia Tecnología e Innovación UTOPÍA COPINH'),
                                        ('Investigación Científica Desarrollo Tecnologíco','Investigación Científica Desarrollo Tecnologíco'),
                                        ('Servicios Generales(Mantenimiento)','Servicios Generales(Mantenimiento)'),
                                        ('Servicios Generales(Aseo)', 'Servicios Generales(Aseo)'),
                                        ('Servicios Generales(Seguridad)', 'Servicios Generales(Seguridad)'),
                                        ('Servicios Generales(Transporte)', 'Servicios Generales(Transporte)')], 
                                        validators=[DataRequired()])
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
    municipio = SelectField('Municipio  (OPCIONAL)',choices=[('', '')])                                           
    edificio = StringField('Edificio', validators=[DataRequired()])
    piso = StringField('Piso', validators=[DataRequired()])
    oficina = StringField('Oficina', validators=[DataRequired()])
    orden_compra = StringField('Orden de Compra (OPCIONAL)')
    fecha_ingreso = DateField('Fecha de Ingreso', format='%Y-%m-%d')
    #costo_adquisicion = DecimalField('Costo Adquisición', places=2, rounding=decimal.ROUND_HALF_EVEN)
    costo_adquisicion = IntegerField('Costo de Adquisición',
                                     validators=[DataRequired(),NumberRange(min=1)])
    modalidad_contratacion = SelectField('Modalidad de Contratación', 
                                         choices=[('Contrato', 'Contrato'), 
                                                  ('Permanente', 'Permanente')], 
                                                  validators=[DataRequired()])
    #dependencia = StringField('Dependencia', validators=[DataRequired()])
    numero_identidad = StringField('Número de Identidad', validators=[DataRequired()])
    #cantidad_bienes = IntegerField('Cantidad de Bienes', validators=[DataRequired(),NumberRange(min=1)])
    #observacion_bien = TextAreaField('Observaciones del Bien',validators=[DataRequired()])
    fecha_ingreso_bien = DateField('Fecha de Ingreso Bien', format='%Y-%m-%d')
    comentario = TextAreaField('Comentario',validators=[DataRequired()])
    estado_bien = SelectField('Estado del Bien', validators=[DataRequired()],
                                                choices=[('',''),
                                                  ('Nuevo', 'Nuevo'), 
                                                  ('Buen Estado', 'Buen Estado'),
                                                  ('Regular', 'Regular'),
                                                  ('Malo', 'Malo')])
   # estatus_bien = StringField('Estatus del Bien', validators=[DataRequired()])
    imagen = FileField('Seleccionar Imagen')
    fecha_ingreso_bien_temporal = DateField('Fecha de Ingreso Bien', format='%Y-%m-%d')
    fecha_documento_temporal = DateField('Fecha de documento', format='%Y-%m-%d')
    fecha_ingreso_temporal = DateField('Fecha de Ingreso', format='%Y-%m-%d')
                                                               


