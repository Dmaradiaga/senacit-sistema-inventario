
USE senacit_inventario;

DELIMITER //

DROP EVENT IF EXISTS eliminar_bodega_registro;

CREATE EVENT eliminar_bodega_registro
ON SCHEDULE EVERY 2 MINUTE
DO
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE delete_id INT;
    DECLARE cur CURSOR FOR SELECT id FROM tabla_bodega_temporal;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO delete_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        DELETE FROM bodega WHERE id_bodega = delete_id;
        DELETE FROM tabla_bodega_temporal WHERE id = delete_id;
    END LOOP;

    CLOSE cur;
END //

DELIMITER ;
