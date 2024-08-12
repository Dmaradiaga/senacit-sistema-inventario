
from flask import Blueprint, render_template,flash,url_for,redirect,session, request
from app.db.db import db
from app.perfil_usuario.forms.editar_perfil_usuario_formulario import EditarPerfilUsuarioFormulario
from app.autorizacion.autorizacon_blueprint import comprobando_autorizacion,comprobando_sesion_administrador
from app.funciones_ayuda.funciones_ayuda import agregar_imagenes,editar_imagen,validar_valores_no_vacios,\
verificar_correo,encriptar_contrasena,verificar_extension_imagen,validar_numero_identidad



perfil_usuario_bp = Blueprint('perfil_usuario_bp', __name__,
    template_folder='templates',
    static_folder='static')

        
# Ruta principal del blueprint
@perfil_usuario_bp.route('/', methods=["GET", "POST"])
@comprobando_autorizacion
def index():
    numero_identidad_usuario = session["codigo_usuario"]
    # Llamar a la función para mostrar los datos del usuario por número de identidad
    datos_usuario = db.mostrar_datos_usuarios(numero_identidad_usuario)

    if datos_usuario:
        # Desempaquetar los datos del usuario
        nombre, apellido, rol_usuario, departamento_interno, numero_identidad,url_firma_imagen, correo= datos_usuario

        # Renderizar el template "perfil_usuario.html" pasando los datos del usuario
        return render_template("perfil_usuario.html", nombre=nombre, apellido=apellido, rol_usuario=rol_usuario, 
                               departamento_interno=departamento_interno, 
                               numero_identidad=numero_identidad,url_firma_imagen=url_firma_imagen, correo=correo)
    else:
        # En caso de que no se encuentren los datos del usuario, manejar el error adecuadamente
        flash("No se encontraron datos de usuario.", "warning")
        return render_template("perfil_usuario.html",error="Vuelve a intentarlo")



@perfil_usuario_bp.route('/editar_perfil_usuario', methods=["GET", "POST"])
@comprobando_autorizacion
def editar_perfil_usuario():
    form = EditarPerfilUsuarioFormulario()
    
    numero_identidad = session["codigo_usuario"]
    apellido_usuario = session["apellido_usuario"]
    nombre_usuario = session["nombre_usuario"]
    departamento_interno = session["departamento_interno"]
    id_usuario = session["id_usuario"]
    id_imagen_url = session["id_imagen_url"]
    correo = session["correo"]
    url_firma_imagen = session["url_firma_imagen"]
    


    if request.method == "POST":
        datos_usuario = {
            "numero_identidad": form.numero_identidad.data,
            "nombre": form.nombre.data.strip(),
            "apellido": form.apellido.data.strip(),
            "departamento_interno": form.departamento_interno.data
        }

        # Verificar si se proporcionó una contraseña y agregarla a los datos del usuario si existe
        if form.contrasena.data:
            datos_usuario["contrasena"] = form.contrasena.data.strip()

        #Verificar el correo
        correo = form.correo.data.strip()
        if correo and verificar_correo(correo):
            datos_usuario["correo"] = correo
            session["correo"] = correo
        else:
            flash("Ingresa un correo válido", "warning")
            return render_template('editar_perfil_usuario.html', form=form,url_firma_imagen=url_firma_imagen)
        

        # Verificar si se proporcionó una imagen y si es válida
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            print("IMAGEN QUE SE VA A SUBIR: ", imagen)
            
            if imagen:
                estado_imagen = verificar_extension_imagen(imagen.filename)
                if estado_imagen:
                    if id_imagen_url is None:
                        try:
                            # Subir la imagen del formulario a Cloudinary
                            imagenes_subidas = agregar_imagenes([imagen])
                            if imagenes_subidas:
                                datos_usuario["url_firma_imagen"] = imagenes_subidas[0]["secure_url"]
                                datos_usuario["id_imagen_url"] = imagenes_subidas[0]["public_id"]
                                session["url_firma_imagen"] = imagenes_subidas[0]["secure_url"]
                                session["id_imagen_url"] = imagenes_subidas[0]["public_id"]
                        except RuntimeError as e:
                            print(f"Error causado por: {str(e)}")
                            flash("No se pudo subir la imagen. Inténtalo de nuevo", "warning")
                            return render_template('editar_perfil_usuario.html', form=form,url_firma_imagen=url_firma_imagen)
                    else:
                        try:
                            # Subir la imagen para editar del formulario a Cloudinary
                            nueva_url_imagen = editar_imagen(imagen, id_imagen_url)
                            print(nueva_url_imagen)
                            if nueva_url_imagen:
                                datos_usuario["url_firma_imagen"] = nueva_url_imagen
                                session["url_firma_imagen"] = datos_usuario["url_firma_imagen"]
                                #session["id_imagen_url"] = uploaded_images[0]["public_id"]
                            # datos_usuario["id_imagen_url"] = uploaded_images[0]["public_id"]
                        except RuntimeError as e:
                            flash("No se pudo subir la imagen. Inténtalo de nuevo", "warning")
                            return render_template('editar_perfil_usuario.html', form=form,url_firma_imagen=url_firma_imagen)
                else:
                    flash("Formato de imagen no válido. Solo se permiten archivos PNG, JPG, JPEG", "warning")
                    return render_template('editar_perfil_usuario.html', form=form,url_firma_imagen=url_firma_imagen)

        # Validar que se ingresen los datos necesarios
        estado_valores = validar_valores_no_vacios(datos_usuario)
        if estado_valores:

            es_numero_identidad = validar_numero_identidad(datos_usuario["numero_identidad"])
            if not es_numero_identidad:
                flash("Debes ingresar un número de identidad válido","warning")
                return render_template('editar_perfil_usuario.html',form=form,url_firma_imagen=url_firma_imagen)
            
            # Encriptar la contraseña si se proporcionó
            if "contrasena" in datos_usuario:
                contrasena_encriptada = encriptar_contrasena(datos_usuario["contrasena"])
                datos_usuario["contrasena"] = contrasena_encriptada

            session["codigo_usuario"] = form.numero_identidad.data
            session["apellido_usuario"] = form.apellido.data.strip()
            session["nombre_usuario"] = form.nombre.data.strip()
            session["departamento_interno"] = form.departamento_interno.data
            
            # Editar los datos del usuario en la base de datos
            estado_consulta = db.editar_datos_usuario(datos_usuario, id_usuario)
            if estado_consulta:
                flash("Se editaron los datos correctamente.", "success")
                return redirect(url_for('perfil_usuario_bp.index'))
            else:
                flash("No se pudo editar los datos.", "warning")
                return render_template('editar_perfil_usuario.html', form=form,url_firma_imagen=url_firma_imagen)
        else:
            flash("Debes ingresar los datos", "warning")
            return render_template('editar_perfil_usuario.html', form=form,url_firma_imagen=url_firma_imagen)

    
    form.nombre.data = nombre_usuario
    form.apellido.data = apellido_usuario
    form.departamento_interno.data = departamento_interno
    form.numero_identidad.data = numero_identidad
    form.correo.data = correo

    return render_template("editar_perfil_usuario.html", form=form, url_firma_imagen=url_firma_imagen)
    

