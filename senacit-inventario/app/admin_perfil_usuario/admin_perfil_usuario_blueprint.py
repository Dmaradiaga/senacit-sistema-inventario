from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from app.db.db import db
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion, comprobando_sesion_administrador
from app.admin_perfil_usuario.forms.editar_perfil_usuario_formulario import EditarEstadoUsuarioFormulario
from app.funciones_ayuda.funciones_ayuda import validar_valores_no_vacios, convert_date_to_str
import json


admin_perfil_usuario_bp = Blueprint('admin_perfil_usuario_bp', __name__,
                                    template_folder='templates',
                                    static_folder='static')


@admin_perfil_usuario_bp.route('/', methods=["GET", "POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def buscar_usuario():
    if request.method == "POST":
        numero_identidad = request.form.get('numero_identidad')
        if not numero_identidad:
            flash('El campo número de identidad no puede estar vacío.', "warning")
            return redirect(url_for('admin_perfil_usuario_bp.buscar_usuario'))

        registro = db.mostrar_informacion_usuario(numero_identidad)
        if registro is None:
            flash('No se encontró ningún registro.', "warning")
            return redirect(url_for('admin_perfil_usuario_bp.buscar_usuario'))

        session["info_usuario"] = registro
        return redirect(url_for('admin_perfil_usuario_bp.mostrar_info_usuario'))
    else:
        return render_template("buscar_usuario.html")



@admin_perfil_usuario_bp.route('/mostrar_info_usuario', methods=["GET", "POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def mostrar_info_usuario():
    form = EditarEstadoUsuarioFormulario()
    if request.method=="POST":

        editar_datos = {
        "rol_usuario": form.rol_usuario.data,
        "estado_usuario":0,
        "es_jefe_departamento":0,
        "es_tecnico":0
    }
        
        if form.estado_usuario.data:
                editar_datos["estado_usuario"] = 1
        if form.es_jefe_departamento.data:
                editar_datos["es_jefe_departamento"] = 1
        if form.es_tecnico.data:
                editar_datos["es_tecnico"] = 1

        id_usuario = form.id_usuario.data
        estado_datos = validar_valores_no_vacios(editar_datos)
        if estado_datos:
            estado = db.editar_estado_usuario(editar_datos,id_usuario)
            if estado:
                flash("Enhorabuena se ha actualizado el registro","success")
                return redirect(url_for('admin_perfil_usuario_bp.buscar_usuario'))
            else:
                flash("No se pudo actualizar el registro","warning")
                return redirect(url_for('admin_perfil_usuario_bp.mostrar_info_usuario'))
        else:
            flash("Debes ingresar el rol del usuario","warning")
            return redirect(url_for('admin_perfil_usuario_bp.mostrar_info_usuario'))
            
    else:
        registro = session.get("info_usuario")
        print(registro)
        if not registro:
            flash('No se encontró ningún registro.', "warning")
            return redirect(url_for("admin_perfil_usuario_bp.buscar_usuario"))

        form.rol_usuario.data = registro[2]
        form.estado_usuario.data = registro[3]
        form.es_jefe_departamento.data = registro[4]
        form.es_tecnico.data = registro[5]
        form.id_usuario.data = registro[6]

        return render_template("info_usuario.html", form=form, registro=registro)


#Ruta para eliminar un usuario que no tenga registros
@admin_perfil_usuario_bp.route('/eliminar_usuario/<string:id_usuario>', methods=["GET", "POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def eliminar_usuario(id_usuario):
    id_usuario = id_usuario
    if request.method=="POST":
        if id_usuario:
            estado_consulta = db.eliminar_usuario(id_usuario)
            if estado_consulta is True:
                nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                detalle_actividad = json.dumps({"ID_USUARIO":id_usuario}, default=convert_date_to_str)
                    
                db.registrar_accion(session["codigo_usuario"], nombre_usuario, "ELIMINAR", "usuarios",detalle_actividad)
                flash("Enhorabuena se ha eliminado el usuario.","success")
                return redirect(url_for("admin_perfil_usuario_bp.buscar_usuario"))
            elif estado_consulta==2:
                 flash("El usuario tiene bienes asignados", "warning")
                 return redirect(url_for("admin_perfil_usuario_bp.mostrar_info_usuario"))
            else:
                 flash("No se pudo eliminar. Vuelvelo a intentar.", "warning")
                 return redirect(url_for("admin_perfil_usuario_bp.mostrar_info_usuario"))
        else:
            flash("No se pudo eliminar. Vuelvelo a intentar.","warning")
            return redirect(url_for("admin_perfil_usuario_bp.mostrar_info_usuario"))
    else:
         return redirect(url_for("admin_perfil_usuario_bp.buscar_usuario"))