
USE senacit_inventario;

DROP TRIGGER IF EXISTS mover_a_inventario_despues_de_actualizar;

DELIMITER //

CREATE TRIGGER mover_a_inventario_despues_de_actualizar
AFTER UPDATE ON bodega
FOR EACH ROW
BEGIN
    IF NEW.numero_identidad IS NOT NULL AND NEW.numero_identidad != 'None' THEN
        -- Verifica si el numero_identidad existe en la tabla usuarios
        IF EXISTS (SELECT 1 FROM usuarios WHERE numero_identidad = NEW.numero_identidad) THEN
            -- Insert the record into inventario
            INSERT INTO inventario (tipo_documento, fecha_documento, numero_documento, descripcion, numero_inventario,
                                    modelo, marca, serie, placa, motor, numero_chasis, color, departamento, departamento_interno,
                                    municipio, edificio, piso, orden_compra, fecha_ingreso, costo_adquisicion, modalidad_contratacion,
                                    numero_identidad, comentario, estado_bien, oficina, fecha_ingreso_bien,
                                    imagenes_bien, fecha_registro_inventario)
            VALUES (NEW.tipo_documento, NEW.fecha_documento, NEW.numero_documento, NEW.descripcion,
                    NEW.numero_inventario, NEW.modelo, NEW.marca, NEW.serie, NEW.placa, NEW.motor,
                    NEW.numero_chasis, NEW.color, NEW.departamento, NEW.departamento_interno, NEW.municipio,
                    NEW.edificio, NEW.piso, NEW.orden_compra, NEW.fecha_ingreso, NEW.costo_adquisicion,
                    NEW.modalidad_contratacion, NEW.numero_identidad,
                    NEW.comentario, NEW.estado_bien, NEW.oficina, NEW.fecha_ingreso_bien, NEW.imagenes_bien,
                    NOW());
            -- Se inserta un registro temporal en la tabla "tabla-bodega_temporal"
            INSERT INTO tabla_bodega_temporal (id) VALUES (NEW.id_bodega);
        END IF;
    END IF;
END //

DELIMITER ;
