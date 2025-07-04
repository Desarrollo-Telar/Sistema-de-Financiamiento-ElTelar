
-- UTILIZAR LA BASE DE DATOS ACTUAL
USE db;

-- REGISTRAR CONDICION MIGRATORIA
INSERT INTO customers_immigrationstatus(condition_name) 
VALUES('Residente temporal'),
('Turista o visitante'),
('Residente permanente'),
('Permiso de trabajo'),
('Persona en tránsito'),
('Permiso consular o similar'),
('Otra');

-- REGISTROS DE CLIENTES EJEMPLOS
INSERT INTO customers_customer(customer_code,first_name,last_name,type_identification,identification_number,telephone,email,status,date_birth,number_nit,place_birth,marital_status,profession_trade,gender,nationality,person_type,user_id_id,immigration_status_id_id,creation_date) 
VALUES('2024-S1', 'John', 'Doe', 'DPI', '123456789', '555-123', 'johndoe@example.com', 'Posible Cliente', '1985-05-10', '1234589-0', 'New York', 'married', 'Engineer', 'MASCULINO', 'American', 'Indivicual (PI)', 1, 1,'2024-06-04 12:30:00');

INSERT INTO customers_customer(customer_code,first_name,last_name,type_identification,identification_number,telephone,email,status,date_birth,number_nit,place_birth,marital_status,profession_trade,gender,nationality,person_type,user_id_id,immigration_status_id_id,creation_date)
VALUES ('2024-N1', 'Jane', 'Smith', 'DPI', '987654321', '555-987', 'janesmith@example.com', 'No Aprobado', '1988-09-15', '987621-1', 'Los Angeles', 'single', 'Doctor', 'FEMENINO', 'American', 'Indivicual (PI)', 1, 1,'2024-06-04 12:30:00');

INSERT INTO customers_customer(customer_code,first_name,last_name,type_identification,identification_number,telephone,email,status,date_birth,number_nit,place_birth,marital_status,profession_trade,gender,nationality,person_type,user_id_id,immigration_status_id_id,creation_date)
VALUES ('2024-1', 'Alice', 'Johnson', 'DPI', '456789123', '555-456', 'alicejohnson@example.com', 'Aprobado', '1992-03-20', '459123-2', 'Chicago', 'married', 'Artist', 'FEMENINO', 'American', 'Indivicual (PI)', 1, 1,'2024-06-04 12:30:00');


INSERT INTO FinancialInformation_reference(full_name, phone_number,reference_type, customer_id_id) 
VALUES('JUAN CARLOS CHOC XOL','42249955','Personales',1),
('Héctor Medina Castro','42249955','Personales',1),
('Santiago Vázquez León','42249955','Bancarias',1),
('Renata Campos Estrada','42249955','Bancarias',1);


INSERT INTO FinancialInformation_othersourcesofincome(source_of_income,nit,phone_number,salary,customer_id_id)
VALUES('DSAD','1808964-K','42249955','35',1);



INSERT INTO addresses_address(street, number, city, state,  country, type_address, customer_id_id)
VALUES
('Calle Falsa 123', 456, 'Springfield', 'IL',  'USA', 'Dirección de Personal', 1),
('Avenida Siempre Viva 742', 100, 'Springfield', 'IL',  'USA', 'Dirección de Trabajo', 1);

INSERT INTO addresses_coordinate(latitud, longitud, address_id_id)
VALUES
(39.7817, -89.6501, 1),
(39.7817, -89.6502, 2);

INSERT INTO InvestmentPlan_investmentplan(
    type_of_product_or_service,
    total_value_of_the_product_or_service,
    investment_plan_description,
    initial_amount,
    monthly_amount,
    transfers_or_transfer_of_funds,
    type_of_transfers_or_transfer_of_funds,
    customer_id_id
) VALUES (
    'Mutual Fund', 
    100000, 
    'Long-term investment in a diversified mutual fund.', 
    5000, 
    500, 
    1, 
    'Local', 
    1
);

-- MOSTRAR LA INFORMACION DE LOS CLIENTES
SELECT * FROM customers_customer\G;

-- MOSTRAR LA INFORMACION DE CONDICION MIGRATORIA
SELECT * FROM customers_immigrationstatus;

