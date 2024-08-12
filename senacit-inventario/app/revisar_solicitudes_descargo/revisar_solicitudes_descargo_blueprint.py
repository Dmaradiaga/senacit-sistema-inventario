
from flask import Blueprint, render_template,request,url_for,redirect,flash,session
from app.db.db import db
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion, \
 es_tecnico
from app.funciones_ayuda.funciones_ayuda import validar_valores_no_vacios
import textwrap

revisar_solicitudes_descargo_bp = Blueprint('revisar_solicitudes_descargo_bp', __name__,
    template_folder='templates',
    static_folder='static')


#Ruta principal
@revisar_solicitudes_descargo_bp.route('/', methods=["GET", "POST"])
@es_tecnico
@comprobando_autorizacion
def index():
        es_jefe_departamento = session['es_jefe_departamento']
        departamento_interno = session['departamento_interno']
        es_tecnico = session['es_tecnico']

        if es_jefe_departamento == 1:
            print("es jefe")
            try:
                if departamento_interno!="Bienes":
                    registros = db.mostrar_solicitudes_descargo_jefe_departamento(departamento_interno)
                    if registros is None:
                        return render_template('revisar_solicitudes_descargo.html')
                                           
                    print(registros)
                    # Si se encuentra el registro, redirigir a la página de edición con los datos del registro
                    return render_template('revisar_solicitudes_descargo.html', 
                                            registros=registros, es_jefe_departamento=True)
                else:
                    registros = db.mostrar_solicitudes_descargo()

                    if registros is None:
                        return render_template('revisar_solicitudes_descargo.html')
                                           
                    print(registros)
                    # Si se encuentra el registro, redirigir a la página de edición con los datos del registro
                    return render_template('revisar_solicitudes_descargo.html', 
                                        registros=registros,aprobar_solicitud=True,es_jefe_departamento_bienes=True)
            except Exception as e:
                # Muestra error si  hay
                return render_template("revisar_solicitudes_descargo.html", mensaje_error="Vuelve a intentarlo.")
  
        elif es_tecnico==1:
            try:
                # Buscar solicitudes de descargo en la tabla solicitud_descargo
                registros = db.mostrar_solicitudes_descargo_tenico_departamento(departamento_interno)
                
                if len(registros)==0:
                    return render_template('revisar_solicitudes_descargo.html')
                                                                        
                print(registros)
                # Si se encuentra el registro, redirigir a la página de edición con los datos del registro
                return render_template('revisar_solicitudes_descargo.html', 
                                        registros=registros, generar_dictamen=True)
            except Exception as e:
                # Muestra error si no hay
                return render_template("revisar_solicitudes_descargo.html", mensaje_error="Vuelve a intentarlo.")
        

#Funcion agrega la firma del jefe de departamento
@revisar_solicitudes_descargo_bp.route('/agregar_firma', methods=["GET","POST"])
@es_tecnico
@comprobando_autorizacion
def agregar_firma():
    if request.method=="POST":
        id_solicitud_descargo =  request.form.get('id_solicitud_descargo')
        if not session.get("url_firma_imagen"):
            flash("Debes ingresar tu firma",'warning')
            return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
        
        datos_editar = {
            "firma_jefe_departamento": session["url_firma_imagen"]
        }

        if id_solicitud_descargo:
           estado_solicitud = db.editar_solicitud_descargo(datos_editar,id_solicitud_descargo)
           if estado_solicitud:
               flash("Enhorabuena se ha agregado tu firma",'success')
               return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
           else:
               flash("Vuelve a intentarlo",'warning')
               return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
        else:
                flash("Vuelve a intentarlo",'warning')
                return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
    else:
        return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
    


#Funcion aprobar el dictamen de la solicitude de desacargo
@revisar_solicitudes_descargo_bp.route('/aprobar_solicitud', methods=["GET","POST"])
@es_tecnico
@comprobando_autorizacion
def aprobar_solicitud():
    if request.method == "POST":
        id_solicitud_descargo = request.form.get('id_solicitud_descargo')
        if not session.get("url_firma_imagen"):
            flash("Debes ingresar tu firma",'warning')
            return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
        
        registro = db.mostrar_solicitudes_descargo_id_solicitud_descargo(id_solicitud_descargo)
        print(registro)

        datos_editar = {
            "firma_jefe_unidad_bien": session["url_firma_imagen"],
            "estado_solicitud": 1
        }

        firma_jefe_departamento = registro[16]
        firma_responsable_dictamen = registro[17]
        firma_responsable_bien = registro[18]

        if firma_jefe_departamento and firma_responsable_dictamen and firma_responsable_bien and id_solicitud_descargo:
            estado_solicitud = db.aprobar_solicitud_descargo(datos_editar, id_solicitud_descargo)
            if estado_solicitud:
                flash("Enhorabuena, se ha aprobado la solicitud", 'success')
            else:
                flash("No se pudo aprobar la solicitud. Por favor, inténtalo de nuevo.", 'warning')
        else:
            if not id_solicitud_descargo:
                flash("ID de solicitud de descargo no proporcionado.", 'warning')
            flash("Faltan firmas para poder aprobar la solicitud.", 'warning')
        
        return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
    else:
        return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
    

def formatear_descripcion(contenido):
    lineas = textwrap.wrap(contenido, width=25)
    return '\n'.join(lineas)


#Funcion agregar el dictaen de infotecnologia
@revisar_solicitudes_descargo_bp.route('/agregar_dictamen', methods=["GET","POST"])
@es_tecnico
@comprobando_autorizacion
def agregar_dictamen():
    if request.method=="POST":
        id_solicitud_descargo =  request.form.get('id_solicitud_descargo')
        if not session.get("url_firma_imagen"):
            flash("Debes ingresar tu firma",'warning')
            return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
        
        descripcion =  formatear_descripcion(request.form.get('descripcion'))
        diagnostico =  request.form.get('diagnostico')


        datos_editar = {
            "descripcion": descripcion,
            "diagnostico": diagnostico,
            "firma_responsable_dictamen":session["url_firma_imagen"],
            "numero_identidad_responsable_dictamen":session["codigo_usuario"]
        }

        print(datos_editar)
       
        estado_campos_vacios = validar_valores_no_vacios(datos_editar)
        if estado_campos_vacios:
           estado_solicitud = db.agregar_dictamen_solicitud_descargo(datos_editar,id_solicitud_descargo)
           if estado_solicitud:
               flash("Enhorabuena se ha agregado tu dictamen",'success')
               return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
           else:
               flash("Vuelve a intentarlo",'warning')
               return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
        else:
            
               flash("Debes ingresar los datos",'warning')
               return redirect(url_for('revisar_solicitudes_descargo_bp.index'))
    else:
        return redirect(url_for('revisar_solicitudes_descargo_bp.index'))