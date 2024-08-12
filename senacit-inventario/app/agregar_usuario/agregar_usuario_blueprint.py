from flask import Blueprint, render_template,request,url_for,redirect,flash, session
from app.db.db import db
from app.agregar_usuario.forms.agregar_usuario_formulario import AgregarUsuarioFormulario
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion, comprobando_sesion_administrador
import bcrypt
from app.funciones_ayuda.funciones_ayuda import verificar_correo, validar_numero_identidad,convert_date_to_str
import json



agregar_usuario_bp = Blueprint('agregar_usuario_bp', __name__,
                                        template_folder='templates',
                                        static_folder='static')

# Validador personalizado para verificar si el archivo es una imagen
def verificar_extension_imagen(field):
        extension = field.split('.')[-1].lower()
        print(extension)
        if extension not in ['jpg', 'jpeg', 'png']:
            return False
        else:
             return True
        
#Función para validar espacios en blanco
def validar_valores_no_vacios(diccionario):
    # Verificar que cada valor del diccionario no esté vacío si es una cadena
    for valor in diccionario.values():
        if isinstance(valor, str) and not valor.strip():
            return False
    return True


#Fución para encriptar la contraseña del usuario
def encriptar_contrasena(contrasena):
  # Se genera una cadena aleatoria
  salt = bcrypt.gensalt()

  # Se encripta la contraseña con la cadena aleatoria
  contrasena_encriptada = bcrypt.hashpw(contrasena.encode('utf-8'), salt).decode('utf-8')

  return contrasena_encriptada


#Ruta agregar registro
@agregar_usuario_bp.route('/', methods=["GET", "POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def index():
    form = AgregarUsuarioFormulario()
    if request.method=="POST":
        datos_usuario = {
            "contrasena": form.contrasena.data.strip(),
            "numero_identidad": form.numero_identidad.data.strip(),
            "nombre": form.nombre.data.strip(),
            "apellido": form.apellido.data.strip(),
            "rol_usuario": form.rol_usuario.data,
            "departamento_interno": form.departamento_interno.data
        }

        correo = form.correo.data.strip()
        if verificar_correo(correo):
            datos_usuario["correo"] = correo
        else:
            flash("Ingresa un correo válido", "warning")
            return render_template('agregar_usuario.html',form=form)   
         
        if  form.es_jefe_departamento.data==True:
            datos_usuario["es_jefe_departamento"] = 1
        else:
            datos_usuario["es_jefe_departamento"] = 0

        if  form.es_tecnico.data==True:
            datos_usuario["es_tecnico"] = 1
        else:
            datos_usuario["es_tecnico"] = 0

        estado_valores = validar_valores_no_vacios(datos_usuario)
        contrasena_encriptada = encriptar_contrasena(datos_usuario["contrasena"])
        datos_usuario["contrasena"] = contrasena_encriptada

        if estado_valores:
            print(datos_usuario)
            es_numero_identidad = validar_numero_identidad(datos_usuario["numero_identidad"])
            
            if not es_numero_identidad:
                flash("Debes ingresar un número de identidad válido","warning")
                return render_template('agregar_usuario.html',form=form)
            
            estado_consulta = db.agregar_usuario(datos_usuario)

            if estado_consulta==True:
                nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                detalle_actividad = json.dumps(datos_usuario, default=convert_date_to_str)
                    
                db.registrar_accion(session["codigo_usuario"], nombre_usuario, "AGREGAR", "usuarios",detalle_actividad)
                
                flash("El usuario se agregó correctamente.","success")
                return redirect(url_for('agregar_usuario_bp.index'))
            else:
                if estado_consulta=="clave_duplicada":
                    flash("El usuario ya fue registrado.","warning")
                    return render_template('agregar_usuario.html',form=form)
                    #return redirect(url_for('agregar_usuario_bp.index'))
                else:
                    flash("No se pudo agregar el usuario.","warning")
                    return render_template('agregar_usuario.html',form=form)
                    #return redirect(url_for('agregar_usuario_bp.index'))
        else:
            flash("Debes ingresar los datos","warning")
            return render_template('agregar_usuario.html',form=form)
            #return redirect(url_for('agregar_usuario_bp.index'))
    return render_template('agregar_usuario.html',form=form)
