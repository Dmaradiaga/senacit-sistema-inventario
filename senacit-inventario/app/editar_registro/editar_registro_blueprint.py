from flask import Blueprint, render_template, url_for,request,flash,redirect,session
from app.db.db import db
from app.funciones_ayuda.funciones_ayuda import editar_imagen, verificar_extension_imagen,\
validar_numero_identidad, convert_date_to_str
from app.editar_registro.form.editar_registro__formulario import EditarFormulario
from app.editar_registro.form.editar_registro_formulario import ConsultaFormularioEditar
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion,comprobando_sesion_administrador
import json

# fechas del registro del inventario que se va a editar
fechas_globales ={} 
# id del registro del inventario que se va a editar
id_inventario = None 
registro = None

editar_registro_bp = Blueprint('editar_registro_bp', __name__,
    template_folder='templates',
    static_folder='static')

def validar_valores_no_vacios(diccionario):
    # Verificar que cada valor del diccionario no esté vacío si es una cadena
    for valor in diccionario.values():
        if isinstance(valor, str) and not valor.strip():
            return False
    return True


#Ruta maneja editar registro
@editar_registro_bp.route('/',methods=["GET"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def editar():
    form = ConsultaFormularioEditar()
    return render_template("editar.html",form=form)


# Ruta que maneja 
@editar_registro_bp.route('/buscar_registro', methods=['GET','POST'])
@comprobando_sesion_administrador
@comprobando_autorizacion
def buscar_registro():
    if request.method == "POST":
         # Obtener el código de numero de inventario del formulario
        numero_inventario = request.form['numero_inventario']
        numero_inventario = numero_inventario.strip()
        if numero_inventario!="":
            try:
                # Buscar el registro en la base de datos utilizando el código de numero de invenetario
                registro = db.buscar_registro_por_numero_inventario(numero_inventario)
                
                if registro is None:
                    # Si no se encuentra el registro, mostrar un mensaje de error
                    flash('No se encontraron registros.', 'warning')
                    return redirect(url_for('editar_registro_bp.editar'))  # Redirigir a alguna página de error o inicio
                
                session["registro"] = registro
                # Si se encuentra el registro, redirigir a la página de edición con los datos del registro
                return redirect(url_for('editar_registro_bp.editar_registro'))
            except Exception as e:
                # Muestra error si no hay
                print("Error al buscar registro por orden de compra:", e)
                flash("Ocurrió un error al buscar el registro.", "warning")
                return redirect(url_for('editar_registro_bp.editar'))
        else:
            flash("Debe ingresar el número de inventario", "warning")
            return redirect(url_for('editar_registro_bp.editar'))
    return redirect(url_for('editar_registro_bp.editar'))



@editar_registro_bp.route('/editar_imagenes_registro_inventario/<string:numero_inventario>', methods=['GET','POST'])
@comprobando_sesion_administrador
@comprobando_autorizacion
def editar_imagenes_registro_inventario(numero_inventario):
    numero_inventario = numero_inventario
    global registro
    
    if request.method=="POST":
        if "imagen" in request.files:
            imagen = request.files["imagen"]
            indice_imagen = int(request.form['imagen_indice'])
            imagenes = json.loads(registro[27])

            if imagen.filename == '':
                flash("Debes seleccionar una imagen", "warning")
                return redirect(url_for("editar_registro_bp.editar_imagenes_registro_inventario",numero_inventario=numero_inventario))
            
            extension_imagen = verificar_extension_imagen(imagen.filename)
            if extension_imagen:
                url_imagen = editar_imagen(imagen, imagenes[indice_imagen]["public_id"])
                imagenes[indice_imagen]["secure_url"] = url_imagen
                imagenes_actualizadas = json.dumps(imagenes)

                datos_actualizar = { "imagenes_bien": imagenes_actualizadas }
                estado_consulta = db.actualizar_imagenes_inventario(datos_actualizar,numero_inventario)

                if estado_consulta:
                    flash("La imagen se ha actualizado correctamente.", "success")
                    return redirect(url_for("editar_registro_bp.editar_imagenes_registro_inventario",numero_inventario=numero_inventario))
                else:
                    flash("No se pudo actualizar la imagen. Vuelve a intentarlo.", "warning")
                    return redirect(url_for("editar_registro_bp.editar_imagenes_registro_inventario",numero_inventario=numero_inventario))
            else:
                flash("Debes ingresar un imagen (png, jpg, jpeg)", "warning")
                return redirect(url_for("editar_registro_bp.editar_imagenes_registro_inventario",numero_inventario=numero_inventario))
        else:
            flash("Debes ingresar una imagen", "warning")
            return redirect(url_for("editar_registro_bp.editar_imagenes_registro_inventario",numero_inventario=numero_inventario))
    else:
        if numero_inventario!="":
            try:
                # Buscar el registro en la base de datos utilizando el código de numero de inventario
                registro = db.buscar_registro_por_numero_inventario(numero_inventario)
                
                if registro is None:
                    # Si no se encuentra el registro, mostrar un mensaje de error
                    flash('No se encontraron registros.', 'warning')
                    return redirect(url_for('editar_registro_bp.editar'))  # Redirigir a alguna página de error o inicio
                
                imagenes = json.loads( registro[27])
                return render_template("editar_imagenes.html",imagenes=imagenes, numero_inventario=numero_inventario)
            
            except Exception as e:
                print(f"Ocurrió un error: {str(e)}")  
                flash("Ocurrió un error al buscar el registro.", "warning")
                return redirect(url_for('editar_registro_bp.editar'))
        else:
            flash("Debe ingresar el número de inventario", "warning")
            return redirect(url_for('editar_registro_bp.editar'))



@editar_registro_bp.route('/editar_registro', methods=['GET','POST'])
@comprobando_sesion_administrador
@comprobando_autorizacion
def editar_registro():
    registro = session.pop('registro', None)
    form = EditarFormulario()
    global id_inventario
    
    if request.method == "POST":
        fecha_documento = request.form['fecha_documento']
        fecha_ingreso = request.form['fecha_ingreso']
        fecha_ingreso_bien = request.form['fecha_ingreso_bien']

        print("fechas globales: ", fechas_globales)

        datos_editar = {
            'tipo_documento': form.tipo_documento.data,             
            'numero_documento': form.numero_documento.data,
            'descripcion': form.descripcion.data,
            'numero_inventario': form.numero_inventario.data,
            'modelo': form.modelo.data,
            'marca': form.marca.data,
            'serie': form.serie.data,
            'color': form.color.data,
            'edificio': form.edificio.data,
            'piso': form.piso.data,
            'numero_identidad': form.numero_identidad.data,
            'oficina': form.oficina.data,          
            'costo_adquisicion': form.costo_adquisicion.data,
            'modalidad_contratacion': form.modalidad_contratacion.data,
            'comentario': form.comentario.data,
            'estado_bien': form.estado_bien.data,
            'departamento_interno':form.departamento_interno.data,
            'fecha_documento': form.fecha_documento.data,
            'fecha_ingreso': form.fecha_ingreso.data,
            'fecha_ingreso_bien': form.fecha_ingreso_bien.data
        }

        estado_valores = validar_valores_no_vacios(datos_editar)
        if fecha_documento == "":
            datos_editar['fecha_documento'] = fechas_globales['fecha_documento']
        if fecha_ingreso == "":
            datos_editar['fecha_ingreso'] = fechas_globales['fecha_ingreso']
        if fecha_ingreso_bien == "":
            datos_editar['fecha_ingreso_bien'] = fechas_globales['fecha_ingreso_bien']

        # mostrando el diccionario de los datos del formulario
        print(datos_editar)
        if estado_valores:
            datos_editar['placa'] = form.placa.data.strip()
            datos_editar['motor'] = form.motor.data.strip()
            datos_editar['municipio'] = form.municipio.data
            datos_editar['departamento'] = form.departamento.data
            datos_editar['numero_chasis'] = form.numero_chasis.data.strip()
            datos_editar['orden_compra'] = form.orden_compra.data.strip()
            #datos_editar['numero_identidad'] = form.numero_identidad.data

            es_numero_identidad = validar_numero_identidad(datos_editar["numero_identidad"])
            
            if not es_numero_identidad:
                flash("Debes ingresar un número de identidad válido","warning")
                return render_template('formulario_edicion.html', form=form)
            
            try:
                estado_consulta = db.editar_datos_inventario(datos_editar, id_inventario)
                if estado_consulta:
                    nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                    detalle_actividad = json.dumps(datos_editar, default=convert_date_to_str)
                    db.registrar_accion(session["codigo_usuario"], nombre_usuario, "ACTUALIZAR", "inventario", detalle_actividad)
                    
                    flash('Registro actualizado exitosamente', 'success')
                    return redirect(url_for('editar_registro_bp.editar'))
                else:
                    flash('No se pudo actualizar el registro', 'warning')
                    return redirect(url_for('editar_registro_bp.editar'))
            except Exception as e:
                    flash('Ocurrió un error al actualizar el registro: ','warning')
                    return redirect(url_for('editar_registro_bp.editar'))
        else:
            flash('Debes ingresar todos los datos.', 'warning')
            return render_template('formulario_edicion.html', form=form)
    else:
        if registro is None:
            return redirect(url_for("editar_registro_bp.editar"))
        
        print(registro)
        for indice, valor in enumerate(registro):
            print(f"indice: {indice} valor: {valor} ")     

        # Campos del formulario con los valores del registro
        form.tipo_documento.data = registro[1]
        form.numero_documento.data = registro[3]
        form.descripcion.data = registro[4]
        form.numero_inventario.data = registro[5]
        form.modelo.data = registro[6]
        form.marca.data = registro[7]
        form.serie.data = registro[8]
        form.placa.data = registro[9]
        form.motor.data = registro[10]
        form.numero_chasis.data = registro[11]
        form.color.data = registro[12]
        form.departamento.data = registro[13]
        form.departamento_interno.data = registro[14]
        form.municipio.data = registro[15]
        form.edificio.data = registro[16]
        form.piso.data = registro[17]
        form.orden_compra.data = registro[18]
        form.costo_adquisicion.data = registro[20]
        form.modalidad_contratacion.data = registro[21]
        form.numero_identidad.data = registro[22]
        form.comentario.data = registro[23]
        form.estado_bien.data = registro[24]
        form.oficina.data = registro[25]
        #form.fecha_ingreso = registro[29]
        #form.fecha_ingreso_bien = registro[30]
        #form.fecha_documento = registro[31]
       
        
        fechas_globales['fecha_ingreso'] =  registro[29]
        fechas_globales['fecha_ingreso_bien'] =  registro[30]
        fechas_globales['fecha_documento'] =  registro[31]
        
        id_inventario = registro[0]
        print("ID_INVENTARIO: ",id_inventario)
        
        return render_template('formulario_edicion.html', form=form)
    