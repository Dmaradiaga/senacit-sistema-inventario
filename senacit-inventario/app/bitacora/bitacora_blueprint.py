from flask import Blueprint, render_template,request,url_for,redirect,flash, session
from app.db.db import db
from app.bitacora.forms.bitacora_formulario import BitacoraFormulario
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion, comprobando_sesion_administrador
#from app.funciones_ayuda.funciones_ayuda import validar_valores_no_vacios


bitacora_bp = Blueprint('bitacora_bp', __name__,
    template_folder='templates',
    static_folder='static')


#Ruta principal del blueprint
@bitacora_bp.route('/', methods=["GET","POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def index():
    form = BitacoraFormulario()
    registros = db.mostrar_datos_bitacora()

    if request.method=="POST":
        nombre_tabla = form.nombre_tabla.data
        numero_identidad_usuario = form.numero_identidad_usuario.data

        if numero_identidad_usuario!="" or  nombre_tabla!="":
            if nombre_tabla and numero_identidad_usuario:
                registros = db.buscar_datos_bitacora(nombre_tabla,numero_identidad_usuario)
                print(registros)
            elif numero_identidad_usuario:
                registros = db.buscar_datos_bitacora_por_usuario(numero_identidad_usuario)
            elif nombre_tabla:
                registros = db.buscar_datos_bitacora_por_tabla(nombre_tabla)
                print(registros)
            return render_template("bitacora.html",form=form, registros=registros)
        else:
            flash("Debes ingresar los datos", "warning")
            return render_template("bitacora.html",form=form, registros=registros)
        
    else:
        print(registros)
        return render_template("bitacora.html",form=form, registros=registros)




    

