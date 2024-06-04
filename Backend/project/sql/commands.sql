
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
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;

-- DELETE
DELETE FROM table_name WHERE condition;

-- MOSTRAR
SELECT column1, column2, ...
FROM table_name\G;

-- Informacion de la tabla
desc tabla;

-- Ejecutar archivos SQL

SOURCE <direccion del archivo sql>