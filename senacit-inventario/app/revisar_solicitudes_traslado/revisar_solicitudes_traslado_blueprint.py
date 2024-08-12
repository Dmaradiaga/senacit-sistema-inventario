
from flask import Blueprint, render_template,request,url_for,redirect,flash,session
from app.db.db import db
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion, comprobando_sesion_administrador
#from app.funciones_ayuda.funciones_ayuda import validar_valores_no_vacios

revisar_solicitudes_traslado_bp = Blueprint('revisar_solicitudes_traslado_bp', __name__,
    template_folder='templates',
    static_folder='static')


#Ruta principal
@revisar_solicitudes_traslado_bp.route('/', methods=["GET", "POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def index():
        es_jefe_departamento = session['es_jefe_departamento']
        departamento_interno = session['departamento_interno']

        if es_jefe_departamento == 1:
            print("es jefe")
            try:
                if departamento_interno!="Bienes":
                    registros = db.mostrar_solicitudes_traslado_jefe_departamento(departamento_interno)
                    if len(registros)==0:
                        return render_template('revisar_solicitudes_traslado.html')
                                           
                    print(registros)
                    # Si se encuentra el registro, redirigir a la página de edición con los datos del registro
                    return render_template('revisar_solicitudes_traslado.html', 
                                            registros=registros, es_jefe_departamento=True)
                else:
                    registros = db.mostrar_solicitudes_traslado()

                    if len(registros)==0:
                        return render_template('revisar_solicitudes_traslado.html')
                                           
                    print(registros)
                    # Si se encuentra el registro, redirigir a la página de edición con los datos del registro
                    return render_template('revisar_solicitudes_traslado.html', 
                                        registros=registros,aprobar_solicitud=True,es_jefe_departamento=True)
            except Exception as e:
                # Muestra error si  hay
                return render_template("revisar_solicitudes_traslado.html", mensaje_error="Vuelve a intentarlo.")
  
        

#Funcion agrega la firma del jefe de departamento
@revisar_solicitudes_traslado_bp.route('/agregar_firma', methods=["GET","POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def agregar_firma():
    if request.method=="POST":
        id_solicitud_traslado =  request.form.get('id_solicitud_traslado')
        if not session.get("url_firma_imagen"):
            flash("Debes ingresar tu firma",'warning')
            return redirect(url_for('revisar_solicitudes_traslado_bp.index'))
        
        datos_editar = {
            "firma_jefe_departamento": session["url_firma_imagen"]
        }
  
        
        print(datos_editar)
        if id_solicitud_traslado:
           estado_solicitud = db.editar_solicitud_traslado(datos_editar,id_solicitud_traslado)
           if estado_solicitud:
               flash("Enhorabuena se ha agregado tu firma",'success')
               return redirect(url_for('revisar_solicitudes_traslado_bp.index'))
           else:
               flash("Vuelve a intentarlo",'warning')
               return redirect(url_for('revisar_solicitudes_traslado_bp.index'))
        else:
                flash("Vuelve a intentarlo",'warning')
                return redirect(url_for('revisar_solicitudes_traslado_bp.index'))
    else:
        return redirect(url_for('revisar_solicitudes_traslado_bp.index'))
    

#Funcion aprobar el dictamen de la solicitude de desacargo
@revisar_solicitudes_traslado_bp.route('/aprobar_solicitud', methods=["GET","POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def aprobar_solicitud():
    if request.method == "POST":
        id_solicitud_traslado = request.form.get('id_solicitud_traslado')
        if not session.get("url_firma_imagen"):
            flash("Debes ingresar tu firma",'warning')
            return redirect(url_for('revisar_solicitudes_traslado_bp.index'))
        
        registro = db.mostrar_solicitudes_traslado_id_solicitud_traslado(id_solicitud_traslado)
        print(registro)

        datos_editar = {
            "firma_jefe_unidad_bien": session["url_firma_imagen"],
            "estado_solicitud": 1
        }

        firma_jefe_departamento = registro[14]
        firma_responsable_bien = registro[15]

        if firma_jefe_departamento and firma_responsable_bien  and id_solicitud_traslado:
            estado_solicitud = db.aprobar_solicitud_traslado(datos_editar, id_solicitud_traslado)
            if estado_solicitud:
                flash("Enhorabuena, se ha aprobado la solicitud", 'success')
            else:
                flash("No se pudo aprobar la solicitud. Por favor, inténtalo de nuevo.", 'warning')
        else:
            if not id_solicitud_traslado:
                flash("ID de solicitud de descargo no proporcionado.", 'warning')
            else:
                flash("Faltan firmas para poder aprobar la solicitud.", 'warning')
        
        return redirect(url_for('revisar_solicitudes_traslado_bp.index'))
    else:
        return redirect(url_for('revisar_solicitudes_traslado_bp.index'))
    
