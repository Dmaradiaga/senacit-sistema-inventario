from flask import Blueprint, render_template,request,flash, redirect,url_for,send_file
from app.db.db import db
from app.consultas.forms.consultas_formulario import ConsultasFormulario
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion
import locale
from app.funciones_ayuda.funciones_ayuda import formatear_numero_identidad


#Librerías para generar el pdf
from io import BytesIO
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


consultas_bp = Blueprint('consultas_bp', __name__,
    template_folder='templates',
    static_folder='static')


def formatear_lps(valor):
    # Configuración para la localización para el formato de números
    locale.setlocale(locale.LC_ALL, 'es_HN')

    # Convertir el valor al formato decimal
    valor_decimal = valor / 100

    # Formatear el valor para incluir la coma de los miles y el símbolo de Lempiras
    valor_formateado = locale.format_string("%.2f", valor_decimal, grouping=True)

    # Eliminar el símbolo de la moneda 'L'
    valor_formateado = valor_formateado.replace('L', '')

    # Agregar el símbolo de la moneda 'L' al inicio
    valor_formateado = 'L. ' + valor_formateado

    return valor_formateado



#Función para crear el pdf
def generar_pdf(datos_solicitud):
    # Crear un objeto Canvas para el PDF
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Obtener la ruta absoluta de la imagen del logo
    directorio_ruta = os.path.dirname(os.path.abspath(__file__))
    logo_ruta = os.path.join(directorio_ruta, "static/imagenes/senacit-logo.png")

    # Verificar la existencia del archivo de logo y su formato
    if not os.path.exists(logo_ruta):
        raise FileNotFoundError(f"No se puede encontrar el archivo: {logo_ruta}")
    

    # Agrega el icono en la parte superior izquierda
    c.drawImage(logo_ruta, 30, 700, width=250, height=75, mask='auto')  

    # Agrega el título
    c.setFont("Helvetica-Bold", 12)
    c.drawString(200, 650, "Información del Bien")  # Ajustar la posición y tamaño del título

    # Configura la fuente y tamaño de texto para el contenido de la tabla
    c.setFont("Helvetica", 10)

    # Agrega la tabla de datos
    y = 600  # Posición inicial en Y, ajustada para dejar más espacio para el título y el logo
    for campo, valor in datos_solicitud.items():
        c.drawString(100, y, campo)
        c.drawString(300, y, str(valor))
        y -= 20


    # Guardar el PDF
    c.showPage()
    c.save()

    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()


#
@consultas_bp.route('/descargar_pdf/<string:numero_inventario>',methods=["GET","POST"])
@comprobando_autorizacion
def descargar_pdf(numero_inventario):
    if request.method=="POST":
        try:
                print(numero_inventario)
                # Buscar solicitudes de descargo en la tabla solicitud_descargo por id_solicitud_descargo
                registro = db.mostrar_registro_por_numero_inventario(numero_inventario)
                    
                if len(registro)==0:
                    flash("No hay registros","warning")
                    return redirect(url_for('consultas_bp.index'))
                                                                            
                print(registro[12])

                datos_informacion_bien = {
                    'Tipo de Documento': registro[0],
                    'Número de Documento': registro[1],
                    'Descripción del Bien': registro[2],
                    'Número de Inventario': registro[3],
                    'Modelo': registro[4],
                    'Marca': registro[5],
                    'Serie': registro[6],
                    'Placa':  registro[7],
                    'Motor': registro[8],
                    'Número de Chasis': registro[9],
                    'Color': registro[10],
                    'Departamento':  registro[11],
                    'Edificio': registro[13],
                    'Piso': registro[14],
                    'Orden de Compra': registro[15],
                    'Fecha de Ingreso': registro[16],
                    'Costo de Adquisición': formatear_lps(registro[17]),
                    'Modalidad de Contratación': registro[18],
                    'Comentario': registro[19],
                    'Estado del Bien': registro[20],
                    'Oficina': registro[21],
                    'Fecha de Documento': registro[22],
                    'Fecha de Registro del Bien': registro[23],
                    'Fecha de Registro de Inventario': registro[27],
                    'Responsable del Bien': registro[24] +" " +registro[25],
                    'Número Identidad': formatear_numero_identidad(registro[26])
            }
                
                # Crear el diccionario filtrado
                datos_informacion_bien = {
                    clave: valor for clave, valor in datos_informacion_bien.items() 
                    if clave not in ['Placa','Motor', 'Número de Chasis', 'Departamento','Orden de Compra',] or valor
                }

                if  registro[11]!="":
                    datos_informacion_bien["Municipio"] = registro[12]
                    
                pdf_data = generar_pdf(datos_informacion_bien)

                return send_file(
                        BytesIO(pdf_data),
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name='Informacion_Bien.pdf'
                    )

        except Exception as e:
                flash("No se pudo generar el pdf","warning")
                print("ERROR PDF: ",e)
                return redirect(url_for("consultas_bp.index"))

    else:
          return redirect(url_for("consultas_bp.index"))
    
    

