from flask import Blueprint, render_template,request, flash,redirect,url_for,session
from app.db.db import db
from app.traslado.forms.traslado_formulario import TrasladoFormulario
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion
from app.funciones_ayuda.funciones_ayuda import validar_valores_no_vacios, convert_date_to_str
import json
from datetime import datetime
import locale

# Configurar el locale para obtener los nombres de los días en español
#locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_TIME, 'es_ES')


traslado_bp = Blueprint('traslado_bp', __name__,
    template_folder='templates',
    static_folder='static')
 

#Ruta agregar registro en bodega
@traslado_bp.route('/', methods=["GET", "POST"])
@comprobando_autorizacion
def index():
    form = TrasladoFormulario()
    if request.method == 'POST':

        if "url_imagen_traslado" not in session:
            flash('Debes ingresar la imagen del bien.', 'warning')
            return render_template("traslado.html", form=form)
        

        codigo_usuario =  session['codigo_usuario']
        departamento_interno = session['departamento_interno']
        nombre_solicitante = session["nombre_usuario"]+" "+session["apellido_usuario"]
        url_imagen_traslado = session["url_imagen_traslado"]
        firma_responsable_bien = session["url_firma_imagen"]


        solicitud_traslado = {
                "nombre_solicitante": nombre_solicitante,
                "fecha_solicitud": request.form["fecha_inicio"],
                "fecha_inicio": request.form["fecha_inicio"],
                "fecha_final": request.form["fecha_final"],
                "lugar": request.form["lugar"].strip(),
                "numero_identidad_solicitante": codigo_usuario,
                "puesto": request.form["puesto"].strip(),
                "serie": request.form["serie"].strip(),
                "color": request.form["color"].strip(),
                "numero_inventario": request.form["numero_inventario"].strip(),
                "descripcion": request.form["descripcion"].strip(),
                "departamento_interno": departamento_interno,
                "imagen":url_imagen_traslado,
                "firma_responsable_bien": firma_responsable_bien
            }

        estado_valores = validar_valores_no_vacios(solicitud_traslado)
        firma_usuario = session["url_firma_imagen"]
        if firma_usuario:
            if estado_valores:
                try:

                    # Convertir las fechas a objetos datetime
                    inicio = datetime.strptime(solicitud_traslado['fecha_inicio'], '%Y-%m-%d')
                    fin = datetime.strptime(solicitud_traslado['fecha_final'], '%Y-%m-%d')
                    
                    # Calcular la duración en días
                    duracion = (fin - inicio).days + 1
                    
                    # Formato de las fechas para la respuesta
                    inicio_str = inicio.strftime("%d de %B de %Y")
                    fin_str = fin.strftime("%d de %B de %Y")
                    
                    # Crear el mensaje detallado
                    mensaje = f"El traslado se hará del {inicio_str} al {fin_str} ({duracion} días en total)."
                    solicitud_traslado['mensaje'] = mensaje

                    print(solicitud_traslado)
                    solicitud_traslado['justificacion_traslado'] = request.form["justificacion_traslado"]
                    
                    estado = db.agregar_solicitud_traslado(solicitud_traslado)
                    if estado:
                        nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                        detalle_actividad = json.dumps(solicitud_traslado, default=convert_date_to_str)   
                        db.registrar_accion(session["codigo_usuario"], nombre_usuario, "AGREGAR", "solicitud_traslado",detalle_actividad)
                        
                        session.pop('url_imagen_traslado', None)
                        flash("Se agregó la solicitud","success")
                        return redirect(url_for('traslado_bp.index'))
                    else:
                        flash("No se pudo agregar la solicitud. Verifique sus datos","warning")
                        return render_template('traslado.html', form=form)
                except Exception as e:
                    # Muestra el error del sino se pudo ingresar el registro
                    print("Error al agregar registro a la base de datos:", e)
                    flash("No se pudó realizar la solicitud.","warning")
                    return render_template('traslado.html', form=form)
            else:
                    flash('Debes ingresar todos los datos.','warning')
                    return render_template('traslado.html',  form=form)
        else:
            flash('Debes ingresar tú firma para relizar la solicitud.', 'warning')
            return render_template("traslado.html", form=form)                      
    else:
        return render_template('traslado.html', form=form)


#Función para rellenar los campos del formulario
@traslado_bp.route('/buscar_datos_numero_inventario', methods=["GET","POST"])
@comprobando_autorizacion
def buscar_datos_numero_inventario():
    if request.method=="POST":
        numero_inventario = request.form['numero_inventario'].strip()
        if numero_inventario!="":
            registro = db.mostrar_registro_por_numero_inventario(numero_inventario)
            if registro is None:
                return ({"estado":False})
            else:
                print(registro)
                imagen_secure_url = json.loads(registro[28])[0]['secure_url']
                session["url_imagen_traslado"] = imagen_secure_url
                print(imagen_secure_url)
                return ({"estado":True,
                         "color":registro[10],
                         "serie":registro[6],
                         "url_imagen":imagen_secure_url
                         })
        else:
             return ({"mensaje":"no_hay_datos"})
    else:
        return redirect(url_for("traslado_bp.index"))  