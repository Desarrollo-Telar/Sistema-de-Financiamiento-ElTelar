
/* ---- CONECTARSE A LA BASE DE DATOS MYSQL*/
mysql -u user -h db db -p

use db;
 
SHOW DATABASES;
SHOW TABLES;
 -- CONSULTA DE INSERTAR
INSERT INTO table_name (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...);

-- INNER JOIN
SELECT columns
FROM table1
INNER JOIN table2
ON table1.column = table2.column;

-- UPDATE
UPDATE financings_payment
SET tipo_pago = "CLIENTE" 
WHERE id = 97;

-- DELETE
DELETE FROM table_name WHERE condition;

-- MOSTRAR
SELECT column1, column2, ...
FROM table_name\G;

-- Informacion de la tabla
desc tabla;

-- Ejecutar archivos SQL

SOURCE <direccion del archivo sql>

UPDATE financings_paymentplan SET mora = 0, cuota_vencida = 0 WHERE credit_id_id = 3;

UPDATE financings_paymentplan SET start_date = "2025-02-13 06:00:00.000000" where credit_id_id = 65;


 UPDATE financings_paymentplan SET mora = 0, cuota_vencida = 0 WHERE credit_id_id = 4;



 UPDATE financings_paymentplan SET mora = 0, cuota_vencida = 0 WHERE credit_id_id = 5;


UPDATE financings_banco fb
SET fb.status = FALSE
WHERE fb.referencia IN (
    SELECT fp.numero_referencia 
    FROM financings_payment fp 
    WHERE fp.estado_transaccion = 'PENDIENTE'
);
