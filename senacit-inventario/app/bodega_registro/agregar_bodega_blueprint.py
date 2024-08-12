from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from app.db.db import db
from app.bodega_registro.forms.bodega_formulario import BodegaFormulario
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion, comprobando_sesion_administrador
import json
from app.funciones_ayuda.funciones_ayuda import agregar_imagenes, verificar_extension_imagen, \
validar_valores_no_vacios, convert_date_to_str



agregar_bodega_bp = Blueprint('agregar_bodega_bp', __name__,
                              template_folder='templates',
                              static_folder='static')






# Ruta agregar registro en bodega
@agregar_bodega_bp.route('/', methods=["GET", "POST"])
@comprobando_sesion_administrador
@comprobando_autorizacion
def index():
    form = BodegaFormulario()
    if request.method == 'POST':
        #imagen = request.files['imagen']
        datos_registro = {
                'tipo_documento': form.tipo_documento.data.strip(),
                'fecha_documento': form.fecha_documento.data,
                'numero_documento': form.numero_documento.data.strip(),
                'descripcion': form.descripcion.data.strip(),
                'numero_inventario': form.numero_inventario.data.strip(),
                'modelo': form.modelo.data.strip(),
                'marca': form.marca.data.strip(),
                'serie': form.serie.data.strip(),    
                'color': form.color.data.strip(),            
                'edificio': form.edificio.data.strip(),
                'piso': form.piso.data.strip(),
                'oficina': form.oficina.data.strip(),
                'fecha_ingreso': form.fecha_ingreso.data,
                'costo_adquisicion': form.costo_adquisicion.data,
                'fecha_ingreso_bien': form.fecha_ingreso_bien.data,
                'comentario': form.comentario.data.strip(),
                'estado_bien': form.estado_bien.data.strip()
        }

        
        estado_valores = validar_valores_no_vacios(datos_registro)
        if estado_valores:
                datos_registro['placa'] = form.placa.data.strip()
                datos_registro['motor'] = form.motor.data.strip()
                datos_registro['municipio'] = form.municipio.data
                datos_registro['departamento'] = form.departamento.data
                datos_registro['numero_chasis'] = form.numero_chasis.data.strip()
                datos_registro['orden_compra'] = form.orden_compra.data.strip()
                datos_registro['departamento_interno'] = form.departamento_interno.data
                datos_registro['modalidad_contratacion'] = form.modalidad_contratacion.data

                # Obtener la lista de imágenes
                imagenes = request.files.getlist('imagen')
               

                # Verificar si se han agregado más de 5 imágenes y que no este vacías
                if imagenes==0:
                    flash("Debes ingresar las imágenes","warning")
                    return render_template('bodega.html', form=form)
                                            
                elif len(imagenes) > 5:
                    flash("Solo se pueden agregar un máximo de 5 imágenes.","warning")
                    return render_template('bodega.html', form=form)
                             
                try:
                        # Subir las imágenes del formulario a Cloudinary
                        imagenes_bien = []
                        for imagen in imagenes:
                        # Verificar la extensión de la imagen
                            estado_imagen = verificar_extension_imagen(imagen.filename)
                            if not estado_imagen:
                                flash("La extensión de una de las imágenes no es válida", "warning")
                                return render_template('bodega.html', form=form)
                            
                        datos_imagenes = agregar_imagenes(imagenes)
                        if datos_imagenes:
                            for dato_imagen in datos_imagenes:
                                imagenes_bien.append({
                                    "secure_url": dato_imagen["secure_url"],
                                    "public_id": dato_imagen["public_id"]
                                })
                            datos_registro["imagenes_bien"] = json.dumps(imagenes_bien)
                except RuntimeError as e:
                        print(f"Error: {str(e)}")
                        flash("No se pudo subir las imágenes. Inténtalo de nuevo", "warning")
                        return render_template('bodega.html', form=form)
                

                estado_registro = db.agregar_registro_bodega_db(datos_registro)
                nombre_usuario = session["nombre_usuario"]+" "+session["apellido_usuario"]

                if estado_registro==True:
                    detalle_actividad = json.dumps(datos_registro, default=convert_date_to_str)
                    db.registrar_accion(session["codigo_usuario"], nombre_usuario, "AGREGAR", "bodega",detalle_actividad)
                    flash("Se agregó exitosamente","success")
                    return redirect(url_for('agregar_bodega_bp.index'))        
                else:
                    if estado_registro=="clave_duplicada":
                        flash("Ya existe ese número de inventario","warning")
                        #return redirect(url_for('agregar_registro_bp.index'))
                        return render_template('bodega.html', form=form)
                    else:
                        flash("No se pudo agregar el registro. Verifique sus datos","warning")
                        #return redirect(url_for('agregar_registro_bp.index'))
                        return render_template('bodega.html', form=form)
        else:
                return render_template('bodega.html', 
                                       mensaje_error='Debes ingresar todos los datos.',
                                       form=form)

        
    return render_template('bodega.html', form=form)