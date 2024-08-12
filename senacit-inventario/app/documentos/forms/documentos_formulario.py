from flask_wtf import FlaskForm
from wtforms import  IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField



class DocumentosFormulario(FlaskForm):
    numero_identidad_destinatario = IntegerField('Número Identidad Destinatario', validators=[DataRequired()])
    documento = FileField('Agregar Documento', validators=[DataRequired()])
                                                               