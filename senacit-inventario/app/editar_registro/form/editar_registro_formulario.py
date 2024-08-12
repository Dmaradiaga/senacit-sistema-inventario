from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ConsultaFormularioEditar(FlaskForm):
    numero_inventario = StringField('Número de Inventario', validators=[DataRequired()])