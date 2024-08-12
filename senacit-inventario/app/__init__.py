
# Importaciones
from flask import Flask, render_template, session, g
from app.consultas.consultas_blueprint import consultas_bp
from app.agregar_registro.agregar_registro_blueprint import agregar_registro_bp
from app.editar_registro.editar_registro_blueprint import editar_registro_bp
from app.editar_bodega.editar_bodega_blueprint import editar_registro_bodega_bp
from app.bodega_registro.agregar_bodega_blueprint import agregar_bodega_bp
from app.traslado.traslado_blueprint import traslado_bp
from app.descargo.descargo_blueprint import descargo_bp
from app.login.login_blueprint import login_bp
from app.agregar_usuario.agregar_usuario_blueprint import agregar_usuario_bp
from app.documentos.documentos_blueprint import documentos_bp
from app.revisar_solicitudes_descargo.revisar_solicitudes_descargo_blueprint import revisar_solicitudes_descargo_bp
from app.revisar_solicitudes_traslado.revisar_solicitudes_traslado_blueprint import revisar_solicitudes_traslado_bp
from app.perfil_usuario.perfil_usuario_blueprint import perfil_usuario_bp
from app.solicitudes_descargo.solicitudes_descargo_blueprint import solicitudes_descargo_bp
from app.solicitudes_traslado.solicitudes_traslado_blueprint import solicitudes_traslado_bp
from app.reestablecer_contrasena.reestablecer_contrasena_blueprint import reestablecer_contrasena_bp
from app.admin_perfil_usuario.admin_perfil_usuario_blueprint import admin_perfil_usuario_bp
from app.bitacora.bitacora_blueprint import bitacora_bp
import locale
import json
#from app.db.db import db

# Cloudinary
import cloudinary

# Creación de la aplicación Flask
app = Flask(__name__)


# Configuración de Cloudinary
cloudinary.config(
    cloud_name="xxxxx",
    api_key="xxxxxxx",
    api_secret="xxxxxx"
)


# Configuración de la clave secreta en la aplicación
app.config['SECRET_KEY'] = 'senacit-inventario-2024'

#Configuraciones de MailJet
app.config['MAILJET_API_KEY'] = 'xxxxxxx'
app.config['MAILJET_SECRET_KEY'] = 'xxxxxxx'


#Se configura el objeto global g 
@app.before_request
def gobal_app():
    g.app = app




#Registro de Blueprints
app.register_blueprint(consultas_bp, url_prefix="/consultas") # Blueprint de consultas
app.register_blueprint(editar_registro_bp, url_prefix="/editar_inventario") # Blueprint para editar  registros de inventario
app.register_blueprint(editar_registro_bodega_bp,url_prefix='/editar_bodega') # Blueprint para editar registros de bodega
app.register_blueprint(agregar_registro_bp, url_prefix="/agregar") # Blueprint de registro de nuevos datos (ruta principal)
app.register_blueprint(agregar_bodega_bp, url_prefix="/bodega") # Blueprint de registro de bodegas
app.register_blueprint(traslado_bp, url_prefix="/traslado") # Blueprint de gestión de traslados
app.register_blueprint(descargo_bp, url_prefix="/descargo") # Blueprint de gestión de descargos
app.register_blueprint(login_bp, url_prefix="/") # Blueprint de gestión de login
app.register_blueprint(agregar_usuario_bp, url_prefix="/agregar_usuario") # Blueprint de gestión de administración
app.register_blueprint(documentos_bp, url_prefix="/documentos") # Blueprint de gestión de documentos
app.register_blueprint(revisar_solicitudes_descargo_bp, url_prefix="/revisar_solicitudes_descargo") # Blueprint de gestión de solicitudes
app.register_blueprint(revisar_solicitudes_traslado_bp, url_prefix="/revisar_solicitudes_traslado") # Blueprint de gestión de solicitudes
app.register_blueprint(solicitudes_descargo_bp, url_prefix="/solicitudes_descargo") # Blueprint de gestión de mostrar solicitudes descargo
app.register_blueprint(solicitudes_traslado_bp, url_prefix="/solicitudes_traslado") # Blueprint de gestión de mostrar solicitudes traslado
app.register_blueprint(perfil_usuario_bp, url_prefix="/perfil") # Blueprint de gestión de perfil_usuario_bp
app.register_blueprint(admin_perfil_usuario_bp, url_prefix="/usuarios") # Blueprint de gestión de admin_perfil_usuario_bp
app.register_blueprint(reestablecer_contrasena_bp, url_prefix="/reestablecer_contrasena") # Blueprint para restablecer contraseña
app.register_blueprint(bitacora_bp,url_prefix="/bitacora") #BluePrint que maneja la ruta de la bitácora


#Función maneja el error 404 
@app.errorhandler(404)
def not_found(error):
  """
  Manejador de errores para rutas no válidas.
  """
  print(error)
  return render_template("404.html"), 404


#Filtro para formatear el valor del costo de adquisición.
@app.template_filter()
def formatear_lps(valor):
    # Configuración para la localización para el formato de números
    locale.setlocale(locale.LC_ALL, 'es_HN')

    # Convertir el valor al formato decimal
    valor_decimal = valor / 100

    # Formatear el valor para incluir la coma de los miles y el símbolo de Lempiras
    valor_formateado = locale.format_string("%.2f", valor_decimal, grouping=True)

    # Eliminar el símbolo de la moneda 'L'
    valor_formateado = valor_formateado.replace('L', '')

    # Agregar el símbolo de la moneda 'L' al inicio
    valor_formateado = 'L. ' + valor_formateado

    return valor_formateado


#Filtro para formatear  un string a un diccionario
@app.template_filter()
def cadena_diccionario(valor):    
    return json.loads(valor)


#Filtro para formatear  el número de identidad
@app.template_filter()
def formato_numero_identidad(numero_identidad):    
    return f"{numero_identidad[:4]}-{numero_identidad[4:8]}-{numero_identidad[8:]}"



