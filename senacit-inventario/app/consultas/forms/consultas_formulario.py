from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class ConsultasFormulario(FlaskForm):
    numero_inventario = StringField('Número de Inventario', validators=[DataRequired()])
    numero_inventario_bodega = StringField('Número de Inventario [Bodega]', validators=[DataRequired()])
    numero_identidad = IntegerField('Número de Identidad', validators=[DataRequired()])