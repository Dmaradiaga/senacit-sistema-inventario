from flask import Blueprint, render_template,request,flash, redirect,url_for,session,send_file
from app.db.db import db
from app.solicitudes_descargo.forms.editar_solicitud_descargo_formulario import EditarSolicitudDescargoFormulario
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion
from app.funciones_ayuda.funciones_ayuda import validar_valores_no_vacios, convert_date_to_str, formatear_numero_identidad
import time
import json
import requests

#Librerías para generar el pdf
from io import BytesIO
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


#Registra el BluePrint
solicitudes_descargo_bp = Blueprint('solicitudes_descargo_bp', __name__,
    template_folder='templates',
    static_folder='static')

registro = None


#Función para descargar las imágenes que se utilizaran en el pdf
def descargar_imagen(url, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                print(f"Intento {attempt + 1} falló. Reintentando en {delay} segundos...")
                time.sleep(delay)
            else:
                print(f"No se pudo obtener la imagen después de {max_retries} intentos.")
                return None
            

#Función para crear el pdf
def generar_pdf(datos_solicitud,imagenes):
# Crear un objeto Canvas para el PDF
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Obtener la ruta absoluta de la imagen del logo
    directorio_ruta = os.path.dirname(os.path.abspath(__file__))
    logo_ruta = os.path.join(directorio_ruta, "static/imagenes/logo-senacit.png")

    # Verificar la existencia del archivo de logo y su formato
    if not os.path.exists(logo_ruta):
        raise FileNotFoundError(f"No se puede encontrar el archivo: {logo_ruta}")

    # Agrega el logo en la parte superior izquierda
    c.drawImage(logo_ruta, 30, 700, width=250, height=75, mask='auto')

    # Agrega el título
    c.setFont("Helvetica-Bold", 12)
    c.drawString(200, 650, "Solicitud de Descargo")  # Ajustar la posición y tamaño del título

    # Configura la fuente y tamaño de texto para el contenido de la tabla
    c.setFont("Helvetica", 10)

    # Agrega la tabla de datos
    y = 580  # Posición inicial en Y, ajustada para dejar más espacio para el título y el logo
    for campo, valor in datos_solicitud.items():
        c.drawString(100, y, campo)
        c.drawString(300, y, str(valor))
        y -= 20

    # Definir las posiciones iniciales para las imágenes
    _x = 100  # Posición inicial en X
    _y = 210  # Posición inicial en Y

    # Itera sobre las claves y valores del diccionario de imágenes
    for imagen in imagenes:
        imagen_datos = descargar_imagen(imagen["url"])
        if imagen_datos:
            # Dibujar la imagen en la posición actual
            img = ImageReader(BytesIO(imagen_datos))
            c.drawImage(img, _x, _y, width=50, height=50)
            c.drawString(_x, _y - 20, imagen["texto"])  # Agregar el texto debajo de la imagen
            
            # Ajusta las coordenadas para la próxima imagen
            _x += 150  # Aumentar la posición en X para la próxima imagen

            # Si la posición en X excede el límite, reiniciar en X y mover hacia abajo en Y
            if (_x + 50) > 500:  # Ajuste según el ancho de la imagen
                _x = 100  # Reiniciar en X
                _y -= 100  # Mover hacia abajo en Y para la próxima fila de imágenes
        else:
             print(f"No se pudo cargar la imagen: {imagen['url']}")


    # Guardar el PDF
    c.showPage()
    c.save()

    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()



#Mostrar solicitudes de descargo por el número de identidad del solicitante
@solicitudes_descargo_bp.route('/descargar_pdf/<string:id_solicitud_descargo>',methods=["GET","POST"])
@comprobando_autorizacion
def descargar_pdf(id_solicitud_descargo):
    if request.method=="POST":
        try:
                print(id_solicitud_descargo)
                # Buscar solicitudes de descargo en la tabla solicitud_descargo por id_solicitud_descargo
                registro = db.mostrar_solicitudes_descargo_id_solicitud_descargo(id_solicitud_descargo)
                    
                if len(registro)==0:
                    flash("No hay registros","warning")
                    return redirect(url_for('solicitudes_descargo_bp.index'))
                                                                            
                print(registro)
                # Si hay registros se muestran en el template

                datos_solicitud_descargo = {
                    'Nombre Solicitante': registro[1],
                    'Fecha Solicitud': registro[2],
                    'Lugar': registro[3],
                    'Justificación Descargo': registro[4][:70],
                    'Número Identidad Solicitante': formatear_numero_identidad(registro[5]),
                    'N.Identidad Responsable Dictamen': formatear_numero_identidad(registro[20]),
                    'Puesto': registro[6],
                    'Marca':registro[7],
                    'Serie': registro[8],
                    'Número Inventario': registro[9],
                    'Diagnóstico': registro[10][:70],
                    'Departamento Interno': registro[13],
                    'Descripción':registro[12][:70]
                }
            
                imagenes = [
                    {'url': registro[18], "texto":"Responsable del Bien",},
                    {'url': registro[16], "texto":"Jefe Departamento",},
                    {'url': registro[19], "texto":"Jefe de Bienes",},
                    {'url': registro[17], "texto":"Responsable Dictamen"}
                ]


                pdf_data = generar_pdf(datos_solicitud_descargo,imagenes)
                #pdf_data = crear_tabla(datos_solicitud_descargo,imagenes)

                return send_file(
                        BytesIO(pdf_data),
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name='solicitud_descargo.pdf'
                    )

        except Exception as e:
                flash("No se pudo generar el pdf","warning")
                print(f"ERROR PDF: {str(e)}",)
                return redirect(url_for("solicitudes_descargo_bp.index"))
    else:
          return redirect(url_for("solicitudes_descargo_bp.index"))


# Editar solicitud de descargo por el número de identidad del solicitante
@solicitudes_descargo_bp.route('/editar_solicitud_descargo/<string:id_solicitud_descargo>', methods=['GET','POST'])
@comprobando_autorizacion
def editar_solicitud_descargo(id_solicitud_descargo):
    global registro
    form = EditarSolicitudDescargoFormulario()
    if request.method == "POST":
        
        editar_solicitud_descargo = {
                "lugar": request.form["lugar"].strip(),
                "puesto": request.form["puesto"].strip(),
                "departamento_interno": request.form["departamentos_internos"].strip(),
                "marca": request.form["marca"].strip(),
                "serie": request.form["serie"].strip(),
                "justificacion_descargo": request.form["justificacion_descargo"].strip(),
                "modelo": request.form["modelo"].strip(),
                "imagen": registro[14],
                "fecha_solicitud" : request.form['fecha_solicitud'],
                "numero_inventario":request.form["numero_inventario"],
                "firma_responsable_bien":session["url_firma_imagen"]
            }
        
        estado_valores = validar_valores_no_vacios(editar_solicitud_descargo)

        if estado_valores:
            try:
                #Ediar solicitude por id
                estado_consulta = db.editar_solicitud_descargo(editar_solicitud_descargo,id_solicitud_descargo)
                
                if estado_consulta:
                    nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                    detalle_actividad = json.dumps(editar_solicitud_descargo, default=convert_date_to_str)        
                    db.registrar_accion(session["codigo_usuario"], nombre_usuario, "EDITAR", "solicitud_descargo",detalle_actividad)
                    
                    flash('Registro actualizado exitosamente', 'success')
                    return redirect(url_for('solicitudes_descargo_bp.index'))
                else:
                    flash('No se pudo actualizar el registro', 'warning')
                    return render_template('editar_solicitud_descargo.html', 
                                        form=form)
            except Exception as e:
                # Muestra error si no hay
                print("Error al buscar registro por numero de inventario:", e)
                flash('Ocurrió un error al buscar el registro.','warning')
                return redirect(url_for('solicitudes_descargo_bp.index'))
        else:
            flash("Debes ingresar los datos",'warning')
            return render_template('editar_solicitud_descargo.html', 
                                        form=form)
    else:
            try:
                # Buscar solicitudes de descargo en la tabla solicitud_descargo por id_solicitud_descargo
                registro = db.mostrar_solicitudes_descargo_id_solicitud_descargo(id_solicitud_descargo)
                
                if len(registro)==0:
                    flash("No hay registros","warning")
                    return redirect(url_for('solicitudes_descargo_bp.index'))
                                                                        
                print(registro)
                # Si hay registros se muestran en el template
                form.fecha_solicitud.data = registro[2]
                form.lugar.data = registro[3]
                form.justificacion_descargo.data = registro[4]
                form.departamentos_internos.data = registro[13]
                form.puesto.data = registro[6]
                form.marca.data = registro[7]
                form.serie.data = registro[8]
                form.numero_inventario.data = registro[9]
                form.modelo.data = registro[11]

                return render_template('editar_solicitud_descargo.html', 
                                        form=form)
            except Exception as e:
                # Muestra error si no hay
                return render_template("editar_solicitud_descargo.html", 
                                       mensaje_error="Vuelve a intentarlo.")     
        

#Eliminar solicitud descargo
@solicitudes_descargo_bp.route('/eliminar_solicitud_descargo/<string:id_solicitud_descargo>', methods=['GET','POST'])
@comprobando_autorizacion
def eliminar_solicitud_descargo(id_solicitud_descargo):
            if request.method=="POST":
                try:
                    # Buscar solicitudes de descargo en la tabla solicitud_descargo
                    estado_solicitud = db.eliminar_solicitud_descargo(id_solicitud_descargo)
                                                                            
                    if estado_solicitud:
                        nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                        detalle_actividad = json.dumps({"ID_SOLICITUD_DESCARGO":id_solicitud_descargo}, default=convert_date_to_str)   
                        db.registrar_accion(session["codigo_usuario"], nombre_usuario, "ELIMINAR", "solicitud_descargo",detalle_actividad)
                        
                        flash("El registro se ha eliminado","success")
                        return redirect(url_for("solicitudes_descargo_bp.index"))
                    else:
                        flash("No se pudo eliminar el registro","warning")
                        return redirect(url_for("solicitudes_descargo_bp.index"))
                except Exception as e:
                    # Muestra error si no hay
                    return render_template("solicitudes_descargo.html", mensaje_error="Vuelve a intentarlo.")
            else:
                 return redirect(url_for("solicitudes_descargo_bp.index"))


#Mostrar solicitudes de descargo por el número de identidad del solicitante
@solicitudes_descargo_bp.route('/',methods=["GET"])
@comprobando_autorizacion
def index():
            numero_identidad = session["codigo_usuario"]
            try:
                # Buscar solicitudes de descargo en la tabla solicitud_descargo
                registros = db.mostrar_solicitudes_descargo_numero_identidad(numero_identidad)
                
                if len(registros)==0:
                    return render_template('solicitudes_descargo.html')
                                                                        
                return render_template('solicitudes_descargo.html', 
                                        registros=registros)
            except Exception as e:
                # Muestra error si no hay
                print(e)
                return render_template("solicitudes_descargo.html", mensaje_error="Vuelve a intentarlo.")
            

