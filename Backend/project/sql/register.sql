
-- UTILIZAR LA BASE DE DATOS ACTUAL
USE db;

-- REGISTROS DE USUARIOS EJEMPLOS
INSERT INTO customers_customer(customer_code,first_name,last_name,type_identification,identification_number,telephone,email,status,date_birth,number_nit,place_birth,marital_status,profession_trade,gender,nationality,person_type,user_id_id,immigration_status_id_id,creation_date) 
VALUES('2024-S1', 'John', 'Doe', 'DPI', '123456789', '555-123', 'johndoe@example.com', 'Posible Cliente', '1985-05-10', '1234589-0', 'New York', 'married', 'Engineer', 'MASCULINO', 'American', 'Indivicual (PI)', 4, 1,'2024-06-04 12:30:00');

INSERT INTO customers_customer(customer_code,first_name,last_name,type_identification,identification_number,telephone,email,status,date_birth,number_nit,place_birth,marital_status,profession_trade,gender,nationality,person_type,user_id_id,immigration_status_id_id,creation_date)
VALUES ('2024-N1', 'Jane', 'Smith', 'DPI', '987654321', '555-987', 'janesmith@example.com', 'No Aprobado', '1988-09-15', '987621-1', 'Los Angeles', 'single', 'Doctor', 'FEMENINO', 'American', 'Indivicual (PI)', 4, 1,'2024-06-04 12:30:00');

INSERT INTO customers_customer(customer_code,first_name,last_name,type_identification,identification_number,telephone,email,status,date_birth,number_nit,place_birth,marital_status,profession_trade,gender,nationality,person_type,user_id_id,immigration_status_id_id,creation_date)
VALUES ('2024-1', 'Alice', 'Johnson', 'DPI', '456789123', '555-456', 'alicejohnson@example.com', 'Aprobado', '1992-03-20', '459123-2', 'Chicago', 'married', 'Artist', 'FEMENINO', 'American', 'Indivicual (PI)', 4, 1,'2024-06-04 12:30:00');

-- MOSTRAR LA INFORMACION DE LOS CLIENTES
SELECT * FROM customers_customer\G;


