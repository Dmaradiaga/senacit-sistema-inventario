
#Configuraciones de Cloudinary
import cloudinary
import cloudinary.uploader
import re
import bcrypt
from  datetime import date


# Función para validar espacios vacíos
def validar_valores_no_vacios(diccionario):
    # Verificar que cada valor del diccionario no esté vacío si es una cadena
    for valor in diccionario.values():
        if isinstance(valor, str) and not valor.strip():
            return False
    return True


# Validador personalizado para verificar si el archivo es una imagen
def verificar_extension_imagen(campo):
    try:
        extension = campo.split('.')[-1].lower()
        return extension in ['jpg', 'png', 'jpeg']
    except IndexError:
        return False  # Retorna False si no hay extensión


# Validador personalizado para verificar si el archivo es un pdf
def verificar_extension_archivo(campo):
    try:
        extension = campo.split('.')[-1].lower()
        return extension in ['pdf']
    except IndexError:
        return False  # Retorna False si no hay extensión


def convert_date_to_str(obj):
    if isinstance(obj, (date)):
        return obj.isoformat()
    raise TypeError(f"Tipo de dato no serializable: {type(obj)}")


    
#Función para encriptar la contraseña del usuario
def encriptar_contrasena(contrasena):
  # Se genera una cadena aleatoria
  salt = bcrypt.gensalt()

  # Se encripta la contraseña con la cadena aleatoria
  contrasena_encriptada = bcrypt.hashpw(contrasena.encode('utf-8'), salt).decode('utf-8')

  return contrasena_encriptada


# Función para comprobar la hash de la contraseña
def comprobar_hash_contrasena(contrasena_ingresada, contrasena_hash):
        print("contraseña hash: ", contrasena_hash)
        if bcrypt.checkpw(contrasena_ingresada.encode('utf-8'), contrasena_hash.encode('utf-8')):
            print("La contraseña es correcta. ¡Bienvenido!")
            return True        
        else:
            print("Contraseña incorrecta. Por favor, inténtalo de nuevo.")
            return False
      
        
#Función para agregar imagen/es
def agregar_documentos_cloudinary(documentos):
    lista_documentos = []
    # Obtenemos las imágenes del formulario
    documento_formulario = documentos
    for doc in documento_formulario:
        try:
            resultado = cloudinary.uploader.upload(doc, resource_type="auto")
            lista_documentos.append(resultado)
        except cloudinary.exceptions.Error as e:
            # Manejar el error en caso de que falle la subida de la imagen
            print(f"Error al subir el documento {doc.filename} a Cloudinary: {str(e)}")
            # Lanzar una excepción para indicar que la subida de la imagen falló
            raise RuntimeError("No se pudo subir el documento a Cloudinary")
    return lista_documentos


#Función para agregar imágenes
def agregar_imagenes(imagenes):
    lista_imagenes = []
    # Obtenemos las imágenes del formulario
    imagenes_formulario = imagenes
    for image in imagenes_formulario:
        try:
            resultado = cloudinary.uploader.upload(image)
            lista_imagenes.append(resultado)
        except cloudinary.exceptions.Error as e:
            # Manejar el error en caso de que falle la subida de la imagen
            print(f"Error al subir la imagen {image.filename} a Cloudinary: {str(e)}")
            # Lanzar una excepción para indicar que la subida de la imagen falló
            raise RuntimeError("No se pudo subir la imagen a Cloudinary")
    return lista_imagenes


#Función para editar imagenes en cloudinary
def editar_imagen(image, public_id):
    try:
        # Subir la imagen editada a Cloudinary utilizando su ID
        result = cloudinary.uploader.upload(image, public_id=public_id)

        # Extraer la URL segura de la imagen editada
        secure_url = result['secure_url']

        # Retornar la URL segura y el ID de la imagen
        return secure_url
    except cloudinary.exceptions.Error as e:
        # Manejar el error en caso de que falle la edición de la imagen
        print(f"Error al editar la imagen en Cloudinary: {str(e)}")
        raise RuntimeError("No se pudo editar la imagen en Cloudinary")
    

def eliminar_documento_cloudinary(id_url_documento):
    try:
        # Intentar eliminar como imagen/video
        resultado = cloudinary.uploader.destroy(id_url_documento)
        if resultado.get("result") == "ok":
            print(f"Archivo eliminado como imagen/video: {id_url_documento}")
            return True

        # Si falla, intentar eliminar como archivo raw
        resultado = cloudinary.uploader.destroy(id_url_documento, resource_type="raw")
        if resultado.get("result") == "ok":
            print(f"Archivo eliminado como raw: {id_url_documento}")
            return True

        print(f"No se pudo eliminar el archivo: {id_url_documento}")
        return False
    except cloudinary.exceptions.NotFound:
        print(f"Archivo no encontrado: {id_url_documento}")
        return False
    except cloudinary.exceptions.Error as e:
        print(f"Error de Cloudinary al eliminar el archivo: {str(e)}")
        return False
    except Exception as e:
        print(f"Error inesperado al eliminar el archivo: {str(e)}")
        return False
    


#Función para editar documento en  cloudinary
def reenviar_documento_cloudinary(documento, id_url_documento):
    try:
        # Subir el documento a cloudinary, utilizando el public_id
        resultado = cloudinary.uploader.upload(documento, 
                                               public_id=id_url_documento,
                                               resource_type="auto")

        # Extra la URL segura del documento editado
        secure_url = resultado['secure_url']
        # Retornar la URL segura
        return secure_url,True
        
    except cloudinary.exceptions.Error as e:
        # Manejar el error en caso de que falle la edición de la imagen
        print(f"Error al editar el documento en Cloudinary: {str(e)}")
        return False
    

def verificar_correo(correo):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(patron, correo):
        return True
    else:
        return False
    

    
#Válida que el número de identidad sea un dígito y además
# solamente tenga 13 dígitos.
def validar_numero_identidad(numero_identidad):
    # Convertir a string si es un entero
    numero_identidad = str(numero_identidad)
    
    if not numero_identidad.isdigit():
        return False
    if len(numero_identidad) != 13:
        return False
    return True


#Formatear el número de identidad
def formatear_numero_identidad(numero_identidad):
    return f"{numero_identidad[:4]}-{numero_identidad[4:8]}-{numero_identidad[8:]}"


def ajustar_texto(texto, ancho_maximo, fuente, tamanio_fuente):
   palabras = texto.split()
   lineas = []
   linea_actual = ""

   for palabra in palabras:
       nueva_linea = linea_actual + palabra + " "
       if fuente.stringWidth(nueva_linea, tamanio_fuente) <= ancho_maximo:
           linea_actual = nueva_linea
       else:
           lineas.append(linea_actual.strip())
           linea_actual = palabra + " "

   if linea_actual:
       lineas.append(linea_actual.strip())

   return lineas