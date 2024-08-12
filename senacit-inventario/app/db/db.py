import pymysql
#import time

#Clase SenacitInventarioDB del sistema de  inventario
class SenacitInventarioDB:
    def __init__(self, host, user, password, database):
        """
        Constructor de la clase SenacitInventarioDB.
        
        Parámetros:
            - host: El host de la base de datos.
            - user: El usuario de la base de datos.
            - password: La contraseña del usuario de la base de datos.
            - database: El nombre de la base de datos.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None



    def connect(self):
            try:
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    charset='utf8mb4',
                    use_unicode=True,
                )
                print("Conexión exitosa a la base de datos")
                return
            except pymysql.err.InterfaceError as e:
                print(f"Error al tratar de conectar a la db: {e}")
            except pymysql.MySQLError as e:
                print(f"MySQLError: {e}")



    def registrar_accion(self, numero_identidad_usuario, nombre_usuario, tipo_operacion, 
                         nombre_tabla,detalle_actividad):
        if self.connection is None:
            print("No se puede registrar la acción porque la conexión a la base de datos no está establecida.")
            return

        try:
            cursor = self.connection.cursor()
            sql = """
                INSERT INTO bitacora 
                (numero_identidad_usuario, nombre_usuario, tipo_operacion, nombre_tabla, detalle_actividad)
                VALUES (%s, %s, %s,%s, %s)
                """
            cursor.execute(sql, (numero_identidad_usuario, nombre_usuario, tipo_operacion,nombre_tabla,
                                 detalle_actividad))
            self.connection.commit()
            print("Acción registrada en la bitácora.")
        except pymysql.MySQLError as e:
            print(f"Error registrando la acción: {str(e)}")
            self.connection.rollback()




    #Método que cierra la conexión con la base de datos
    def close(self):
        """
        Método para cerrar la conexión a la base de datos.
        """
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")
 
    #Método para buscar un registro en la tabla inventario y posteriormente actualizarlo
    def buscar_registro_por_numero_inventario(self, numero_inventario):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar el registro por orden de compra
            query = """
                        SELECT *,  
                        DATE_FORMAT(fecha_ingreso, '%%Y-%%m-%%d') AS fecha_ingreso_formateada,
                        DATE_FORMAT(fecha_ingreso_bien, '%%Y-%%m-%%d') AS fecha_ingreso_bien_formateada,
                        DATE_FORMAT(fecha_documento, '%%Y-%%m-%%d') AS fecha_documento_formateada
                        FROM inventario
                        WHERE numero_inventario = %s 
                """
            cursor.execute(query, (numero_inventario))

            # Obtener el registro de la base de datos
            registro = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

            return registro  # Devolver el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro por orden de compra: {e}")
            return None  # Devolver None si ocurre algún error


    #Método para buscar un registro ne la tabla bodega y posteriormente actualizarlo
    def buscar_registro_por_numero_inventario_bodega(self, numero_inventario):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar el registro por orden de compra
            query = """
                        SELECT *,  
                        DATE_FORMAT(fecha_ingreso, '%%Y-%%m-%%d') AS fecha_ingreso_formateada,
                        DATE_FORMAT(fecha_ingreso_bien, '%%Y-%%m-%%d') AS fecha_ingreso_bien_formateada,
                        DATE_FORMAT(fecha_documento, '%%Y-%%m-%%d') AS fecha_documento_formateada
                        FROM bodega
                        WHERE numero_inventario = %s 
                """
            cursor.execute(query, (numero_inventario))

            # Obtener el registro de la base de datos
            registro = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

            return registro  # Devolver el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro por número de inventario: {e}")
            return None  # Devolver None si ocurre algún error
        
   

    # Método para consultar registro por número de inventario
    def mostrar_registro_por_numero_inventario(self, numero_inventario):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar el registro por número de inventario
            consulta = """
                    SELECT tipo_documento,numero_documento,descripcion,
                    numero_inventario,modelo,marca,serie,placa,motor,numero_chasis,
                    color,departamento,municipio,edificio,piso,orden_compra,fecha_ingreso,
                    costo_adquisicion,modalidad_contratacion,comentario,
                    estado_bien,oficina,fecha_documento,fecha_registro_inventario,
                    usuarios.nombre,usuarios.apellido,usuarios.numero_identidad,fecha_ingreso_bien,
                    imagenes_bien
                    FROM inventario
                    INNER JOIN usuarios ON inventario.numero_identidad = usuarios.numero_identidad
                    WHERE inventario.numero_inventario  = %s
                """
            cursor.execute(consulta, (str(numero_inventario),))

            # Obtener el registro de la base de datos
            registro = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

            return registro  # Devolver el registro encontrado
        except Exception as e:
            print(f"Error al buscar el registro por número de inventario: {e}")
            return None  # Devolver None si ocurre algún error

    

    #Método para consultar registro por numero de inventario
    def mostrar_registro_por_numero_inventario_bodega(self, numero_inventario):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()
            consulta = """
                    SELECT tipo_documento,numero_documento,descripcion,
                    numero_inventario,modelo,marca,serie,placa,motor,numero_chasis,
                    color,departamento,municipio,edificio,piso,orden_compra,fecha_ingreso,
                    costo_adquisicion,modalidad_contratacion,comentario,
                    estado_bien,oficina,fecha_documento,fecha_registro_bodega,
                    fecha_ingreso_bien,imagenes_bien
                    FROM bodega
                    WHERE numero_inventario  = %s
                """

            cursor.execute(consulta, (str(numero_inventario),))

            # Obtener el registro de la base de datos
            registro = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

            return registro  # Devolver el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro por numero de inventario: {e}")
            return None  # Devolver None si ocurre algún error
        
        
    #Método que muestra un registro por número de inventario
    def registros_por_numero_inventario(self, numero_inventario):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar el registro por orden de compra
            query = """
                        SELECT *,  
                        DATE_FORMAT(fecha_ingreso, '%%Y-%%m-%%d') AS fecha_ingreso_formateada,
                        DATE_FORMAT(fecha_ingreso_bien, '%%Y-%%m-%%d') AS fecha_ingreso_bien_formateada,
                        DATE_FORMAT(fecha_documento, '%%Y-%%m-%%d') AS fecha_documento_formateada
                        FROM inventario
                        WHERE numero_inventario = %s 
                """
            cursor.execute(query, (numero_inventario))

            # Obtener el registro de la base de datos
            registro = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

            return registro  # Devolver el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro por orden de compra: {e}")
            return None  # Devolver None si ocurre algún error       


    #Método para agregar un registro en la base de datos
    def agregar_registro_db(self,datos_registro):
        try:
            # Crear el cursor
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para insertar un nuevo registro en la tabla
            # Consulta SQL para el INSERT
            consulta = "INSERT INTO inventario ("
            columnas = ", ".join(datos_registro.keys())
            valores = "', '".join(map(str, datos_registro.values()))
            consulta += f"{columnas}) VALUES ('{valores}')"

            # Ejecutar la consulta SQL
            cursor.execute(consulta)

            # Confirmar la transacción
            self.connection.commit()

            # Cerrar el cursor
            cursor.close()

            return True  # Éxito al agregar el registro a la base de datos

        except pymysql.IntegrityError as e:
            if e.args[0] == 1062:  # Código de error para clave duplicada
                print("Error: Clave duplicada. No se pudo agregar el registro.")
                return "clave_duplicada"
        except Exception as e:
            print(f"Error al agregar el registro a la tabla inventario: {e}")
            return False  # Error al agregar el registro a la base de datos
        
    #Método para actualizar un registro en la base de datos
    def editar_datos_inventario(self, datos_actualizar, id_inventario):
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE inventario SET "
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Eliminar la coma y el espacio sobrantes
        consulta += f" WHERE id_inventario = '{id_inventario}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Datos actualizados correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar los datos: {str(e)}")
            return False


       #Método para actualizar un registro en la base de datos
    
    #Método para editar los datos de la bodega
    def editar_datos_bodega(self, datos_actualizar, id_bodega):
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE bodega SET "
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Elimina la coma y el espacio sobrantes
        consulta += f" WHERE id_bodega = '{id_bodega}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Datos actualizados correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar los datos: {str(e)}")
            return False

    #Método para editar los campos de la tabla usuarios    
    def editar_datos_usuario(self, datos_actualizar, id_usuario):
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE usuarios SET "
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Elimina la coma y el espacio sobrantes
        consulta += f" WHERE id_usuario = '{id_usuario}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Datos actualizados correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar los datos: {str(e)}")
            return False
        

    #Método buscar un registro por el número de identidad
    def mostrar_registro_por_numero_identidad(self, numero_identidad):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros por numero de identidad
            consulta = """
            SELECT 
                u.nombre, 
                u.apellido, 
                u.numero_identidad, 
                DATE_FORMAT(i.fecha_registro_inventario, '%%Y-%%m-%%d') as 'fecha_registro_inventario',
                DATE_FORMAT(i.fecha_ingreso_bien, '%%Y-%%m-%%d') as 'fecha_ingreso_bien',
                DATE_FORMAT(i.fecha_ingreso, '%%Y-%%m-%%d') as 'fecha_ingreso',
                DATE_FORMAT(i.fecha_documento, '%%Y-%%m-%%d') as 'fecha_documento',
                i.numero_documento, 
                i.descripcion,
                i.numero_inventario,
                i.tipo_documento,
                i.modelo,i.serie,
                i.marca,i.placa,i.motor,
                i.numero_chasis,i.color,i.departamento,
                i.municipio,i.departamento_interno,
                i.edificio,i.piso,i.orden_compra,
                i.costo_adquisicion,
                i.modalidad_contratacion,i.comentario,
                i.estado_bien,i.oficina,i.imagenes_bien
                FROM usuarios u
                INNER JOIN inventario i ON u.numero_identidad = i.numero_identidad
                WHERE u.numero_identidad = %s
                ORDER BY i.fecha_registro_inventario DESC
            """

            cursor.execute(consulta, (numero_identidad))

            # Obtener los registros de la tabla inventario y usuario
            registros_retornados = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            return registros_retornados  # Devuelve los registros encontrados

        except Exception as e:
            print(f"Error al buscar los registros por numero de identidad[DB]: {e}")
            return None  # Devolver None si ocurre algún error

    #Método para mostrar lso datos del usuario
    def mostrar_datos_usuarios(self, numero_identidad):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros por número de identidad 
            # en la tabla de usuarios
            consulta = """
                SELECT 
                    nombre,
                    apellido,
                    rol_usuario,
                    departamento_interno,
                    numero_identidad,url_firma_imagen, correo
                FROM usuarios
                WHERE numero_identidad = %s
                """

            cursor.execute(consulta, (numero_identidad,))

            # Obtener el registro de la tabla usuarios
            registro_retornado = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

            return registro_retornado  # Devuelve el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro por número de identidad en la tabla usuarios [DB]: {e}")
            return None  # Devolver None si ocurre algún error

  
    def mostrar_solicitudes_descargo_jefe_departamento(self, departamento_interno):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros por departamento_interno 
            # en la tabla de solicitud_descargo
            consulta = """
                SELECT 
                    *
                FROM solicitud_descargo
                WHERE departamento_interno = %s 
                """

            cursor.execute(consulta, (departamento_interno))

            # Obtener el registro de la tabla usuarios
            registros_retornados = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            return registros_retornados  # Devuelve el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro por número de identidad en la tabla usuarios [DB]: {e}")
            return None  # Devolver None si ocurre algún error
        

    def mostrar_solicitudes_descargo_tenico_departamento(self, departamento_interno):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros por departamento_interno 
            # en la tabla de solicitud_descargo
            consulta = """
                SELECT 
                    *
                FROM solicitud_descargo
                WHERE departamento_interno = %s 
                """

            cursor.execute(consulta, (departamento_interno))

            # Obtener el registro de la tabla usuarios
            registros_retornados = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            return registros_retornados  # Devuelve el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro por número de identidad en la tabla usuarios [DB]: {e}")
            return None  # Devolver None si ocurre algún error
        

        
 
    def mostrar_solicitudes_traslado_jefe_departamento(self, departamento_interno):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros por departamento_interno 
            # en la tabla de solicitud_traslado
            consulta = """
                SELECT 
                    *
                FROM solicitud_traslado
                WHERE departamento_interno = %s 
                """

            cursor.execute(consulta, (departamento_interno))

            # Obtener el registro de la tabla usuarios
            registros_retornados = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            return registros_retornados  # Devuelve el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro: {e}")
            return None  # Devolver None si ocurre algún error
        

  
    def mostrar_solicitudes_descargo(self):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros  
            # en la tabla de solicitud_descargo
            consulta = """
                SELECT 
                    *
                FROM solicitud_descargo
                ORDER BY fecha_solicitud DESC
                """

            cursor.execute(consulta)

            # Obtener el registro de la tabla usuarios
            registros_retornados = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            return registros_retornados  # Devuelve el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro : {e}")
            return None  # Devolver None si ocurre algún error


    def mostrar_solicitudes_traslado(self):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros  
            # en la tabla de solicitud_descargo
            consulta = """
                SELECT 
                    *
                FROM solicitud_traslado
                ORDER BY fecha_solicitud DESC
                """

            cursor.execute(consulta)

            # Obtener el registro de la tabla usuarios
            registros_retornados = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            return registros_retornados  # Devuelve el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro : {e}")
            return None  # Devolver None si ocurre algún error
        
   
    def mostrar_solicitudes_descargo_id_solicitud_descargo(self,id_solicitud_descargo):

        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros  
            # en la tabla de solicitud_descargo
            consulta = """
                SELECT 
                    *
                FROM solicitud_descargo
                WHERE
                id_solicitud_descargo = %s
                ORDER BY fecha_solicitud DESC
                """

            cursor.execute(consulta,(id_solicitud_descargo))

            # Obtener el registro de la tabla usuarios
            registros_retornados = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

            return registros_retornados  # Devuelve el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro {e}")
            return None  # Devolver None si ocurre algún error 
        
    
    def mostrar_solicitudes_traslado_id_solicitud_traslado(self,id_solicitud_traslado):

        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros  
            # en la tabla de solicitud_descargo
            consulta = """
                SELECT 
                    *
                FROM solicitud_traslado
                WHERE
                id_solicitud_traslado = %s
                ORDER BY fecha_solicitud DESC
                """

            cursor.execute(consulta,(id_solicitud_traslado))

            # Obtener el registro de la tabla usuarios
            registros_retornados = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

            return registros_retornados  # Devuelve el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro {e}")
            return None  # Devolver None si ocurre algún error 
        
 
    def mostrar_solicitudes_descargo_numero_identidad(self,numero_identidad):

        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros  
            # en la tabla de solicitud_descargo
            consulta = """
                SELECT 
                    *
                FROM solicitud_descargo
                WHERE
                numero_identidad_solicitante = %s
                ORDER BY fecha_solicitud DESC;
                """

            cursor.execute(consulta,(numero_identidad))

            # Obtener el registro de la tabla usuarios
            registros_retornados = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            return registros_retornados  # Devuelve el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro por número de identidad en la tabla:  {e}")
            return None  # Devolver None si ocurre algún error    


    def mostrar_solicitudes_traslado_numero_identidad(self,numero_identidad):

        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros  
            # en la tabla de solicitud_descargo
            consulta = """
                SELECT 
                    *
                FROM solicitud_traslado
                WHERE
                numero_identidad_solicitante = %s
                ORDER BY fecha_solicitud DESC;
                """

            cursor.execute(consulta,(numero_identidad))

            # Obtener el registro de la tabla usuarios
            registros_retornados = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()

            return registros_retornados  # Devuelve el registro encontrado

        except Exception as e:
            print(f"Error al buscar el registro por número de identidad en la tabla:  {e}")
            return None  # Devolver None si ocurre algún error
        

    #Método loguearse al sistema
    def login_inventario(self,numero_identidad):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar el usuario por número de identidad y 
            #contraseña  
            consulta = """
                    SELECT nombre, apellido, numero_identidad,
                    contrasena, rol_usuario, departamento_interno,id_usuario,
                    id_imagen_url, url_firma_imagen,es_jefe_departamento, es_tecnico, correo
                    FROM usuarios
                    WHERE numero_identidad  = %s and estado_usuario = 1
                """

            cursor.execute(consulta, (numero_identidad))

            # Obtener el registro de la base de datos
            registro = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()

            print("Se han creado las variables de nombre_usuario y codigo_usuario")
            return registro  # Devolver el registro encontrado

        except Exception as e:
            print(f"Error al comprobar el usuario: {e}")
            return None  # Devolver None si ocurre algún error

    #Método para agregar un usuario
    def agregar_usuario(self,datos_usuario):
        try:
            # Crear el cursor
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para insertar un nuevo usuario en la tabla usuarios
            consulta = "INSERT INTO usuarios ("
            columnas = ", ".join(datos_usuario.keys())
            valores = "', '".join(map(str, datos_usuario.values()))
            consulta += f"{columnas}) VALUES ('{valores}')"

            # Ejecutar la consulta SQL
            cursor.execute(consulta)

            # Confirmar la transacción
            self.connection.commit()

            # Cerrar el cursor
            cursor.close()

            return True  # Éxito al agregar el registro a la base de datos
        except pymysql.IntegrityError as e:
            if e.args[0] == 1062:  # Código de error para clave duplicada
                print("Error: Clave duplicada. No se pudo agregar el usuario.")
                return "clave_duplicada"
        except Exception as e:
            print(f"Error al agregar el usuario a la tabla usuarios: {e}")
            return False  # Error al agregar el registro a la base de datos

    #Método para guardar la solicitud de descargo
    def agregar_solicitud_descargo(self,datos_solicitud_descargo):
        try:
            # Crear el cursor
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para insertar un nuevo registro en la tabla solicitud_descargo
            consulta = "INSERT INTO solicitud_descargo ("
            columnas = ", ".join(datos_solicitud_descargo.keys())
            valores = "', '".join(map(str, datos_solicitud_descargo.values()))
            consulta += f"{columnas}) VALUES ('{valores}')"

            print(consulta)
            # Ejecutar la consulta SQL
            cursor.execute(consulta)

            # Confirmar la transacción
            self.connection.commit()

            # Cerrar el cursor
            cursor.close()

            return True  # Éxito al agregar el registro a la base de datos

        except Exception as e:
            print(f"Error al agregar el registro a la tabla solicitud_descargo: {e}")
            return False  # Error al agregar el registro a la base de datos

    #Método agregar el dictamen en la solicitud de descargo
    def agregar_dictamen_solicitud_descargo(self,datos_editar,id_solicitud_descargo):
    
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE solicitud_descargo SET "
        for columna, valor in datos_editar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Elimina la coma y el espacio sobrantes
        consulta += f" WHERE id_solicitud_descargo = '{id_solicitud_descargo}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Datos actualizados correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar los datos: {str(e)}")
            return False
        
    #Método para guardar la solicitud de traslado
    def agregar_solicitud_traslado(self,datos_solicitud_traslado):
        try:
            # Crear el cursor
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para insertar un nuevo registro en la tabla solicitud_traslado
            consulta = "INSERT INTO solicitud_traslado ("
            columnas = ", ".join(datos_solicitud_traslado.keys())
            valores = "', '".join(map(str, datos_solicitud_traslado.values()))
            consulta += f"{columnas}) VALUES ('{valores}')"

            print(consulta)
            # Ejecutar la consulta SQL
            cursor.execute(consulta)

            # Confirmar la transacción
            self.connection.commit()

            # Cerrar el cursor
            cursor.close()

            return True  # Éxito al agregar el registro a la base de datos

        except Exception as e:
            print(f"Error al agregar el registro en la tabla solicitud de traslado: {e}")
            return False  # Error al agregar el registro a la base de datos


    #Método para agregar un registro a la tabla bodega
    def agregar_registro_bodega_db(self,datos_bodega):
        try:
            # Crear el cursor
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para insertar un nuevo registro en la tabla bodega
            # Consulta SQL para el INSERT
            consulta = "INSERT INTO bodega ("
            columnas = ", ".join(datos_bodega.keys())
            valores = "', '".join(map(str, datos_bodega.values()))
            consulta += f"{columnas}) VALUES ('{valores}')"

            # Ejecutar la consulta SQL
            cursor.execute(consulta)

            # Confirmar la transacción
            self.connection.commit()

            # Cerrar el cursor
            cursor.close()

            return True  # Éxito al agregar el registro a la base de datos

        except pymysql.IntegrityError as e:
            if e.args[0] == 1062:  # Código de error para clave duplicada
                print("Error: Clave duplicada. No se pudo agregar el registro.")
                return "clave_duplicada"
        except Exception as e:
            print(f"Error al agregar el registro a la tabla bodega: {e}")
            return False  # Error al agregar el registro a la base de datos


    #Método para actualizar un registro en la tabla de descargo
    def editar_solicitud_descargo(self, datos_actualizar, id_solicitud_descargo):
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE solicitud_descargo SET "
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Eliminar la coma y el espacio sobrantes
        consulta += f" WHERE id_solicitud_descargo = '{id_solicitud_descargo}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Datos actualizados correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar los datos: {str(e)}")
            return False
    

    #Método para actualizar un registro en la tabla de descargo
    def editar_solicitud_traslado(self, datos_actualizar, id_solicitud_traslado):
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE solicitud_traslado SET "
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Eliminar la coma y el espacio sobrantes
        consulta += f" WHERE id_solicitud_traslado = '{id_solicitud_traslado}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Datos actualizados correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar los datos: {str(e)}")
            return False
        

    #Método para aprobar la solicitude de descargo
    def aprobar_solicitud_descargo(self, datos_actualizar, id_solicitud_descargo):
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE solicitud_descargo SET "
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Eliminar la coma y el espacio sobrantes
        consulta += f" WHERE id_solicitud_descargo = '{id_solicitud_descargo}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Datos actualizados correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar los datos: {str(e)}")
            return False
        
    
    #Método para aprobar la solicitud de  traslado
    def aprobar_solicitud_traslado(self, datos_actualizar, id_solicitud_traslado):
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE solicitud_traslado SET "
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Eliminar la coma y el espacio sobrantes
        consulta += f" WHERE id_solicitud_traslado = '{id_solicitud_traslado}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Datos actualizados correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar los datos: {str(e)}")
            return False
        

    #Método para eliminar un registro en la tabla de descargo
    def eliminar_solicitud_descargo(self, id_solicitud_descargo):
        # Consulta SQL para eliminar un registro de la tabla solicitud_descargo
        consulta = "DELETE FROM solicitud_descargo WHERE id_solicitud_descargo = %s"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta,(id_solicitud_descargo))
            self.connection.commit()
            cursor.close()
            print("Registro eliminado correctamente.")
            return True
        except Exception as e:
            print(f"Error al eliminar el registro: {str(e)}")
            return False
        

    #Método para eliminar un registro en la tabla de usuarios
    def eliminar_usuario(self, id_usuario):
        # Consulta SQL para eliminar un registro de la tabla usuarios
        consulta = "DELETE FROM usuarios WHERE id_usuario = %s"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta,(id_usuario))
            self.connection.commit()
            cursor.close()
            print("Registro eliminado correctamente.")
            return True
        except pymysql.err.IntegrityError as e:
            print(f"Error de integración: str({e})")
            return 2
        except Exception as e:
            print(f"Error al eliminar el registro: {str(e)}")
            return False
    


    #Método para eliminar un registro en la tabla de descargo
    def eliminar_solicitud_traslado(self, id_solicitud_traslado):
        # Consulta SQL para eliminar un registro de la tabla solicitud_descargo
        consulta = "DELETE FROM solicitud_traslado WHERE id_solicitud_traslado = %s"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta,(id_solicitud_traslado))
            self.connection.commit()
            cursor.close()
            print("Registro eliminado correctamente.")
            return True
        except Exception as e:
            print(f"Error al eliminar el registro: {str(e)}")
            return False
        

    def mostrar_informacion_usuario(self, numero_identidad):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar el registro
            # en la tabla usuarios
            consulta = """
                SELECT 
                    nombre, apellido,rol_usuario,estado_usuario,
                    es_jefe_departamento,es_tecnico,id_usuario
                FROM usuarios
                WHERE numero_identidad = %s
                """
            cursor.execute(consulta,(numero_identidad))
            # Obtener el registro de la tabla usuarios
            registro_retornado = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()
            return registro_retornado  # Devuelve los registros encontrados

        except Exception as e:
            print(f"Error al retornar el registro: {e}")
            return None  # Devolver None si ocurre algún error
        
    
    #Método para actualizar un registro en la tabla de usuarios
    def editar_estado_usuario(self, datos_actualizar, id_usuario):
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE usuarios SET "
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Eliminar la coma y el espacio sobrantes
        consulta += f" WHERE id_usuario = '{id_usuario}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Dato actualizado correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar el registro: {str(e)}")
            return False
        

    #Método para guardar la solicitud de traslado
    def agregar_documentos(self,datos_documentos):
        try:
            # Crear el cursor
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para insertar un nuevo registro en la tabla solicitud_traslado
            consulta = "INSERT INTO documentos ("
            columnas = ", ".join(datos_documentos.keys())
            valores = "', '".join(map(str, datos_documentos.values()))
            consulta += f"{columnas}) VALUES ('{valores}')"

            print(consulta)
            # Ejecutar la consulta SQL
            cursor.execute(consulta)

            # Confirmar la transacción
            self.connection.commit()

            # Cerrar el cursor
            cursor.close()

            return True  # Éxito al agregar el registro a la base de datos

        except Exception as e:
            print(f"Error al agregar el registro en la tabla documentos: {e}")
            return False  # Error al agregar el registro a la base de datos
        

    # Método para actualizar un registro en la tabla de documentos
    def actualizar_documento(self, datos_actualizar, id_documento):
        # Consulta SQL para actualizar los datos con placeholders
        consulta = "UPDATE documentos SET "
        valores = []
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = %s, "
            valores.append(valor)
        consulta = consulta[:-2]  # Eliminar la coma y el espacio sobrantes
        consulta += " WHERE id_documento = %s"
        valores.append(id_documento)  # Añadir el ID del documento a los valores

        print(consulta)
        print(valores)

        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta, valores)
            self.connection.commit()
            cursor.close()
            print("Dato actualizado correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar el registro: {str(e)}")
            return False
    

    #Método para eliminar un registro en la tabla de documentos
    def eliminar_documento(self, id_documento):
        # Consulta SQL para eliminar un registro de la tabla documentos
        consulta = "DELETE FROM documentos WHERE id_documento = %s"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta,(id_documento))
            self.connection.commit()
            cursor.close()
            print("Registro eliminado correctamente.")
            return True
        except Exception as e:
            print(f"Error al eliminar el registro: {str(e)}")
            return False

    
   #Mostrar documentos por número de identidad
    def mostrar_documentos(self, numero_identidad):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar el registro
            # en la tabla documentos
            consulta = """
                SELECT 
                    *
                FROM documentos
                WHERE numero_identidad_destinatario = %s
                OR numero_identidad_remitente = %s
                ORDER BY fecha_envio DESC
                """
            cursor.execute(consulta,(numero_identidad,numero_identidad))
            # Obtener el registro de la tabla documentos
            registro_retornado = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()
            return registro_retornado  # Devuelve los registros encontrados

        except Exception as e:
            print(f"Error al retornar el registro: {e}")
            return None  # Devolver None si ocurre algún error
    

    #Comprobar usuario por correo
    def comprobar_usuario_correo(self, correo):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para comprobar correo
            # en la tabla usuario
            consulta = """
                SELECT 
                    correo
                FROM reestablecer_contrasena
                WHERE correo = %s
                """
            cursor.execute(consulta,(correo))
            # Obtener el registro de la tabla reestablecer_contrasena
            registro_retornado = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()
            return registro_retornado

        except Exception as e:
            print(f"Error al retornar el registro: {e}")
            return False  # Devolver None si ocurre algún error
        

    #Método para guardar el código en la tabla reestablecer contraseña
    def agregar_codigo_reestablecer_contrasena(self,datos):
        try:
            # Crear el cursor
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para insertar un nuevo registro en la tabla reestablecer_contrasena
            consulta = "INSERT INTO reestablecer_contrasena ("
            columnas = ", ".join(datos.keys())
            valores = "', '".join(map(str, datos.values()))
            consulta += f"{columnas}) VALUES ('{valores}')"

            print(consulta)
            # Ejecutar la consulta SQL
            cursor.execute(consulta)

            # Confirmar la transacción
            self.connection.commit()

            # Cerrar el cursor
            cursor.close()

            return True  # Éxito al agregar el registro a la base de datos

        except Exception as e:
            print(f"Error al agregar el registro en la tabla reestablecer_contrasena: {e}")
            return False  # Error al agregar el registro a la base de datos
        

    #Comprobar código para reestablecer la contraseña
    def comprobar_codigo_contrasena(self, codigo):
        try:
            # Crea un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para comprobar código para reestablecr contraseña
            consulta = """
                SELECT 
                    codigo, correo
                FROM reestablecer_contrasena
                WHERE codigo = %s
                """
            
            cursor.execute(consulta,(codigo))

            # Obtener el registro de la tabla reestablecr contraseña
            registro_retornado = cursor.fetchone()

            # Cerrar el cursor
            cursor.close()
            return registro_retornado

        except Exception as e:
            print(f"Error al retornar el registro: {e}")
            return False  # Devolver None si ocurre algún error
        
    
    #Método para actualizar la contraseña
    def actualizar_contrasena(self, datos_actualizar, correo):
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE usuarios SET "
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Eliminar la coma y el espacio sobrantes
        consulta += f" WHERE correo = '{correo}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Dato actualizado correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar el registro: {str(e)}")
            return False
        
    
    #Método para eliminar un registro en la tabla de reestablecer contraseña
    def eliminar_registro_reestablecer_contrasena(self, correo):
        # Consulta SQL para eliminar un registro de la tabla reestablecer contraseña
        consulta = "DELETE FROM reestablecer_contrasena WHERE correo = %s"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta,(correo))
            self.connection.commit()
            cursor.close()
            print("Registro eliminado correctamente.")
            return True
        except Exception as e:
            print(f"Error al eliminar el registro: {str(e)}")
            return False
        


      #Método para mostrar los datos de la bitácora
    def mostrar_datos_bitacora(self):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros 
            # en la tabla de bitácora
            consulta = """
                SELECT 
                    id_bitacora,
                    nombre_tabla,
                    tipo_operacion,
                    numero_identidad_usuario,
                    fecha_hora, detalle_actividad
                FROM bitacora
                ORDER BY fecha_hora DESC;
                """

            cursor.execute(consulta)

            # Obtener los registros de la tabla bitácora
            registros_retornados = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()
            return registros_retornados 

        except Exception as e:
            print(f"Error al buscar el registro : {str(e)}")
            return None  # Devolver None si ocurre algún error
        

    
      #Método para mostrar los datos de la bitácora
    def buscar_datos_bitacora(self,nombre_tabla,numero_identidad_usuario):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros 
            # en la tabla de bitácora
            consulta = """
                SELECT 
                    id_bitacora,
                    nombre_tabla,
                    tipo_operacion,
                    numero_identidad_usuario,
                    fecha_hora, detalle_actividad
                FROM bitacora
                WHERE nombre_tabla = %s 
                AND numero_identidad_usuario = %s
                ORDER BY fecha_hora DESC;
                """

            cursor.execute(consulta,(nombre_tabla,numero_identidad_usuario))

            # Obtener los registros de la tabla bitácora
            registros_retornados = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()
            return registros_retornados

        except Exception as e:
            print(f"Error al buscar el registro : {str(e)}")
            return None  # Devolver None si ocurre algún error
        
    
    def buscar_datos_bitacora_por_tabla(self,nombre_tabla):
        try:
            # Crear un cursor para ejecutar consultas SQL
            cursor = self.connection.cursor()

            # Preparar la consulta SQL para buscar los registros 
            # en la tabla de bitácora
            consulta = """
                SELECT 
                    id_bitacora,
                    nombre_tabla,
                    tipo_operacion,
                    numero_identidad_usuario,
                    fecha_hora, detalle_actividad
                FROM bitacora
                WHERE nombre_tabla = %s 
                ORDER BY fecha_hora DESC;
                """

            cursor.execute(consulta,(nombre_tabla))

            # Obtener los registros de la tabla bitácora
            registros_retornados = cursor.fetchall()

            # Cerrar el cursor
            cursor.close()
            return registros_retornados

        except Exception as e:
            print(f"Error al buscar el registro : {str(e)}")
            return None  # Devolver None si ocurre algún error
        

    def buscar_datos_bitacora_por_usuario(self,numero_identidad_usuario):
            try:
                # Crear un cursor para ejecutar consultas SQL
                cursor = self.connection.cursor()

                # Preparar la consulta SQL para buscar los registros 
                # en la tabla de bitácora
                consulta = """
                    SELECT 
                        id_bitacora,
                        nombre_tabla,
                        tipo_operacion,
                        numero_identidad_usuario,
                        fecha_hora, detalle_actividad
                    FROM bitacora
                    WHERE numero_identidad_usuario = %s 
                    ORDER BY fecha_hora DESC;
                    """

                cursor.execute(consulta,(numero_identidad_usuario))

                # Obtener los registros de la tabla bitácora
                registros_retornados = cursor.fetchall()

                # Cerrar el cursor
                cursor.close()
                return registros_retornados

            except Exception as e:
                print(f"Error al buscar el registro : {str(e)}")
                return None  # Devolver None si ocurre algún error
        


    #Método para actualizar las imágenes del inventario
    def actualizar_imagenes_inventario(self, datos_actualizar, numero_inventario):
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE inventario SET "
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Eliminar la coma y el espacio sobrantes
        consulta += f" WHERE numero_inventario = '{numero_inventario}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Dato actualizado correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar el registro: {str(e)}")
            return False
        

    #Método para actualizar las imágenes del inventario
    def actualizar_imagenes_bodega(self, datos_actualizar, numero_inventario):
        # Consulta SQL para actualizar los datos
        consulta = "UPDATE bodega SET "
        for columna, valor in datos_actualizar.items():
            consulta += f"{columna} = '{valor}', "
        consulta = consulta[:-2]  # Eliminar la coma y el espacio sobrantes
        consulta += f" WHERE numero_inventario = '{numero_inventario}'"

        print(consulta)
        try:
            # Ejecutar la consulta
            cursor = self.connection.cursor()
            cursor.execute(consulta)
            self.connection.commit()
            cursor.close()
            print("Dato actualizado correctamente.")
            return True
        except Exception as e:
            print(f"Error al actualizar el registro: {str(e)}")
            return False
        


#Instancia  de la clase SenacitInventarioDB
db = SenacitInventarioDB('localhost', 'root', '123456', 'senacit_inventario')
connection = db.connect()
