USE senacit_inventario;

drop event if exists eliminar_registros_expirados;

DELIMITER //
	CREATE EVENT eliminar_registros_expirados
	ON SCHEDULE EVERY 15 MINUTE
	DO
	BEGIN
		DELETE FROM reestablecer_contrasena
		WHERE fecha_hora < NOW() - INTERVAL 12 MINUTE;
	END //
DELIMITER ;
