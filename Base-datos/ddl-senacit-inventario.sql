
CREATE DATABASE senacit_inventario;

USE senacit_inventario;

drop table  if exists inventario;
drop table  if exists usuarios;
drop table  if exists bodega;
drop table if exists solicitud_descargo;
drop table if exists solicitud_traslado;
drop table if exists documentos;
drop table if exists tabla_bodega_temporal;
drop table if exists reestablecer_contrasena;
drop table if exists bitacora;


CREATE TABLE usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    numero_identidad VARCHAR(20) NOT NULL UNIQUE,
    correo VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol_usuario  VARCHAR(500) NOT NULL,
    url_firma_imagen VARCHAR(255),
    id_imagen_url  VARCHAR(100),
    estado_usuario BOOLEAN DEFAULT TRUE NOT NULL,
    es_jefe_departamento BOOLEAN NOT NULL,
    es_tecnico BOOLEAN NOT NULL,
    departamento_interno VARCHAR(100) NOT NULL,
    fecha_registro_usuario TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE inventario (
    id_inventario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tipo_documento VARCHAR(100),
    fecha_documento DATE NOT NULL,
    numero_documento VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    numero_inventario VARCHAR(100) NOT NULL UNIQUE,
    modelo VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    serie VARCHAR(100) NOT NULL,
    placa VARCHAR(100),
    motor VARCHAR(100),
    numero_chasis VARCHAR(100),
    color VARCHAR(100) NOT NULL,
    departamento VARCHAR(100),
    departamento_interno VARCHAR(100) NOT NULL,
    municipio VARCHAR(100) DEFAULT NULL,
    edificio VARCHAR(100) NOT NULL,
    piso VARCHAR(100) NOT NULL,
    orden_compra VARCHAR(100),
    fecha_ingreso DATE NOT NULL,
    costo_adquisicion INT NOT NULL,
    modalidad_contratacion VARCHAR(100) NOT NULL,
    numero_identidad VARCHAR(13) NOT NULL, 
    comentario TEXT NOT NULL,
    estado_bien VARCHAR(100) NOT NULL,
    oficina VARCHAR(100) NOT NULL,
    fecha_ingreso_bien DATE NOT NULL,
    imagenes_bien TEXT NOT NULL,
    fecha_registro_inventario TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (numero_identidad)
        REFERENCES usuarios (numero_identidad)
);

CREATE TABLE bodega  (
	id_bodega INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tipo_documento VARCHAR(100),
    fecha_documento DATE NOT NULL,
    numero_documento VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    numero_inventario VARCHAR(100) NOT NULL UNIQUE,
    modelo VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    serie VARCHAR(100) NOT NULL,
    placa VARCHAR(100),
    motor VARCHAR(100),
    numero_chasis VARCHAR(100),
    color VARCHAR(100) NOT NULL,
    departamento VARCHAR(100),
    departamento_interno VARCHAR(100),
    municipio VARCHAR(100) DEFAULT NULL,
    edificio VARCHAR(100) NOT NULL,
    piso VARCHAR(100) NOT NULL,
    orden_compra VARCHAR(100),
    fecha_ingreso DATE NOT NULL,
    costo_adquisicion INT NOT NULL,
    modalidad_contratacion VARCHAR(100),
    numero_identidad VARCHAR(20),
    comentario TEXT NOT NULL,
    estado_bien VARCHAR(100) NOT NULL,
    oficina VARCHAR(100) NOT NULL,
    fecha_ingreso_bien DATE NOT NULL,
    imagenes_bien TEXT NOT NULL,
    fecha_registro_bodega TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE tabla_bodega_temporal (
    id INT PRIMARY KEY,
    tiempo DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE solicitud_descargo (
    id_solicitud_descargo INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_solicitante VARCHAR(255) NOT NULL,
    fecha_solicitud DATE NOT NULL,
    lugar VARCHAR(255) NOT NULL,
    justificacion_descargo TEXT NOT NULL,
    numero_identidad_solicitante VARCHAR(20) NOT NULL,
    puesto VARCHAR(255) NOT NULL,
    /* Información del bien */
    marca VARCHAR(255) NOT NULL,
    serie VARCHAR(255) NOT NULL,
    numero_inventario VARCHAR(255) NOT NULL,
    diagnostico TEXT,
    modelo VARCHAR(255) NOT NULL,
    /* Información adicional */
    descripcion TEXT,
    departamento_interno VARCHAR(100) NOT NULL,
    imagen VARCHAR(100),
    estado_solicitud BOOLEAN DEFAULT FALSE,
    /* firmas de aprobación */
    firma_jefe_departamento VARCHAR(255),
    firma_responsable_dictamen VARCHAR(255),
    firma_responsable_bien VARCHAR(255),
    firma_jefe_unidad_bien VARCHAR(255),
	numero_identidad_responsable_dictamen VARCHAR(20),
    /* Clave foránea */
    FOREIGN KEY (numero_identidad_solicitante) REFERENCES usuarios(numero_identidad)
);

CREATE TABLE solicitud_traslado (
    id_solicitud_traslado INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_solicitante VARCHAR(255) NOT NULL,
    fecha_solicitud DATE NOT NULL,
    descripcion TEXT NOT NULL,
    lugar VARCHAR(255) NOT NULL,
    justificacion_traslado TEXT,
    numero_identidad_solicitante VARCHAR(20) NOT NULL,
    serie VARCHAR(255) NOT NULL,
    color VARCHAR(255) NOT NULL,
    puesto VARCHAR(255) NOT NULL,
    numero_inventario VARCHAR(255) NOT NULL,
    departamento_interno VARCHAR(255) NOT NULL,
    imagen VARCHAR(255),
    estado_solicitud BOOLEAN DEFAULT FALSE,
    /* firmas de aprobación */
    firma_jefe_departamento VARCHAR(255),
    firma_responsable_bien VARCHAR(255),
    firma_jefe_unidad_bien VARCHAR(255),
    fecha_final DATE NOT NULL,
    fecha_inicio DATE NOT NULL,
    mensaje VARCHAR(100) NOT NULL,
    /* Clave foránea */
	FOREIGN KEY (numero_identidad_solicitante) REFERENCES usuarios(numero_identidad)
);

CREATE TABLE documentos (
	id_documento INT NOT NULL  AUTO_INCREMENT PRIMARY KEY,
    numero_identidad_destinatario VARCHAR(20) NOT NULL,
    numero_identidad_remitente VARCHAR(20) NOT NULL,
    nombre_remitente VARCHAR (100) NOT NULL,
    url_documento VARCHAR(200) NOT NULL,
    id_url_documento VARCHAR(100) NOT NULL,
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE bitacora (
    id_bitacora INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_tabla VARCHAR(20) NOT NULL,
    nombre_usuario TEXT NOT NULL,
    detalle_actividad TEXT,
    tipo_operacion VARCHAR(20) NOT NULL,
    numero_identidad_usuario VARCHAR(20) NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reestablecer_contrasena (
    id_reestablecer_contrasena INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL,
    correo VARCHAR(50) NOT NULL UNIQUE,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


