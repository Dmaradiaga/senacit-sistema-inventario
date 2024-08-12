
USE senacit_inventario;

DELIMITER //

	DROP TRIGGER IF EXISTS despues_actualizar_estado_solicitud;
    
	CREATE TRIGGER despues_actualizar_estado_solicitud
	AFTER UPDATE ON solicitud_descargo
	FOR EACH ROW
	BEGIN
		IF NEW.estado_solicitud = 1 THEN
			DELETE FROM inventario WHERE numero_inventario = NEW.numero_inventario;
		END IF;
	END //
DELIMITER ;
