INSERT INTO addresses_departamento(id, nombre) VALUES
(1, 'Alta Verapaz'),
(2, 'Baja Verapaz'),
(3, 'Chimaltenango'),
(4, 'Chiquimula'),
(5, 'El Progreso'),
(6, 'Escuintla'),
(7, 'Guatemala'),
(8, 'Huehuetenango'),
(9, 'Izabal'),
(10, 'Jalapa'),
(11, 'Jutiapa'),
(12, 'Peten'),
(13, 'Quetzaltenango'),
(14, 'Quiche'),
(15, 'Retalhuleu'),
(16, 'Sacatepequez'),
(17, 'San Marcos'),
(18, 'Santa Rosa'),
(19, 'Solola'),
(20, 'Suchitepéquez'),
(21, 'Totonicapan'),
(22, 'Zacapa');

INSERT INTO addresses_municiopio (id, nombre, depart_id) VALUES
-- Alta Verapaz
(1, 'Coban', 1),
(2, 'San Pedro Carcha', 1),
(3, 'Santa Cruz Verapaz', 1),
(4, 'San Cristobal Verapaz', 1),
(5, 'Tactic', 1),

-- Guatemala
(6, 'Guatemala', 7),
(7, 'Santa Catarina Pinula', 7),
(8, 'San Jose Pinula', 7),
(9, 'Mixco', 7),
(10, 'Villa Nueva', 7),

-- Quetzaltenango
(11, 'Quetzaltenango', 13),
(12, 'Salcaja', 13),
(13, 'San Carlos Sija', 13),
(14, 'Olintepeque', 13),
(15, 'La Esperanza', 13),

-- Zacapa
(16, 'Zacapa', 22),
(17, 'Estanzuela', 22),
(18, 'Rio Hondo', 22),
(19, 'Teculutan', 22),
(20, 'Usumatlan', 22);
