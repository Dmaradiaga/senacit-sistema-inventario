
from app.funciones_ayuda.funciones_ayuda import verificar_correo, validar_numero_identidad, encriptar_contrasena
from app.db.db import db

def agregar_admin():

    print("\n\nAgregando Administrador\n\n")

    nombre = str(input("Ingresa el nombre: "))
    apellido = str(input("Ingresa el apellido: "))
    numero_identidad = str(input("Ingresa el numero_identidad (sin guiones): "))
    rol_usuario = "Administrador"
    departamento_interno = str(input("Ingresa el departamento: "))
    contrasena = str(input("Ingresa la contrasena: "))
    correo = str(input("Ingresa el correo: "))

    if not correo or not contrasena or not departamento_interno or not rol_usuario or \
       not numero_identidad or not apellido or not nombre:
        print("\n Debes ingresar los datos del usuario \n")
        return
    if not verificar_correo(correo):
       print("\n Ingresa un correo válido \n")
       return

    if not validar_numero_identidad(numero_identidad):
        print("\n Número de identidad inválido \n")
        return
    
    contrasena_encriptada = encriptar_contrasena(contrasena)

    datos_usuario = {
            "contrasena": contrasena_encriptada,
            "numero_identidad": numero_identidad,
            "nombre": nombre,
            "apellido": apellido,
            "rol_usuario": rol_usuario,
            "es_tecnico":0,
            "correo":correo,
            "es_jefe_departamento":1,
            "departamento_interno": departamento_interno
        }
    
    estado_consulta = db.agregar_usuario(datos_usuario)
    if estado_consulta==True:
        print("\n El usuario se agregó correctamente \n")
        print("\n\n\n")
        return
    else:
        if estado_consulta=="clave_duplicada":
            print("\nEse correo ya existe\n")
            print("\n\n\n")
            return
        else:
            print("\nNo se pudo agregar el usuario\n")
            print("\n\n\n")
            return
        

agregar_admin()

#Primero ejecutar: python run.py
# Segundo: python agregar_admin.py
#Tercero: reiniciar el servidor para que pueda ingresar al sistema