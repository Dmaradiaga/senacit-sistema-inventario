
from flask import Blueprint, render_template,request,url_for,redirect,flash,session
from app.db.db import db
from app.documentos.forms.documentos_formulario import DocumentosFormulario
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion,comprobando_sesion_administrador
from app.funciones_ayuda.funciones_ayuda import agregar_documentos_cloudinary, validar_valores_no_vacios,\
eliminar_documento_cloudinary, reenviar_documento_cloudinary, convert_date_to_str, \
verificar_extension_archivo
import json


#Registra el blueprint a la aplicación
documentos_bp = Blueprint('documentos_bp', __name__,
    template_folder='templates',
    static_folder='static')


#Ruta para enviar el documento
@documentos_bp.route('/', methods=["GET", "POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def index():
    form = DocumentosFormulario()
    
    if request.method=="POST":
        enviar_datos = {
            "numero_identidad_remitente":session["codigo_usuario"],
            "numero_identidad_destinatario":form.numero_identidad_destinatario.data,
            "nombre_remitente": session["nombre_usuario"] + " " +session["apellido_usuario"]
        }

        documento  = request.files['documento']

        estado_extension_archivo = verificar_extension_archivo(documento.filename)
        if not estado_extension_archivo:
            flash("Solamente se permiten archivos: PDF", "warning")
            return render_template('enviar_documento.html', form=form)
        
        if documento:
            try:
                        # Subir el documento del formulario a Cloudinary
                        documentos_subidos = agregar_documentos_cloudinary([documento])
                        if documentos_subidos:
                            enviar_datos["url_documento"] = documentos_subidos[0]["secure_url"]
                            enviar_datos["id_url_documento"] = documentos_subidos[0]["public_id"]

            except RuntimeError as e:
                        flash("No se pudo subir el documento. Inténtalo de nuevo", "warning")
                        return render_template('enviar_documento.html', form=form)
        else:
            flash("Debes ingresar un documento","warning")
            return render_template("enviar_documento.html",form=form)
        
        # Validar que se ingresen los datos necesarios
        estado_valores = validar_valores_no_vacios(enviar_datos)
        if estado_valores:
            estado_consulta = db.agregar_documentos(enviar_datos)
            if estado_consulta:
                nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                detalle_actividad = json.dumps(enviar_datos, default=convert_date_to_str)
                    
                db.registrar_accion(session["codigo_usuario"], nombre_usuario, "AGREGAR", "documentos",detalle_actividad)
                
                flash("Se envió el documento correctamente.", "success")
                return redirect(url_for('documentos_bp.index'))
            else:
                flash("No se pudo enviar el documento.", "warning")
                return render_template('enviar_documento.html', form=form)
        else:
            flash("Debes ingresar los datos", "warning")
            return render_template('enviar_documento.html', form=form)
    else:
        return render_template("enviar_documento.html",form=form)



#Ruta para ver el documento
@documentos_bp.route('/ver_documentos', methods=["GET", "POST"])
@comprobando_autorizacion
def ver_documentos():
    try:
            numero_identidad = session["codigo_usuario"]
            print(numero_identidad)
            registros = db.mostrar_documentos(numero_identidad)
            return render_template("ver_documentos.html", registros=registros, numero_identidad=numero_identidad)
    except Exception as e:
            print(f"Ocurrió un error al intentar mostrar los documentos: {e}")
            flash("No se pudo mostrar los documentos", "warning")
            return redirect(url_for("documentos_bp.ver_documentos"))



#Ruta editar el documento
@documentos_bp.route('/reenviar_documento/<int:id_documento>/<id_url_documento>', methods=["GET", "POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def reenviar_documento(id_documento,id_url_documento):
    form = DocumentosFormulario()
    id_documento = id_documento
    id_url_documento = id_url_documento

    
    if request.method=="POST":        
        documento  = request.files['documento']
        
        estado_extension_archivo = verificar_extension_archivo(documento.filename)
        if not estado_extension_archivo:
            flash("Solamente se permiten archivos: PDF", "warning")
            return render_template('reenviar_documento.html', form=form, 
                                id_url_documento=id_url_documento,
                                id_documento=id_documento)
        
        nombre_remitente = session["nombre_usuario"] +" "+session["apellido_usuario"]
        numero_identidad_remitente = session["codigo_usuario"]

        reenviar_datos = {
            "numero_identidad_destinatario":form.numero_identidad_destinatario.data,
            "numero_identidad_remitente": numero_identidad_remitente,
            "nombre_remitente": nombre_remitente
        }

        
        if documento:
            try:
                        # Reenviar el documento del formulario a Cloudinary
                        resultado = reenviar_documento_cloudinary(documento,id_url_documento)
                        if isinstance(resultado, tuple) and len(resultado) == 2:
                            url_documento, estado = resultado
                            if estado:
                                reenviar_datos["url_documento"] = url_documento

            except RuntimeError as e:
                        print(f"ERROR DEBIDO A: {str(e)}")
                        flash("No se pudo subir el documento. Inténtalo de nuevo", "warning")
                        return render_template('reenviar_documento.html', form=form)
        else:
            flash("Debes ingresar un documento","warning")
            return render_template("reenviar_documento.html",form=form)
        

        # Validar que se ingresen los datos necesarios
        estado_valores = validar_valores_no_vacios(reenviar_datos)
        if estado_valores:
            estado_consulta = db.actualizar_documento(reenviar_datos, id_documento)
            if estado_consulta:
                nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                detalle_actividad = json.dumps(reenviar_datos, default=convert_date_to_str)
                    
                db.registrar_accion(session["codigo_usuario"], nombre_usuario, "ACTUALIZAR", "documentos",detalle_actividad)
                flash("Se reenvió el documento correctamente.", "success")
                return redirect(url_for('documentos_bp.ver_documentos'))
            else:
                flash("No se pudo reenviar el documento.", "warning")
                return render_template('reenviar_documento.html', form=form,
                                id_url_documento=id_url_documento,
                                id_documento=id_documento)
        else:
            flash("Debes ingresar los datos", "warning")
            return render_template('reenviar_documento.html', form=form, 
                                   id_url_documento=id_url_documento,
                                    id_documento=id_documento)
    else:
        return render_template("reenviar_documento.html",form=form, 
                               id_url_documento=id_url_documento,
                                id_documento=id_documento)
    


#Ruta eliminar el documento
@documentos_bp.route('/eliminar_documento/<int:id_documento>/<id_url_documento>', methods=["GET", "POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def eliminar_documento(id_documento,id_url_documento):
    if request.method=="POST":
        id_documento = id_documento
        id_url_documento = id_url_documento
        print(id_url_documento)
        resultado = eliminar_documento_cloudinary(id_url_documento)
        if resultado:
            estado = db.eliminar_documento(id_documento)
            if estado:
                nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                detalle_actividad = json.dumps({"ID_DOCUMENTO":id_url_documento}, default=convert_date_to_str)      
                db.registrar_accion(session["codigo_usuario"], nombre_usuario, "ELIMINAR", "documentos",detalle_actividad)
                
                flash("Enhorabuena sea eliminado tu documento","success")
                return redirect(url_for("documentos_bp.ver_documentos"))
            else: 
                  flash("No se pudo eliminar el documento","warning")
                  return redirect(url_for("documentos_bp.ver_documentos"))
        else:
             flash("No se pudo eliminar el documento","warning")
             return redirect(url_for("documentos_bp.ver_documentos"))
    else:
        return redirect(url_for("documentos_bp.ver_documentos"))