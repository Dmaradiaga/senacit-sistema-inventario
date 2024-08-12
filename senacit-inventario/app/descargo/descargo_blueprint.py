from flask import Blueprint, render_template,request,url_for,redirect,flash, session
from app.db.db import db
from app.descargo.forms.descargo_formulario import DescargoFormulario
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion
from app.funciones_ayuda.funciones_ayuda import convert_date_to_str, validar_valores_no_vacios
import json


descargo_bp = Blueprint('descargo_bp', __name__,
    template_folder='templates',
    static_folder='static')



#Ruta manejar el formulario de descargo del bien
@descargo_bp.route('/', methods=["GET","POST"])
@comprobando_autorizacion
def index():
    form = DescargoFormulario()
    if request.method == 'POST':
        
        if "url_imagen_descargo" not in session:
            flash('Debes ingresar la imagen del bien.', 'warning')
            return render_template("descargo.html", form=form)
        

        codigo_usuario =  session['codigo_usuario']
        nombre_solicitante = session["nombre_usuario"]+" "+session["apellido_usuario"]
        url_imagen_descargo = session["url_imagen_descargo"]
        firma_responsable_bien = session["url_firma_imagen"]


        solicitud_descargo = {
                "nombre_solicitante": nombre_solicitante,
                "fecha_solicitud": request.form["fecha_solicitud"],
                "lugar": request.form["lugar"].strip(),
                "numero_identidad_solicitante": codigo_usuario,
                "puesto": request.form["puesto"].strip(),
                "marca": request.form["marca"].strip(),
                "serie": request.form["serie"].strip(),
                "numero_inventario": request.form["numero_inventario"].strip(),
                "modelo": request.form["modelo"].strip(),
                "departamento_interno": request.form["departamento_interno"].strip(),
                "imagen":url_imagen_descargo,
                "firma_responsable_bien": firma_responsable_bien
            }

        
        
        estado_valores = validar_valores_no_vacios(solicitud_descargo)
        firma_usuario = session["url_firma_imagen"]
        if firma_usuario:
            if estado_valores:
                try:
                    solicitud_descargo['justificacion_descargo'] = form.justificacion_descargo.data
                    estado = db.agregar_solicitud_descargo(solicitud_descargo)
                    if estado:
                        nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                        detalle_actividad = json.dumps(solicitud_descargo, default=convert_date_to_str)
                            
                        db.registrar_accion(session["codigo_usuario"], nombre_usuario, "AGREGAR", "solicitud_descargo",detalle_actividad)
                        
                        session.pop('url_imagen_descargo', None)
                        flash("Se agregó la solicitud","success")
                        return redirect(url_for('descargo_bp.index'))
                    else:
                        flash("No se pudo agregar la solicitud. Verifique sus datos","warning")
                        return render_template("descargo.html", form=form)
                except Exception as e:
                    # Muestra el error del sino se pudo ingresar el registro
                    print("Error al agregar registro a la base de datos:", e)
                    flash("No se pudó realizar la solicitud.","warning")
                    return render_template("descargo.html", form=form)
            else:
                flash('Debes ingresar todos los datos.', 'warning')
                return render_template("descargo.html", form=form)
        else:
            flash('Debes ingresar tú firma para relizar la solicitud.', 'warning')
            return render_template("descargo.html", form=form)
    else:
        return render_template('descargo.html', form=form)



#Función para rellenar los campos del formulario
@descargo_bp.route('/buscar_datos_numero_inventario', methods=["GET","POST"])
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
                session["url_imagen_descargo"] = imagen_secure_url
                print(imagen_secure_url)
                return ({"estado":True,
                         "modelo":registro[4],
                         "marca":registro[5],
                         "serie":registro[6],
                         "url_imagen": imagen_secure_url
                         })
        else:
             return ({"mensaje":"no_hay_datos"})
    else:
        return redirect(url_for("descargo_bp.index"))   