#Mostrar solicitudes de descargo por el número de identidad del solicitante
@consultas_bp.route('/descargar_bodega_pdf/<string:numero_inventario>',methods=["GET","POST"])
@comprobando_autorizacion
def descargar_bodega_pdf(numero_inventario):
    if request.method=="POST":
        try:
                print(numero_inventario)
                # Buscar solicitudes de descargo en la tabla solicitud_descargo por id_solicitud_descargo
                registro = db.mostrar_registro_por_numero_inventario_bodega(numero_inventario)
                    
                if len(registro)==0:
                    flash("No hay registros","warning")
                    return redirect(url_for('consultas_bp.index'))
                                                                            
                print(registro[12])

                datos_informacion_bien = {
                    'Tipo de Documento': registro[0],
                    'Número de Documento': registro[1],
                    'Descripción del Bien': registro[2][:70],
                    'Número de Inventario': registro[3],
                    'Modelo': registro[5],
                    'Serie': registro[6],
                    'Color': registro[10],     
                    'Edificio': registro[13],
                    'Piso': registro[14],
                    'Orden de Compra': registro[15],
                    'Fecha de Ingreso': registro[16],
                    'Costo de Adquisición': formatear_lps(registro[17]),
                    'Modalidad de Contratación': registro[18],
                    'Comentario': registro[19][:70],
                    'Estado del Bien': registro[20],
                    'Oficina': registro[21],
                    'Fecha de Documento': registro[22],
                    'Fecha de Registro del Bien': registro[24],
                    'Fecha de Registro en Bodega': registro[23]
            }

                # Crear el diccionario filtrado
                datos_informacion_bien = {
                    clave: valor for clave, valor in datos_informacion_bien.items() 
                    if clave not in ['Placa', 'Modalidad de Contratación', 'Motor', 'Número de Chasis', 'Departamento','Orden de Compra'] or valor
                }

                if  registro[11]!="":
                    datos_informacion_bien["Municipio"] = registro[12]

                pdf_data = generar_pdf(datos_informacion_bien)

                return send_file(
                        BytesIO(pdf_data),
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name='Informacion_Bien[Bodega].pdf'
                    )

        except Exception as e:
                flash("No se pudo generar el pdf","warning")
                print("ERROR PDF: ",e)
                return redirect(url_for("consultas_bp.index"))

    else:
          return redirect(url_for("consultas_bp.index"))
    



