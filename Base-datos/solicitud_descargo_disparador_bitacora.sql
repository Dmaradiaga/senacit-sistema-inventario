
USE senacit_inventario;

drop trigger despues_insertar_solicitud_descargo;
drop trigger despues_actualizar_solicitud_descargo;
drop trigger despues_eliminar_solicitud_descargo;

DELIMITER //
        
	-- ACTUALIZAR
		CREATE TRIGGER despues_actualizar_solicitud_descargo
		AFTER UPDATE ON solicitud_descargo
		FOR EACH ROW
		BEGIN
            
	IF NEW.estado_solicitud = 1 THEN
        INSERT INTO bodega (
            tipo_documento,
            fecha_documento,
            numero_documento,
            descripcion,
            numero_inventario,
            modelo,
            marca,
            serie,
            placa,
            motor,
            numero_chasis,
            color,
            departamento,
            departamento_interno,
            municipio,
            edificio,
            piso,
            orden_compra,
            fecha_ingreso,
            costo_adquisicion,
            modalidad_contratacion,
            comentario,
            estado_bien,
            oficina,
            fecha_ingreso_bien,
            imagenes_bien
        )
        SELECT
            inv.tipo_documento,
            inv.fecha_documento,
            inv.numero_documento,
            inv.descripcion,
            inv.numero_inventario,
            inv.modelo,
            inv.marca,
            inv.serie,
            inv.placa,
            inv.motor,
            inv.numero_chasis,
            inv.color,
            inv.departamento,
            inv.departamento_interno,
            inv.municipio,
            inv.edificio,
            inv.piso,
            inv.orden_compra,
            inv.fecha_ingreso,
            inv.costo_adquisicion,
            inv.modalidad_contratacion,
            inv.comentario,
            inv.estado_bien,
            inv.oficina,
            inv.fecha_ingreso_bien,
            inv.imagenes_bien
        FROM inventario inv
        WHERE inv.numero_inventario = OLD.numero_inventario;
        
        -- Eliminando registro de la tabla de inventario, después del descargo
        DELETE FROM inventario WHERE numero_inventario = NEW.numero_inventario;
		
    END IF;
    
  END //

        
DELIMITER ;

