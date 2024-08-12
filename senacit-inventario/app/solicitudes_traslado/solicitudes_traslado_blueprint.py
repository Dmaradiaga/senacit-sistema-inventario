from flask import Blueprint, render_template,request,flash, redirect,url_for,session,send_file
from app.db.db import db
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion
from app.funciones_ayuda.funciones_ayuda import validar_valores_no_vacios, formatear_numero_identidad, convert_date_to_str
from app.solicitudes_traslado.forms.editar_solicitud_traslado_formulario import EditarSolicitudTrasladoFormulario
from datetime import datetime
import json
import time
import requests

#librerias de la funcion crear tabla
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


#Registra el BluePrint
solicitudes_traslado_bp = Blueprint('solicitudes_traslado_bp', __name__,
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
            

def acortar_texto(texto, longitud_maxima=50):
    if len(texto) > longitud_maxima:
        return texto[:longitud_maxima] + '...'
    return texto


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
    c.drawString(200, 650, "Solicitud de Traslado")  # Ajustar la posición y tamaño del título

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
@solicitudes_traslado_bp.route('/descargar_pdf/<int:id_solicitud_traslado>',methods=["GET","POST"])
@comprobando_autorizacion
def descargar_pdf(id_solicitud_traslado):
    if request.method=="POST":
        try:
                print(id_solicitud_traslado)
                # Buscar solicitudes de traslado en la tabla solicitud_traslado por id_solicitud_traslado
                registro = db.mostrar_solicitudes_traslado_id_solicitud_traslado(id_solicitud_traslado)
                    
                if len(registro)==0:
                    flash("No hay registros","warning")
                    return redirect(url_for('solicitudes_traslado_bp.index'))
                                                                            
                print(registro)
                # Si hay registros se muestran en el template

                datos_solicitud_traslado = {
                    'Nombre Solicitante': registro[1],
                    'Fecha Solicitud': registro[2],
                    'Lugar': registro[4],
                    'Justificación Traslado': registro[5][:70],
                    'Número Identidad Solicitante': formatear_numero_identidad(registro[6]),
                    'Cargo': registro[9],
                    'Serie': registro[7],
                    'Color': registro[8],
                    'Número Inventario': registro[10],
                    'Descripción':registro[3][:70],
                    'Departamento Interno': registro[11],
                    'Tiempo Traslado':registro[19][:70]
            }
            
                imagenes = [
                    {'url': registro[15], "texto":"Responsable del Bien",},
                    {'url': registro[14], "texto":"Jefe Departamento",},
                    {'url': registro[16], "texto":"Jefe de Bienes",}
                ]


                pdf_data = generar_pdf(datos_solicitud_traslado,imagenes)
                #pdf_data = crear_pdf(datos_solicitud_traslado,imagenes)
                return send_file(
                        BytesIO(pdf_data),
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name='solicitud_traslado.pdf'
                    )

        except Exception as e:
                flash("No se pudo generar el pdf","warning")
                print("ERROR PDF: ",e)
                return redirect(url_for("solicitudes_traslado_bp.index"))

    else:
          return redirect(url_for("solicitudes_traslado_bp.index"))


# Editar solicitud de descargo por el número de identidad del solicitante
@solicitudes_traslado_bp.route('/editar_solicitud_traslado/<int:id_solicitud_traslado>', methods=['GET','POST'])
@comprobando_autorizacion
def editar_solicitud_traslado(id_solicitud_traslado):
    global registro
    form = EditarSolicitudTrasladoFormulario()
    
    if request.method == "POST":
        editar_solicitud_traslado = {
            "lugar": request.form["lugar"].strip(),
            "puesto": request.form["puesto"].strip(),
            "descripcion": request.form["descripcion_bien"].strip(),
            "serie": request.form["serie"].strip(),
            "justificacion_traslado": request.form["justificacion_traslado"].strip(),
            "imagen": registro[12],
            "numero_inventario": request.form["numero_inventario"],
            'firma_responsable_bien': session["url_firma_imagen"]
        }
    
        estado_valores = validar_valores_no_vacios(editar_solicitud_traslado)

        if estado_valores:
            try:
                # Asignar fechas del formulario si existen
                fecha_inicio = request.form.get('fecha_inicio')
                fecha_final = request.form.get('fecha_final')
                
                if fecha_inicio and fecha_final:
                    editar_solicitud_traslado["fecha_inicio"] = fecha_inicio
                    editar_solicitud_traslado["fecha_final"] = fecha_final
                    editar_solicitud_traslado["fecha_solicitud"] = fecha_inicio

                    # Convertir las fechas a objetos datetime
                    inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                    fin = datetime.strptime(fecha_final, '%Y-%m-%d')

                    # Calcular la duración en días
                    duracion = (fin - inicio).days + 1

                    # Formato de las fechas para la respuesta
                    inicio_str = inicio.strftime("%A %d de %B")
                    fin_str = fin.strftime("%A %d de %B del %Y")

                    # Crear el mensaje detallado
                    mensaje = f"El traslado se hará del {inicio_str} al {fin_str} ({duracion} días en total)."
                    editar_solicitud_traslado['mensaje'] = mensaje
                else:
                    editar_solicitud_traslado["fecha_inicio"] = registro[18]
                    editar_solicitud_traslado["fecha_final"] = registro[17]
                    editar_solicitud_traslado["fecha_solicitud"] = registro[18]
                    editar_solicitud_traslado['mensaje'] = registro[19]

                # Actualizar el registro en la base de datos
                estado_consulta = db.editar_solicitud_traslado(editar_solicitud_traslado, id_solicitud_traslado)

                if estado_consulta:
                    nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                    detalle_actividad = json.dumps(editar_solicitud_traslado, default=convert_date_to_str)   
                    db.registrar_accion(session["codigo_usuario"], nombre_usuario, "EDITAR", "solicitud_traslado",detalle_actividad)
                    
                    flash('Registro actualizado exitosamente', 'success')
                    return redirect(url_for('solicitudes_traslado_bp.index'))
                else:
                    flash('No se pudo actualizar el registro', 'warning')
            except Exception as e:
                print(f"Error causado por: {str(e)}")
                flash(f'No se pudo actualizar el registro. Error: {str(e)}', 'warning')
                return redirect(url_for('solicitudes_traslado_bp.index'))
        else:
            flash("Debes ingresar los datos", 'warning')
        
        return render_template('editar_solicitud_traslado.html', form=form)


    else:
        try:
            registro = db.mostrar_solicitudes_traslado_id_solicitud_traslado(id_solicitud_traslado)
            
            if len(registro) == 0:
                flash("No hay registros", "warning")
                return redirect(url_for('solicitudes_traslado_bp.index'))
            
            print(registro)
           # form.fecha_solicitud.data = registro[2]
            form.descripcion_bien.data = registro[3]
            form.lugar.data = registro[4]
            form.justificacion_traslado.data = registro[5]
            form.puesto.data = registro[9]
            form.serie.data = registro[7]
            form.numero_inventario.data = registro[10]

        except Exception as e:
            print("Error al cargar el registro:", e)
            flash('Ocurrió un error al cargar el registro.', 'warning')
    
    return render_template('editar_solicitud_traslado.html', form=form)    
        

#Eliminar solicitud descargo
@solicitudes_traslado_bp.route('/eliminar_solicitud_traslado/<int:id_solicitud_traslado>', methods=['GET','POST'])
@comprobando_autorizacion
def eliminar_solicitud_traslado(id_solicitud_traslado):
            if request.method=="POST":
                try:
                    # Buscar solicitudes de traslado en la tabla solicitud_traslado
                    estado_solicitud = db.eliminar_solicitud_traslado(id_solicitud_traslado)
                                                                            
                    if estado_solicitud:
                        nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]
                        detalle_actividad = json.dumps({"ID_SOLICITUD": id_solicitud_traslado}, default=convert_date_to_str)   
                        db.registrar_accion(session["codigo_usuario"], nombre_usuario, "ELIMINAR", "solicitud_traslado",detalle_actividad)
                        
                        flash("El registro se ha eliminado","success")
                        return redirect(url_for("solicitudes_traslado_bp.index"))
                    else:
                        flash("No se pudo eliminar el registro","warning")
                        return redirect(url_for("solicitudes_traslado_bp.index"))
                except Exception as e:
                    # Muestra error si no hay
                    return render_template("solicitudes_traslado.html", mensaje_error="Vuelve a intentarlo.")
            else:
                return redirect(url_for("solicitudes_traslado_bp.index"))
                


#Mostrar solicitudes de descargo por el número de identidad del solicitante
@solicitudes_traslado_bp.route('/',methods=["GET"])
@comprobando_autorizacion
def index():
            numero_identidad = session["codigo_usuario"]
            try:
                # Buscar solicitudes de descargo en la tabla solicitud_descargo
                registros = db.mostrar_solicitudes_traslado_numero_identidad(numero_identidad)
                
                if len(registros)==0:
                    return render_template('solicitudes_traslado.html')
                                                                        
                #print("ESTADO SOLICITUD: ",type(registros[16]))
                # Si hay registros se muestran en el template
                return render_template('solicitudes_traslado.html', 
                                        registros=registros)
            except Exception as e:
                # Muestra error si no hay
                print(e)
                return render_template("solicitudes_traslado.html", mensaje_error="Vuelve a intentarlo.")