@consultas_bp.route('/buscar_registro_numero_inventario', methods=['GET', 'POST'])
@comprobando_autorizacion
def buscar_registro_numero_inventario():
    form = ConsultasFormulario()
    if request.method == "POST":
        numero_inventario = request.form["numero_inventario"].strip()
        
        # Depuración adicional
        print("NÚMERO DE INVENTARIO RECIBIDO: ", numero_inventario, type(numero_inventario))

        if numero_inventario == "":
            flash("Debes ingresar el número de inventario", 'warning')
            return redirect(url_for('consultas_bp.index'))

        try:
            # Asegúrate de que numero_inventario sea una cadena
            numero_inventario = str(numero_inventario)
            
            # Depuración adicional antes de la consulta
            print("NÚMERO DE INVENTARIO PARA CONSULTA: ", numero_inventario, type(numero_inventario))
            
            registro = db.mostrar_registro_por_numero_inventario(numero_inventario)
            
            # Depuración adicional después de la consulta
            print("DATOS DE LA CONSULTA DEL INVENTARIO: ", registro)

            if registro is not None:
                return render_template('mostrar_registro.html', registro=registro)
            else:
                flash('No se encontró registro', 'warning')
                return redirect(url_for('consultas_bp.index'))

        except Exception as e:
            print(f"Error al buscar registro por número de inventario: {str(e)}")
            flash('Ocurrió un error al buscar el registro.', 'warning')
            return redirect(url_for('consultas_bp.index'))
    else:
        return render_template('consultar.html', form=form)





# Ruta para buscar un registro por número de inventario en bodega.
@consultas_bp.route('/buscar_registro_numero_inventario_bodega', methods=['GET','POST'])
@comprobando_autorizacion
def buscar_registro_numero_inventario_bodega():
    form = ConsultasFormulario()
    if request.method == "POST":
        # Obtener el código de numero de inventario del formulario
        numero_inventario_bodega = request.form['numero_inventario_bodega']
        numero_inventario_bodega = numero_inventario_bodega.strip()
        if numero_inventario_bodega!="":
            try:
                # Buscar el registro en la base de datos utilizando el  numero de inventario en la bodega
                registro = db.mostrar_registro_por_numero_inventario_bodega(numero_inventario_bodega)
                
                if registro is None:
                    # Si no se encuentran  registros, mostrar un mensaje de error.
                    flash('No se encontró registro','warning')
                    return redirect(url_for('consultas_bp.index'))
                                           
                print(registro)
                print(type(registro[25]))
                # Si se encuentra el registro, redirigir a la página de edición con los datos del registro
                return render_template('mostrar_registro_bodega.html', 
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



#Ruta maneja buscar_registro_numero_identidad
@consultas_bp.route('/buscar_registro_numero_identidad',methods=["POST","GET"])
@comprobando_autorizacion
def buscar_registro_numero_identidad():
    form = ConsultasFormulario()
    if request.method == "POST":
        # Obtener el numero de identidad del formulario
        numero_identidad = request.form['numero_identidad']
        numero_identidad = numero_identidad.strip()
        if numero_identidad!="":
            try:
                # Buscar el registro en la base de datos utilizando el código de numero de invenetario
                registros = db.mostrar_registro_por_numero_identidad(numero_identidad)
                
                if len(registros)==0:
                    # Si no se encuentran  registros, mostrar un mensaje
                    flash('No se encontraron registros','warning')
                    return redirect(url_for('consultas_bp.index'))
                                           
                print(registros)
                print("TOTAL DE REGISTROS: ", len(registros))
                total_registros = len(registros)
                monto_total = 0
                for tupla in registros:
                 #Sumar el elemento en la posición 25 de la tupla actual
                    monto_total+= tupla[24]

               # monto_total = formatear_lps(monto_total)
                # Si se encuentran los registros, se muestran en la pagina mostrar_registros.html
                return render_template('mostrar_registros.html', monto_total=monto_total,
                                        registros=registros, total_registros=total_registros)
            except Exception as e:
                # Muestra error si no hay
                print("Error al buscar registros por numero de identidad:", e)
                flash('Ocurrió un error al buscar los registros.','warning')
                return redirect(url_for('consultas_bp.index'))
        else:
            flash('Debes ingresar el numero de identidad.','warning')
            return redirect(url_for('consultas_bp.index'))
    else:
        #return render_template("consultar.html", form=form)
        return render_template('consultar.html',form=form)



#Ruta maneja consultar registro
@consultas_bp.route('/',methods=["GET"])
@comprobando_autorizacion
def index():
    form = ConsultasFormulario()
    return render_template("consultar.html", form=form)
