from flask import Blueprint, render_template,request,flash, redirect,url_for,session
from app.db.db import db
from app.consultas.forms.consultas_formulario import ConsultasFormulario
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion
from app.funciones_ayuda.funciones_ayuda import validar_valores_no_vacios


mis_solicitudes_bp = Blueprint('mis_solicitudes_bp', __name__,
    template_folder='templates',
    static_folder='static')



# Editar Solicitudes Descargo.
@mis_solicitudes_bp.route('/editar_solicitud_descargo', methods=['GET','POST'])
@comprobando_autorizacion
def editar_solicitud_descargo():
    form = ConsultasFormulario()
    if request.method == "POST":
        # Obtener el código de numero de inventario del formulario
        numero_inventario = request.form['numero_inventario']
        #cabeceras = ["ID", "Tipo de Documento", "Fecha de Adquisición", "Descripción", "..."]
        numero_inventario = numero_inventario.strip()
        if numero_inventario!="":
            try:
                # Buscar el registro en la base de datos utilizando el código de numero de invenetario
                registro = db.mostrar_registro_por_numero_inventario(numero_inventario)
                
                if registro is None:
                    # Si no se encuentran  registros, mostrar un mensaje de error.
                    flash('No se encontró registro','warning')
                    return redirect(url_for('consultas_bp.index'))
                                           
                print(registro)
                # Si se encuentra el registro, redirigir a la página de edición con los datos del registro
                return render_template('mostrar_registro.html', 
                                        registro=registro)
            except Exception as e:
                # Muestra error si no hay
                print("Error al buscar registro por numero de inventario:", e)
                flash('Ocurrió un error al buscar el registro.','warning')
                return redirect(url_for('consultas_bp.index'))
        else:
            flash("Debes ingresar el numero de inventario",'warning')
            return redirect(url_for('consultas_bp.index'))
    else:                        
        return render_template('consultar.html',form=form)


#Ruta muestra solicitud descargo
@mis_solicitudes_bp.route('/',methods=["GET"])
@comprobando_autorizacion
def index():
    return render_template("mis_solicitudes.html")