mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 9.1.0, for Linux (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
mysqldump: Error: 'Access denied; you need (at least one of) the PROCESS privilege(s) for this operation' when trying to dump tablespaces

--
-- Table structure for table `FinancialInformation_othersourcesofincome`
--

DROP TABLE IF EXISTS `FinancialInformation_othersourcesofincome`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FinancialInformation_othersourcesofincome` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `source_of_income` varchar(100) NOT NULL,
  `nit` varchar(20) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `salary` decimal(10,2) NOT NULL,
  `customer_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FinancialInformation_customer_id_id_c6131296_fk_customers` (`customer_id_id`),
  CONSTRAINT `FinancialInformation_customer_id_id_c6131296_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FinancialInformation_othersourcesofincome`
--

LOCK TABLES `FinancialInformation_othersourcesofincome` WRITE;
/*!40000 ALTER TABLE `FinancialInformation_othersourcesofincome` DISABLE KEYS */;
/*!40000 ALTER TABLE `FinancialInformation_othersourcesofincome` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FinancialInformation_reference`
--

DROP TABLE IF EXISTS `FinancialInformation_reference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FinancialInformation_reference` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(150) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `reference_type` varchar(100) NOT NULL,
  `customer_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FinancialInformation_customer_id_id_42b86f6d_fk_customers` (`customer_id_id`),
  CONSTRAINT `FinancialInformation_customer_id_id_42b86f6d_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=281 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FinancialInformation_reference`
--

LOCK TABLES `FinancialInformation_reference` WRITE;
/*!40000 ALTER TABLE `FinancialInformation_reference` DISABLE KEYS */;
INSERT INTO `FinancialInformation_reference` VALUES (2,'Emerson Caal','57409873','Personales',5),(3,'Suany Caal','35968506','Personales',5),(4,'Alex Pop','55150700','Laborales',5),(5,'Henry Chen','31799272','Laborales',5),(6,'FRANCISCO XOL','38300029','Personales',7),(7,'JAVIER LUC','31222427','Personales',7),(8,'IGNACIO VAIDEZ','39304102','Laborales',7),(9,'FEDERICO COC','57275357','Laborales',7),(10,'SERGIO COL','49820167','Personales',8),(11,'CARLOS POP','46622312','Personales',8),(12,'ROSARIO CAAL','33791508','Laborales',8),(13,'LUIS CAAL','41909713','Laborales',8),(14,'SHEYLA LEAL','48335107','Personales',9),(15,'SHERLI VIVIANA LEAL SAGUI','45921266','Personales',9),(16,'MARIO CHUB','45472870','Laborales',9),(17,'ELICEO QUE','55022679','Laborales',9),(18,'DENIS LOPEZ','57488082','Personales',10),(19,'EDISON ESTRADA','51353279','Personales',10),(20,'ABELARDO CAAL','55505163','Laborales',10),(21,'ANGEL GARCIA','553446103','Laborales',10),(22,'DANIELA POOU','50041341','Personales',11),(23,'HILDA VARGAS','46342891','Personales',11),(24,'ESPERO CASTRO','40993297','Laborales',11),(25,'PABLO BAILON','30314248','Laborales',11),(26,'RONALDO POC','47751562','Personales',12),(27,'ANGELA RODRIGUEZ','59998102','Personales',12),(28,'ALEX GOMEZ','32482038','Laborales',12),(29,'CARLOS CAAL','40579589','Laborales',12),(30,'MARILYN SANTOS','59280848','Personales',13),(31,'BLANCA IRIS','46465673','Personales',13),(32,'ESTELA JUAREZ','36002936','Laborales',13),(33,'TERESITA RUIZ','58305615','Laborales',13),(34,'ENEYDA CAAL','42535196','Personales',14),(35,'LUCIA POP','49651310','Personales',14),(36,'MAITE HUMBLERS','31475817','Laborales',14),(37,'MAGDALENA REYES','37654617','Laborales',14),(38,'BEBERLY POP','32064879','Personales',15),(39,'BYRON TOT','49653171','Personales',15),(40,'BRAYAN CASTILLO','45379647','Laborales',15),(41,'DARWIN CAAL','48176285','Laborales',15),(42,'DALILA MOLINA','53854405','Personales',16),(43,'RAMON DALCRUZ','55105017','Personales',16),(44,'LILI PAZ','41396976','Laborales',16),(45,'BRENDA MAXENA','31054763','Laborales',16),(46,'LUCAS CAAL','32465792','Personales',17),(47,'FLORIDALMA CABNAL','51536622','Personales',17),(48,'RUBPERTO COY','56388272','Laborales',17),(49,'MADELYN TZALAM','42765367','Laborales',17),(50,'ABNER OJOM CASTRO','51581248','Personales',18),(51,'ELIZABETH TIUL','30831968','Personales',18),(52,'EMILIO OJOM','48538167','Laborales',18),(53,'MARVIN CAAL TZI','45183252','Laborales',18),(54,'RUBEN DARIO QUIM','46440694','Personales',19),(55,'EFRAIN MAAZ','46441642','Personales',19),(56,'EDIN CHEN','48312828','Laborales',19),(57,'WILSON CUZ','46815876','Laborales',19),(58,'ELMER YAT','31055561','Personales',20),(59,'ABIGAIL PONCE','46163553','Personales',20),(60,'JESSICA TZUL','58327655','Laborales',20),(61,'ANGELINA VARGAS','38302728','Laborales',20),(62,'CESAR ANTONIO BARRIENTOS','36519613','Personales',21),(63,'MIRNA PAOLA LUTHER','40755177','Personales',21),(64,'ERICK GONZALES','40056457','Laborales',21),(65,'DIEGO ADOLFO PEREZ','42464238','Laborales',21),(66,'DIEGO ADOLFO PEREZE','42464238','Personales',23),(67,'ALEJANDRO RUIZ','58743745','Personales',23),(68,'NELSON MOINO','40909047','Laborales',23),(69,'CARLOS PUMAY','54817603','Laborales',23),(70,'VICTORIA CAAL','55562047','Personales',24),(71,'MAYRA SIERRA','46817463','Personales',24),(72,'ALEX COY','51949627','Laborales',24),(73,'ALBERTO TENEBAUM','52058181','Laborales',24),(74,'DENCI OROZCO','53283068','Personales',25),(75,'HENRY RAMIREZ','58192266','Personales',25),(76,'EDIN GREGORIO','53278364','Laborales',25),(77,'DANILO TOC','40902835','Laborales',25),(81,'HEYDI CATUN','58877037','Personales',28),(82,'ANDREA MALDONADO','41807621','Personales',28),(83,'ALVARO YALIBAT','53016341','Laborales',28),(84,'FERMIN AJCA','57016825','Laborales',28),(85,'TERESA ANAHELIA CAAL','51220607','Personales',29),(86,'JORGE ARMANDO CAAL','33465551','Personales',29),(87,'ALVARO POP','37732568','Laborales',29),(88,'DOMINGO BOTOC','37262335','Laborales',29),(89,'ERICK AROLDO COC','31933628','Personales',30),(90,'FRANCISCO BA CUCUL','4268985','Personales',30),(91,'SAMUEL COC TUT','37067253','Laborales',30),(92,'MARCO TIUL','30358614','Laborales',30),(93,'MARIA VICTORIA','46339008','Personales',31),(94,'JOSUE VAIDEZ','38092530','Personales',31),(95,'EVELIN CU','32202587','Laborales',31),(96,'JENIFER GONZALEZ','32202587','Laborales',31),(97,'JEREMIAS YAT','52002502','Personales',32),(98,'GLENDA PACAY','40605477','Personales',32),(99,'EDGAR CU','42892803','Laborales',32),(100,'SELVIN CAL','36537621','Laborales',32),(101,'MERCY MUÑOS','41109515','Personales',33),(102,'ZOILA CACAO','51968537','Personales',33),(103,'KARLA SIERRA','47698889','Laborales',33),(104,'MIRNA CANIL','32732779','Laborales',33),(105,'JAIRO ALEXANDER CASASOLA','50368549','Personales',34),(106,'OSVIN ARMANDO CASASOLA','58991555','Personales',34),(107,'ARIADNA CASTILLO','46919943','Laborales',34),(108,'DANIELA LOPEZ','41592785','Laborales',34),(109,'ANGEL ROMAN','56183626','Personales',35),(110,'AZUCENA TA','47911607','Personales',35),(111,'PAOLA ASIG','46977598','Laborales',35),(112,'MARCOS MORALES','53617139','Laborales',35),(113,'SONIA MORAN','31445838','Personales',36),(114,'DULCE VALDEZ','41779823','Personales',36),(115,'JONATHAN MORAN','56926947','Laborales',36),(116,'IRENE BARREONDO','41830953','Laborales',36),(117,'SIOMARA YALIBAT','59758374','Personales',37),(118,'DAYANA CHOCOOJ','50518103','Personales',37),(119,'EDUARDO RIVEIRO','52025275','Laborales',37),(120,'BRENDA CHOCOOJ','45622523','Laborales',37),(121,'JULIO VARGAS','57171802','Personales',38),(122,'ESTUARDO PACAY','43814783','Personales',38),(123,'ISAIAS OROZCO','39228271','Laborales',38),(124,'GUSTAVO GRANADOS','54606201','Laborales',38),(125,'WILFREDO CIFUENTES','41282465','Personales',40),(126,'KEVIN RAMOS','36111454','Personales',40),(127,'BENJAMIN VELASQUEZ','55856985','Laborales',40),(128,'LUIS GOMEZ','59410667','Laborales',40),(129,'MOISES MENDEZ','41277363','Personales',41),(130,'JORGE CASTELLANOS','46823743','Personales',41),(131,'MARIO MORAN','58343941','Laborales',41),(132,'HUGO SANDOVAL','50581724','Laborales',41),(133,'VICTORIA CAAL','55562047','Personales',42),(134,'MAGDA CANO','59982404','Personales',42),(135,'CARNICERÍA TRESH MITH','33379906','Comerciales',42),(136,'ALMACENES EL GANADOR','024292169','Comerciales',42),(137,'DEYSI LISETH POP CHOCOOJ','46416617','Personales',43),(138,'WALTER ALEXANDER CAL BOL','40796381','Personales',43),(139,'LUIS MACZ','33159492','Laborales',43),(140,'MOISÉS SIERRA','31477827','Laborales',43),(141,'MARÍA FERNANDA REYES','55804972','Personales',44),(142,'MARTHA GABRIELA REYES','45288179','Personales',44),(143,'CARLOS REYES','38194829','Laborales',44),(144,'MAX GIRÓN','155553434','Laborales',44),(145,'LOYDA TIUL','55173485','Personales',46),(146,'ALEJANDRA RAYMUNDO','36172929','Personales',46),(147,'ESMERALDA CHIQUIN','58754527','Laborales',46),(148,'CRYSTA BARRIOS','45071983','Laborales',46),(149,'MARTHA GABRIELA REYES','45288179','Personales',47),(150,'JARY CUELLER','57111627','Personales',47),(151,'HECTOR RUDY MOLINA','46082400','Comerciales',47),(152,'ALMA LORENA GARCIA','57466440','Comerciales',47),(153,'VILMA TZUB GARCIA','50418141','Personales',49),(154,'SELVIN GARCIA','33264494','Personales',49),(155,'MIGUEL CAAL','53711477','Laborales',49),(156,'REGINALDO POP','42108184','Laborales',49),(157,'SILVIA GONZALES','30418597','Personales',50),(158,'MARIA DE LOS ANGELES YAXCAL','30354644','Personales',50),(159,'VANESA ALVARADO','33120903','Laborales',50),(160,'MATERIAL DE PLÁSTICOS HUEHUETENANGO','57622303','Laborales',50),(161,'CESAR YAT','40676493','Personales',51),(162,'ANTONIO POC','45921134','Personales',51),(163,'SELVIN CAN','48255616','Laborales',51),(164,'KEVIN ARROLLO','41754773','Laborales',51),(165,'MARIA CAAL','58011099','Personales',52),(166,'ADELITA RAMIREZ','47354080','Personales',52),(167,'RAUL MARTINEZ','35114011','Laborales',52),(168,'OSCAR TUJAB','58173616','Laborales',52),(169,'Yasira Rene alvarado Castellanos','42640879','Personales',53),(170,'Rocío Águilar','32785550','Personales',53),(171,'Josue Macz','41333467','Laborales',53),(172,'Aurora teni','59720429','Laborales',53),(173,'BRENDA OLIVA','47739619','Personales',54),(174,'ADA REYES','58010395','Personales',54),(175,'JESSICA CUCUL','30160983','Laborales',54),(176,'NATALIE MACZ','46306177','Laborales',54),(177,'DEBORA LEIVA','30480822','Personales',55),(178,'BIANCA SAGUI','45234738','Personales',55),(179,'SERGIO RAMIREZ','39946938','Laborales',55),(180,'DON CESAR','45750986','Laborales',55),(181,'SERGIO IBARRA','51359117','Personales',56),(182,'EDGAR SIERRA','59181654','Personales',56),(183,'SERGIO RAMIREZ','30571005','Laborales',56),(184,'VICTOR MENDOZA','46973701','Laborales',56),(185,'JUAN DANIRL COJOZ','38677169','Personales',57),(186,'DELMY DE LA CRUZ','48310448','Personales',57),(187,'JONATHAN CU CHUN','39892551','Laborales',57),(188,'KATERIN CU DE LA CRUZ','37673126','Laborales',57),(189,'PEDRO CUZ','50447483','Personales',58),(190,'RUBY PEREZ','30789752','Personales',58),(191,'MARIO POP','45701951','Laborales',58),(192,'FRANKLIN RAYMUNDO','38344037','Laborales',58),(193,'JONATHAN COY','51324541','Personales',59),(194,'KIMBERLY COY','45787603','Personales',59),(195,'YESICA TZUL','58327655','Laborales',59),(196,'ERIK CATUN','48126127','Laborales',59),(197,'INGRID ROXANA TZOC BEB','53802374','Personales',60),(198,'CINTHIA ARELY MACZ YAT','51885263','Personales',60),(199,'ROBERTO RAX','56000471','Laborales',60),(200,'HENRY MAYEN','46796693','Laborales',60),(201,'AURELIO QUEJ','51953358','Personales',61),(202,'CARLOS ANTONIO CHOC','45667906','Personales',61),(203,'AXEL COY','31215037','Laborales',61),(204,'CARMEN RODRIGUEZ','37710870','Laborales',61),(205,'MARLON QUIROA GAMARRO','50073323','Personales',62),(206,'HARY ALEXANDER CHUN MOREIRA','46121651','Personales',62),(207,'JORGE BOTZOC','45184925','Laborales',62),(208,'JAVIER TIUL GUALNA','32316286','Laborales',62),(209,'DANIEL DELGADO','48997076','Personales',63),(210,'ANTONY MORALES','39663584','Personales',63),(211,'HARY HUN','45252543','Laborales',63),(212,'IRWIN DELGADO','57509613','Laborales',63),(213,'ANA TIUL CAAL','30578799','Personales',65),(214,'LINDA CAAL','58661271','Personales',65),(215,'GERSON SOSA','52152675','Laborales',65),(216,'BRYAN CHOC','45768474','Laborales',65),(217,'JUILO SOSA','53922255','Personales',66),(218,'JARVIS VALDEZ','33248074','Personales',66),(219,'HUGO TI','46719783','Laborales',66),(220,'JOSÉ LÓPEZ','49316684','Laborales',66),(221,'AXEL GALINDO','53054819','Personales',67),(222,'MARVIN LEONEL GÓNZALES','49052611','Personales',67),(223,'VIKI CAAL','42012270','Laborales',67),(224,'ANA MARÍA BUENAFÉ','32672463','Laborales',67),(225,'MARIO CHEN','58400435','Personales',68),(226,'HERLINDA','48579006','Personales',68),(227,'Victor López','57751195','Laborales',68),(228,'JHONY MO','54291567','Laborales',68),(229,'MISAEL GUERRA','45231735','Personales',69),(230,'ADOUAR BARRIOS','59817330','Personales',69),(231,'ALEJANDRO ASIG','33774624','Laborales',69),(232,'IVAN CAAL','33926154','Laborales',69),(233,'JOSUE IVAN','46646328','Personales',70),(234,'ABINADI CAAL','53722065','Personales',70),(235,'CRISTIAN CAAL','50305121','Laborales',70),(236,'ALEJANDO ASIG','33774624','Laborales',70),(237,'HILDA VARGAS','46342891','Personales',71),(238,'LILIAN MARTIN','55842914','Personales',71),(239,'EDIN DELGADO','57741144','Laborales',71),(240,'CESAR MACZ','40077803','Laborales',71),(241,'HEIDI VIRGINIA MOLINA','58505809','Personales',72),(242,'NILSA AIDEE ORELLANA','59076549','Personales',72),(243,'RAUL CRISTOBAL JUC','59035523','Laborales',72),(244,'MIRNA ISMENIA MACZ','53104881','Laborales',72),(245,'ASTRID CAAL','42665921','Personales',73),(246,'NADIA CAAL','59869861','Personales',73),(247,'URSULA MARIA VARGAS','42700518','Laborales',73),(248,'SHIRLYE GUILLERMO','50064965','Laborales',73),(249,'ALEXANDER TENI','47869917','Personales',74),(250,'GERANDO POP','46233200','Personales',74),(251,'WILMMER POP SANCHEZ','46826143','Laborales',74),(252,'GLORIA ANGELICA MO','49001492','Laborales',74),(253,'MARIO TIUL','45792295','Personales',75),(254,'DYLENE TIUL','30283653','Personales',75),(255,'EDIN MAX','33558849','Laborales',75),(256,'CARLOS CAAL','45489224','Laborales',75),(257,'ASTRID POP','50061507','Personales',76),(258,'RUBY SAGASTUME','57081580','Personales',76),(259,'ALEXANDER SACBA','46072662','Laborales',76),(260,'MAGDA CU','46916836','Laborales',76),(261,'ALMA CU','41150929','Personales',77),(262,'FEDERICO YOJ','40497681','Personales',77),(263,'MIRIAM COC','42493750','Laborales',77),(264,'ALLAN CAAL','39959382','Laborales',77),(265,'ABNER CAAL','30240028','Personales',78),(266,'WILMER SUB','31175245','Personales',78),(267,'BREYNI FERNÁNDEZ','32407470','Laborales',78),(268,'LESLI FERNÁNDEZ','31503929','Laborales',78),(269,'ESTUARDO MERIDA','31341041','Personales',79),(270,'JERVIN GARCIA','50443417','Personales',79),(271,'DONIS CAAL','53711134','Laborales',79),(272,'HAMILTON GAMARRO','53511401','Laborales',79),(273,'EDGAR CU POP','30317932','Personales',81),(274,'SANDRA ALVARADO PÉREZ','39053563','Personales',81),(275,'CÉSAR RONALDO BIN MACZ','40025086','Laborales',81),(276,'MARIA CECILIA CHE POP','49063416','Laborales',81),(277,'ESTUARDO LEAL','46371307','Personales',82),(278,'ESTELA LEAL','41598470','Personales',82),(279,'ALIDA GÓMEZ','47257015','Laborales',82),(280,'LORENA GUAY','42007662','Laborales',82);
/*!40000 ALTER TABLE `FinancialInformation_reference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FinancialInformation_workinginformation`
--

DROP TABLE IF EXISTS `FinancialInformation_workinginformation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FinancialInformation_workinginformation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `position` varchar(150) NOT NULL,
  `company_name` varchar(150) NOT NULL,
  `start_date` date DEFAULT NULL,
  `description` longtext,
  `salary` decimal(10,2) NOT NULL,
  `working_hours` varchar(70) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `source_of_income` varchar(90) NOT NULL,
  `income_detail` longtext,
  `employment_status` varchar(150) NOT NULL,
  `customer_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FinancialInformation_customer_id_id_ce6c4ea9_fk_customers` (`customer_id_id`),
  CONSTRAINT `FinancialInformation_customer_id_id_ce6c4ea9_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FinancialInformation_workinginformation`
--

LOCK TABLES `FinancialInformation_workinginformation` WRITE;
/*!40000 ALTER TABLE `FinancialInformation_workinginformation` DISABLE KEYS */;
INSERT INTO `FinancialInformation_workinginformation` VALUES (4,'PILOTO','EXCEL AUTOMOTRIZ','2024-12-27','',3400.00,'VESPERTINA','22778177','Relación de Dependencia','SALARIO MENSUAL','Empleado a Tiempo Completo',5),(5,'CAJERO GENERAL','BANCO G&T CONTINENTAL','2024-12-10','',5000.00,'VESPERTINA','22861461','Relación de Dependencia','GASTOS VARIOS','Empleado a Tiempo Completo',7),(6,'EJECUTIVO INTEGRAL','BANCO G&T CONTINENTAL','2024-12-10','',4100.00,'VESPERTINA','22861461','Relación de Dependencia','PAGOS MENSUALES','Empleado a Tiempo Completo',8),(7,'AUXILIAR DE TRANSPORTE','Multi perfiles santa cruz alta verapaz','2023-10-01','',4377.82,'VESPERTINA','30376188','Relación de Dependencia','','Empleado a Tiempo Completo',9),(8,'ASISTENTE DE VENTAS','Sherwin Williams','2024-10-01','',7200.00,'VESPERTINA','79521079','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',10),(9,'Técnico de Campo','Coordinadora Nacional para la Reducción de Desastres CONRED',NULL,'',6000.00,'VESPERTINA','31786818','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',11),(10,'LLENADOR AUXILIAR','PURIFICADORA SINAI','2024-02-04','',2800.00,'VESPERTINA','47751562','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',12),(11,'ANALISTA','DELEGACION DEL IGSS','2024-01-21','',5700.00,'VESPERTINA','79521813','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',13),(12,'MANICURISTA','TRABAJO INDEPENDIENTE','2024-02-02','',1900.00,'VESPERTINA','31131442','Relación de Dependencia','GASTOS MENSUALES','Empleado a Tiempo Completo',14),(13,'TECNICO DE CAMPO','MAGA','2024-02-02','',2500.00,'VESPERTINA','77367321','Relación de Dependencia','GASTO MENSUAL','Empleado a Tiempo Completo',15),(14,'JUBILADA','JUBILADA MINEDUC','2023-04-03','',5000.00,'VESPERTINA','58436843','Relación de Dependencia','JUBILADA','Jubilado',16),(15,'MERCADERISTA','COLOCADOR DE RUTA','2024-11-02','',3800.00,'VESPERTINA','42765367','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',17),(16,'GERENTE DE AGENCIA','COOPERATIVA SHARE','2024-10-02','',8000.00,'VESPERTINA','31267157','Relación de Dependencia','GASTOS MENSUALES','Empleado a Tiempo Completo',18),(17,'ASESOR DE CREDITOS','BANCO DE LOS TRABAJADORES','2024-10-02','',7500.00,'VESPERTINA','49050037','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',19),(18,'DEPENDIENTE DE MOSTRADOR','FARMACIA BATRES',NULL,'',4500.00,'VESPERTINA','23003500','Relación de Dependencia','GASTOS MENSUALES','Empleado a Tiempo Completo',20),(19,'PROPIETARIA','NEGOCIO PROPIO','2024-04-27','',4500.00,'VESPERTINA','49711888','Relación de Dependencia','GASTO MENSUALES','Empleado a Tiempo Completo',21),(21,'PROPIETARIO','NEGOCIO PROPIETARIO','2024-10-01','',4500.00,'VESPERTINA','55634365','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',23),(22,'COORDINADOR DE AGENCIA','AGENCIA HONDA MOTOS','2024-05-01','PAGOS MENSUALES',7500.00,'VESPERTINA','41547758','Relación de Dependencia','3 MIL DE COMISIONES','Empleado a Tiempo Completo',24),(23,'PASTOR','IGLESIA MISION CRISTIANA DEL CALVARIO',NULL,'',6000.00,'VESPERTINA','30637619','Relación de Dependencia','GASTOS MENSUALES','Empleado a Tiempo Completo',25),(25,'PROPIETARIA','NEGOCIO PROPIO/COMEDOR LETICIA','2024-02-02','',5000.00,'VESPERTINA','39208802','Relación de Dependencia','GASTOS MENSUALES','Empleado a Tiempo Completo',28),(26,'JEFE DEL DEPARTAMENTO DE RECEPCION','SUPERMERCADO LA TORRE','2024-04-10','',4750.00,'VESPERTINA','33397682','Relación de Dependencia','PAGOS MENSUALES','Empleado a Tiempo Completo',29),(27,'ADMINISTRADOR','NAISA',NULL,'',6500.00,'VESPERTINA','53700472','Relación de Dependencia','GASTOS  MENSUALES','Empleado a Tiempo Completo',30),(28,'ASISTENTE DE SERVICIOS Y NEGOCIOS','BANCO INTERNACIONAL','2024-06-04','',5300.00,'VESPERTINA','50036000','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',31),(29,'PREVENDEDOR','DIANA','2024-05-03','',5000.00,'VESPERTINA','36537621','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',32),(30,'PROPIETARIA','NEGOCIO PROPIO/VARIEDADES LINELY','2024-06-25','',10000.00,'VESPERTINA','35968506','Relación de Dependencia','GASTOS MENSUALES','Empleado a Tiempo Completo',33),(31,'RECEPCIONISTA','CENTRO DENTAL CRISTAL','2024-06-25','',3480.00,'VESPERTINA','79529812','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',34),(32,'AUXILIAR DE CONTROL DE TIENDAS','PANIFICADORA DOÑA LUCIA','2024-10-12','',3600.00,'VESPERTINA','31287749','Relación de Dependencia','GASTOS MENSUALES','Empleado a Tiempo Completo',35),(33,'PROPIETARIA','TACTICOS ADONAY','2016-01-01','',16000.00,'VESPERTINA','41805123','Negocio Propio','VENTA AMBULANTE','Autónomo',36),(34,'SECRETARIA','IGSS','2022-06-01','',6675.17,'VESPERTINA','79521813','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',37),(35,'ASESOR DE VENTAS','CELASA','2024-07-18','',5500.00,'VESPERTINA','77747777','Relación de Dependencia','PAGOS MENSUALES','Empleado a Tiempo Completo',38),(36,'SUBINSPECTOR','POLICIA NACIONAL CIVIL','2023-10-14','',7000.00,'VESPERTINA','40154188','Relación de Dependencia','PAGOS MENSUALES','Empleado a Tiempo Completo',40),(37,'DOCENTE','LACTEOS CAMPO VERDE','2014-06-01','',10000.00,'VESPERTINA','57384627','Relación de Dependencia','GASTOS MENSUALES','Empleado a Tiempo Completo',41),(38,'PROPIETARIA','TIENDA Y VARIEDADES SARITA/CAFETERÍA PA COMER ALGO','2017-01-04','',12000.00,'VESPERTINA','46817463','Negocio Propio','NEGOCIO PROPIO','Empleado a Tiempo Completo',42),(39,'PROPIETARIO','NEGOCIO PROPIO/ ACADEMIA BARRAZA SPORT','2024-06-07','',8000.00,'VESPERTINA','42532182','Relación de Dependencia','GASTOS MENSUALES','Empleado a Tiempo Completo',43),(40,'PLANIFICADOR Y DIGITADOR','HIDROELECTRICA RENACE','2023-05-04','',12000.00,'VESPERTINA','23283500','Relación de Dependencia','PAGOS MENSUALES, SEDE CENTRAL','Empleado a Tiempo Completo',44),(41,'CONTADOR GENERAL','CHORIBURGER','2023-10-13','',3950.00,'VESPERTINA','51054739','Relación de Dependencia','PAGOS MENSUALES','Empleado a Tiempo Completo',46),(42,'PROPIETARIO','TALLER DE ARTESANIAS','2024-10-18','TRABAJO DE MANERA AUTONOMA',5000.00,'VESPERTINA','46418726','Negocio Propio','','Autónomo',47),(44,'JEFE REGIONAL MICROCREDITO','BANCO ANTIGUA','2024-06-19','',17000.00,'VESPERTINA','24173952','Relación de Dependencia','PAGOS MENSUALES','Empleado a Tiempo Completo',49),(45,'INSTRUCTORA/ PROPIETARIA','ACADEMIA RENOVARTE','2024-02-28','',12000.00,'VESPERTINA','40962743','Relación de Dependencia','PAGO MENSUAL','Empleado a Tiempo Completo',50),(46,'GERENTE DE COOPERACION','MUNICIPALIDAD DE COBAN','2023-08-14','',7000.00,'VESPERTINA','79553232','Relación de Dependencia','CAPITAL DE TRABAJ0','Empleado a Tiempo Completo',51),(47,'OFICIAL DE FISCALIA I','MINISTERIO PUBLICO',NULL,'',8000.00,'VESPERTINA','79514607','Relación de Dependencia','GASTOS VARIOS','Empleado a Tiempo Completo',52),(48,'Encargada de tienda','Optical Center plaza del  ParqueOptical Center plaza del  Parque','2024-11-06','',3500.00,'VESPERTINA','23020622','Relación de Dependencia','GASTOS VARIOS','Empleado a Tiempo Completo',53),(49,'PROPIETARIA','NEGOCIO PROPIO/ MUJER BONITA COSMÉTICOS Y ACCESORIOS','2024-11-07','',15000.00,'VESPERTINA','50418141','Relación de Dependencia','GASTOS VARIOS','Empleado a Tiempo Completo',54),(50,'ASESORA INMOBILIARIA','Desarrollos inmobiliarios Chipoc.','2024-07-15','',12500.00,'VESPERTINA','55104517','Relación de Dependencia','GASTOS VARIOS','Empleado a Tiempo Completo',55),(51,'ASESOR DE VENTAS','RESIDENCIALES PORTAL DEL BOSQUE','2024-07-15','',6000.00,'VESPERTINA','30571105','Relación de Dependencia','GASTOS VARIOS','Empleado a Tiempo Completo',56),(52,'MONITOR DE SALUD','COOPERATIVA COBAN','2024-07-15','',4050.00,'VESPERTINA','79417332','Relación de Dependencia','GASTOS VARIOS','Empleado a Tiempo Completo',57),(53,'TECNICO ADMINISTRATIVO DE CAMPO','DIDEDUC, A.V.','2024-08-06','',5000.00,'VESPERTINA','79510080','Relación de Dependencia','GASTOS VARIOS','Empleado a Tiempo Completo',58),(54,'PILOTO','MINISTERIO PUBLICO-SANTA CRUZ VERAPAZ','2024-02-25','',5000.00,'VESPERTINA','23602449','Relación de Dependencia','GASTOS VARIOS','Empleado a Tiempo Completo',59),(55,'ASISTENTE DE ANALISIS','MINISTERIO PÚBLICO','2024-02-27','',13713.70,'VESPERTINA','24119191','Relación de Dependencia','GASSTOS VARIOS','Empleado a Tiempo Completo',60),(56,'GUARDIAN','MERCADO CENTRAL','2024-04-11','',3138.00,'VESPERTINA','79514900','Relación de Dependencia','GASTOS VARIOS','Empleado a Tiempo Completo',61),(57,'PROFESOR','EORM ALDEA BANCAB',NULL,'',9750.00,'VESPERTINA','79566600','Relación de Dependencia','Consultorías  Q 20,000 anual','Empleado a Tiempo Completo',62),(58,'COCINERO','SAN MARTIN','2024-10-04','',5000.00,'VESPERTINA','24209974','Relación de Dependencia','Gastos mensuales','Empleado a Tiempo Completo',63),(59,'PROPIETARIO','EMPRESA REPUESTOS BELEN','2021-12-15','',15000.00,'VESPERTINA','40689250','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',65),(60,'ASESOR DE CREDITOS','BANCO DE LOS TRABAJADORES','2024-08-05','',5000.00,'VESPERTINA','22247650','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',66),(61,'ESTILISTA','SALÓN ADHARA','2024-05-31','',3250.00,'VESPERTINA','51923239','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',67),(62,'ORIENTADOR ESPIRITUAL/SACERDOTE','LICEO BRESSANI/ SACERDOTE','2024-11-19','',9000.00,'VESPERTINA','79521633','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',68),(63,'COACH- SERVICIO AL CLIENTE','MCDONALDS','2024-11-19','',4500.00,'VESPERTINA','23606363','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',69),(64,'CAJERO ANTENCION AL CLIENTE','MCDONALDS','2024-11-19','',3200.00,'VESPERTINA','23606363','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',70),(65,'SECRETARIA','COLEGIO DE ABOGADOS','2023-06-15','',4000.00,'VESPERTINA','79514492','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',71),(66,'DOCENTE','ESCUELA OFICIAL RURAL MIXTA ALDEA GUAXPAC','2024-08-01','',7500.00,'VESPERTINA','59035523','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',72),(67,'ASISTENTE DE ENCARGADO DE TIENDA','DOMINOZ EXPRESS','2024-11-21','',4200.00,'VESPERTINA','55154953','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',73),(68,'AUXILIAR DE ENFERMERIA','HOSPITAL REGIONAL DE COBAN','2024-03-15','',4700.00,'VESPERTINA','79316333','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',74),(69,'PILOTO VENDEDOR','AVICOLA VILLALOBOS S.A','2024-11-27','',5000.00,'VESPERTINA','22002400','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',75),(70,'COLOCADOR','SUPER MERCADO SUMA','2024-06-20','',4300.00,'VESPERTINA','2319005','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',76),(71,'COLOCADOR DE PRODUCTOS','SUPERMERCADO LA TORRE','2024-09-18','',3500.00,'VESPERTINA','33397682','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',77),(72,'COBRADOR','MEGACASH','2023-03-22','',7000.00,'VESPERTINA','35911407','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',78),(73,'COORDINADOR DE MEDIO AMBIENTE Y GESTIÓN SOCIAL','HIDROELECTRICA RENACE','2024-12-18','',17890.00,'VESPERTINA','23283500','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',79),(74,'DOCENTE','EORM Aldea Las Flores Chito','2024-12-20','',7591.50,'VESPERTINA','57886821','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',81),(75,'RASTREADORA','DIRECCIÓN DE ÁREA DE SALUD DE ALTA VERAPAZ','2023-06-13','',3000.00,'VESPERTINA','79516786','Relación de Dependencia','GASTOS PERSONALES','Empleado a Tiempo Completo',82);
/*!40000 ALTER TABLE `FinancialInformation_workinginformation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `InvestmentPlan_investmentplan`
--

DROP TABLE IF EXISTS `InvestmentPlan_investmentplan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `InvestmentPlan_investmentplan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type_of_product_or_service` varchar(75) NOT NULL,
  `total_value_of_the_product_or_service` decimal(15,2) NOT NULL,
  `investment_plan_description` longtext,
  `initial_amount` decimal(15,2) NOT NULL,
  `monthly_amount` decimal(15,2) NOT NULL,
  `transfers_or_transfer_of_funds` tinyint(1) NOT NULL,
  `type_of_transfers_or_transfer_of_funds` varchar(75) NOT NULL,
  `investment_plan_code` varchar(25) NOT NULL,
  `customer_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `investment_plan_code` (`investment_plan_code`),
  KEY `InvestmentPlan_inves_customer_id_id_2328b8d4_fk_customers` (`customer_id_id`),
  CONSTRAINT `InvestmentPlan_inves_customer_id_id_2328b8d4_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `InvestmentPlan_investmentplan`
--

LOCK TABLES `InvestmentPlan_investmentplan` WRITE;
/*!40000 ALTER TABLE `InvestmentPlan_investmentplan` DISABLE KEYS */;
INSERT INTO `InvestmentPlan_investmentplan` VALUES (2,'CONSUMO',3000.00,'CONSUMO',3000.00,3000.00,1,'Local','2024-1/C1',5),(3,'CONSUMO',10000.00,'GASTOS VARIOS',10000.00,10000.00,1,'Local','2024-2/C1',7),(4,'CONSUMO',10000.00,'GASTOS VARIOS',10000.00,10000.00,1,'Local','2024-3/C1',8),(5,'CONSUMO',4377.82,'GASTOS VARIOS',4377.82,4377.82,1,'Local','2024-4/C1',9),(6,'CONSUMO',2000.00,'GASTOS VARIOS',2000.00,2000.00,1,'Local','2025-1/C1',10),(7,'CONSUMO',5000.00,'GASTOS PERSONALES',5000.00,5000.00,1,'Local','2025-2/C1',11),(8,'CONSUMO',1300.00,'GASTOS VARIOS',1300.00,1300.00,1,'Local','2025-3/C1',12),(9,'CONSUMO',4000.00,'GASTOS PERSONALES',4000.00,4000.00,1,'Local','2025-4/C1',13),(10,'CONSUMO',2000.00,'GASTOS PERSONALES',2000.00,2000.00,1,'Local','2025-5/C1',14),(11,'CONSUMO',2000.00,'GASTOS PERSONALES',2000.00,2000.00,1,'Local','2025-6/C1',15),(12,'CONSUMO',3000.00,'GASTOS PERSONALES',3000.00,3000.00,1,'Local','2025-7/C1',16),(13,'CONSUMO',2000.00,'GASTOS PERSONALES',2000.00,2000.00,1,'Local','2025-8/C1',17),(14,'CONSUMO',7000.00,'GASTOS PERSONALES',7000.00,7000.00,1,'Local','2025-9/C1',18),(15,'CONSUMO',2000.00,'GASTOS PERSONALES',2000.00,2000.00,1,'Local','2025-10/C1',19),(16,'CONSUMO',5000.00,'GASTOS PERSONALES',5000.00,5000.00,1,'Local','2025-11/C1',20),(17,'CONSUMO',4000.00,'GASTOS PERSONALES',4000.00,4000.00,1,'Local','2025-12/C1',21),(18,'CONSUMO',4000.00,'GASTOS PERSONALES',4000.00,4000.00,1,'Local','2025-13/C1',23),(19,'COMERCIO',15000.00,'GASTOS PERSONALES',15000.00,15000.00,1,'Local','2025-14/C1',24),(20,'CONSUMO',10000.00,'GASTOS PERSONALES',10000.00,10000.00,1,'Local','2025-15/C1',25),(22,'CONSUMO',10000.00,'GASTOS PERSONALES',10000.00,10000.00,1,'Local','2025-16/C1',28),(23,'CONSUMO',2000.00,'GASTOS VARIOS',2000.00,2000.00,1,'Local','2025-17/C1',29),(24,'CONSUMO',3000.00,'GASTOS PERSONALES',3000.00,3000.00,1,'Local','2025-18/C1',30),(25,'CONSUMO',3000.00,'GASTOS VARIOS',3000.00,3000.00,1,'Local','2025-19/C1',31),(26,'CONSUMO',5000.00,'GASTOS PERSONALES',5000.00,5000.00,1,'Local','2025-20/C1',32),(27,'CONSUMO',5000.00,'GASTOS PERSONALES',5000.00,5000.00,1,'Local','2025-21/C1',33),(28,'COMERCIO',10000.00,'CAPITAL DE TRABAJO',10000.00,10000.00,1,'Local','2025-22/C1',34),(29,'CONSUMO',3000.00,'GASTOS PERSONALES',3000.00,3000.00,1,'Local','2025-23/C1',35),(30,'COMERCIO',15000.00,'CAPITAL DE TRABAJO/ COMERCIO',15000.00,15000.00,1,'Local','2025-24/C1',36),(31,'CONSUMO',5000.00,'GASTOS PERSONALES',5000.00,5000.00,1,'Local','2025-25/C1',37),(32,'CONSUMO',8000.00,'GASTOS VARIOS',8000.00,8000.00,1,'Local','2025-26/C1',38),(33,'COMERCIO',15000.00,'CAPITAL DE TRABAJO',15000.00,15000.00,1,'Local','2025-27/C1',40),(34,'CONSUMO',100000.00,'GASTOS PERSONALES',100000.00,100000.00,1,'Local','2025-28/C1',41),(35,'COMERCIO',20000.00,'CAPITAL DE TRABAJO',20000.00,20000.00,1,'Local','2025-29/C1',42),(36,'CONSUMO',6000.00,'GASTOS PERSONALES',6000.00,6000.00,1,'Local','2025-30/C1',43),(37,'CONSUMO',30000.00,'GASTOS VARIOS',30000.00,30000.00,1,'Local','2025-31/C1',44),(38,'CONSUMO',2000.00,'GASTOS VARIOS',2000.00,2000.00,1,'Local','2025-32/C1',46),(39,'COMERCIO',3500.00,'CAPITAL DE TRABAJO',3500.00,3500.00,1,'Local','2025-33/C1',47),(40,'CONSUMO',10000.00,'',10000.00,10000.00,1,'Local','2025-34/C1',49),(41,'CONSUMO',15000.00,'GASTOS PERSONALES',15000.00,150000.00,1,'Local','2025-35/C1',50),(42,'CONSUMO',5000.00,'GASTOS VARIOS',5000.00,5000.00,1,'Local','2025-36/C1',51),(43,'CONSUMO',15000.00,'CAPITAL DE TRABAJO',15000.00,15000.00,1,'Local','2025-37/C1',52),(44,'CONSUMO',15000.00,'CAPITAL DE TRABAJO',15000.00,15000.00,1,'Local','2025-38/C1',53),(45,'CONSUMO',10000.00,'CAPITAL DE TRABAJO',10000.00,10000.00,1,'Local','2025-39/C1',54),(46,'CONSUMO',10000.00,'CAPITAL DE TRABAJO',10000.00,10000.00,1,'Local','2025-40/C1',55),(47,'CONSUMO',10000.00,'CAPITAL DE TRABAJO',10000.00,10000.00,1,'Local','2025-41/C1',56),(48,'SERVICIOS',10000.00,'CAPITAL DE TRABAJO',10000.00,10000.00,1,'Local','2025-42/S1',57),(49,'CONSUMO',2500.00,'CAPITAL DE TRABAJO',2500.00,2500.00,1,'Local','2025-43/C1',58),(50,'CONSUMO',117000.00,'CAPITAL DE TRABAJO',117000.00,117000.00,1,'Local','2025-44/C1',59),(51,'CONSUMO',117000.00,'CAPITAL DE TRABAJO',117000.00,117000.00,1,'Local','2025-45/C1',60),(52,'CONSUMO',5000.00,'CAPITAL DE TRABAJO',5000.00,5000.00,1,'Local','2025-46/C1',61),(53,'CONSUMO',38000.00,'GASTOS VARIOS',38000.00,38000.00,1,'Local','2025-47/C1',62),(54,'CONSUMO',3000.00,'GASTOS VARIOS',3000.00,3000.00,1,'Local','2025-48/C1',63),(55,'COMERCIO',8000.00,'CAPITAL DE TRABAJO',8000.00,8000.00,1,'Local','2025-49/C2',65),(56,'CONSUMO',4000.00,'GASTOS VARIOS',4000.00,4000.00,1,'Local','2025-50/C1',66),(57,'CONSUMO',6000.00,'GASTOS VARIOS',6000.00,6000.00,1,'Local','2025-51/C1',67),(58,'CONSUMO',15000.00,'GASTOS VARIOS',15000.00,15000.00,1,'Local','2025-52/C1',68),(59,'CONSUMO',4000.00,'GASTOS VARIOS',4000.00,4000.00,1,'Local','2025-53/C1',69),(60,'CONSUMO',4000.00,'GASTOS VARIOS',4000.00,4000.00,1,'Local','2025-54/C1',70),(61,'CONSUMO',75000.00,'GASTOS VARIOS',7500.00,7500.00,1,'Local','2025-55/C1',71),(62,'CONSUMO',3000.00,'GASTOS VARIOS',3000.00,3000.00,1,'Local','2025-56/C1',72),(63,'CONSUMO',2000.00,'GASTOS VARIOS',2000.00,2000.00,1,'Local','2025-57/C1',73),(64,'CONSUMO',10000.00,'GASTOS VARIOS',10000.00,10000.00,1,'Local','2025-58/C1',74),(65,'CONSUMO',5000.00,'GASTOS VARIOS',5000.00,5000.00,1,'Local','2025-59/C1',75),(66,'CONSUMO',5000.00,'GASTOS VARIOS',5000.00,5000.00,1,'Local','2025-60/C1',76),(67,'CONSUMO',5000.00,'GASTOS VARIOS',5000.00,5000.00,1,'Local','2025-61/C1',77),(68,'CONSUMO',4000.00,'GASTOS VARIOS',4000.00,4000.00,1,'Local','2025-62/C1',78),(69,'CONSUMO',15000.00,'GASTOS VARIOS',15000.00,15000.00,1,'Local','2025-63/C1',79),(70,'CONSUMO',20000.00,'GASTOS VARIOS',20000.00,20000.00,1,'Local','2025-64/C1',81),(71,'CONSUMO',5000.00,'GASTOS VARIOS',5000.00,5000.00,1,'Local','2025-65/C1',82);
/*!40000 ALTER TABLE `InvestmentPlan_investmentplan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `addresses_address`
--

DROP TABLE IF EXISTS `addresses_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses_address` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `street` varchar(120) NOT NULL,
  `number` varchar(90) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(90) NOT NULL,
  `country` varchar(90) NOT NULL,
  `type_address` varchar(90) NOT NULL,
  `latitud` varchar(120) NOT NULL,
  `longitud` varchar(120) NOT NULL,
  `customer_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `addresses_address_customer_id_id_4be9b657_fk_customers` (`customer_id_id`),
  CONSTRAINT `addresses_address_customer_id_id_4be9b657_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses_address`
--

LOCK TABLES `addresses_address` WRITE;
/*!40000 ALTER TABLE `addresses_address` DISABLE KEYS */;
INSERT INTO `addresses_address` VALUES (6,'2da Calle B14-20 Colonia Saclack','1','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.472373','-90383255',5),(7,'1 Avenida 14-204 Lotificacion Carlos V','12','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.456562819686788','-90.39232339078104',5),(9,'06 CALLE 15-76','4','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.470232','-90.367956',7),(10,'1RA. CALLE 7-28','12','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.47074126682795','-90.3757720042732',7),(11,'3 CALLE 10-24','3','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.469292','-90.364928',8),(12,'1RA. CALLE 7-28','12','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.471337906025896','-90.4025559910132',8),(13,'3av 8-13','10','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.477679','-90.368581',9),(14,'2 CALLE','10','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.477679','-90.368581',9),(15,'10 Avenida 5-58','12','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.465309','-90.399881',10),(16,'1A CALLE 14-85','1','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.47740108162323','-90.38434383519231',10),(17,'6ta avenida, 5 -66 \"a\"  Barrio Chiu','3','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.465132','-90.368303',11),(18,'Calle 1-76','4','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.475674382210766','-90.37095358522787',11),(19,'12 AV 3-11 ESFUERZO 2','12','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.468336','-90.404245',12),(20,'COBAN A.V','12','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.464934189572267','-90.37296706820675',12),(21,'15av 3-70','12','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.465558','-90.405501',13),(22,'5ta calle 5-38','4','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15,471331','-90,375896',13),(23,'2.DA CALLE  BARRIO CHIBUJBU SAN PEDRO CARCHA A.V','5','Alta Verapaz','San Pedro Carcha','GUATEMALA','Dirección Personal','15.481589','-90.307022',14),(24,'SAN PEDRO CARCHA','5','Alta Verapaz','San Pedro Carcha','GUATEMALA','Dirección de Trabajo','15.481589','-90.307022',14),(25,'2DA CALLE BARRIO CHIBUJBU','5','Alta Verapaz','San Pedro Carcha','GUATEMALA','Dirección Personal','15.481537','-90.306979',15),(26,'Km 210 Finca Sachamach, CA14,','12','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.46287220738868','-90.39170269259625',15),(27,'RESIDENCIALES IMPERIAL','7','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.463723','-90.367348',16),(28,'RESIDENCIALES IMPERIAL','7','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.463723','-90.367348',16),(29,'Comunidad sachamach lll','0','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.465156','-90.393810',17),(30,'COBAN A.V','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.465156','-90.393810',17),(31,'Aldea San Benito Clle II Fray Bartolome de las Casas a 150 meto de la entrada de naturaceites','0','Alta Verapaz','FRAY BARTOLOME DE LAS CASAS','GUATEMALA','Dirección Personal','15.801856','-89.838440',18),(32,'Placita arcely segundo nivel de renap Fray Bartolome de las Casas.','0','Alta Verapaz','FRAY BARTOLOME DE LAS CASAS','GUATEMALA','Dirección de Trabajo','15.806977534419815','-89.86082176165908',18),(33,'CANTON LAS CASAS POR EL TANQUE DE AGUA','8','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.459699','-90.372911',19),(34,'COBAN A.V','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.470890268789757','-90.38536993413898',19),(35,'Cobán 2, 03 CL 0002 08-040','2','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.468134,','-90.364191',20),(36,'ZONA 4 COBÁN A. V.','4','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.47175541232787','-90.3846314553206',20),(37,'4av 1-89','8','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.462729','-90.367124',21),(38,'COBAN A.V','8','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.462729','-90.367124',21),(41,'4av1-89','8','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.462595','-90.367157',23),(42,'COBAN A.V','8','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.462595','-90.367157',23),(43,'4TA CALLE 8-45','6','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.468871528219402','-90.36525923334155',24),(44,'1a Calle 13-98','1','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.470860366726603','-90.38167900450567',24),(45,'COMUNIDAD CUBILGUITZ, REFERENCIA CENTRO DE VENTAS CUBIL','0','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.666918','-90.429244',25),(46,'COMUNIDAD CUBILGUITZ','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.666918','-90.429244',25),(50,'COMUNIDAD CUBILGUITZ','0','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.666856','-90.429287',28),(51,'COMUNIDAD CUBILGUITZ','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.666856','-90.429287',28),(52,'Barrio Esquipulas','5','Alta Verapaz','San Cristobal Verapaz','GUATEMALA','Dirección Personal','15.356420532115008','-90.47814274666021',29),(53,'1a Calle 313','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.470853606831621','-90.37493219286416',29),(54,'COLONIA LAS ILUSIONES','5','Alta Verapaz','San Pedro Carcha','GUATEMALA','Dirección Personal','15.479500','-90.309770',30),(55,'NAISA','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','16.22947870651439','-90.15400943494413',30),(56,'07 AVENIDA LOTE 56 COLONIA EL ESFUERZO 1','12','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.467274507590945','-90.39814531665843',31),(57,'8a Avenida 1-11','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.471186981741724','-90.37879770185094',31),(58,'5 CALLE 5-55','3','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.475117','-90.390518',32),(59,'COBAN, A.V','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','14.629846868332782','-90.4966022799108',32),(60,'Comunidad Satiz','6','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.463202','-90.385526',33),(61,'NEGOCIO PROPIO/VARIEDADES LINELY','6','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.463202','-90.385526',33),(62,'3RA CALLE 9-77  BARRIO SAN VICENTE','6','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.467389155788858','-90.38620257845311',34),(63,'1a Calle 935','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.47126638384735','-90.3803869297943',34),(64,'Barrio El Chorro, Tactic, Alta Verapaz (Callejon frente al campo colorado)','0','Alta Verapaz','Tactic','GUATEMALA','Dirección Personal','15.316282','-90.352645',35),(65,'TACTIC, ALTA VERAPAZ','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.3198942661257','-90.3523941420635',35),(66,'CALLE EL VALVARIO 8055','3','Alta Verapaz','San Cristobal Verapaz','GUATEMALA','Dirección Personal','15.366808','-90.485834',36),(67,'CALLE EL VALVARIO 8055','5','Alta Verapaz','San Cristobal Verapaz','GUATEMALA','Dirección de Trabajo','15.366808','-90.485834',36),(68,'7MA AV 12-69 ZONA 2 SAN PEDRO CARCHA','2','Alta Verapaz','San Pedro Carcha','GUATEMALA','Dirección Personal','15.473118','-90.367589',37),(69,'FJFJ+5X7, 8a Avenida, Cobán','4','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.473089964831408','-90.36754718892975',37),(70,'3ra calle 3-15','12','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.470027','-90.395020',38),(71,'1ra calle 8-15','4','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.471636258912225','-90.36711241753565',38),(73,'SAN CRISTOBAL CALLE CALVARIO','3','Alta Verapaz','San Cristobal Verapaz','GUATEMALA','Dirección Personal','15.366808','-90.485834',40),(74,'7.MA AVENIDA','6','Baja Verapaz','Santa Cruz Verapaz','GUATEMALA','Dirección de Trabajo','15.104533314082497','-90.31807307219069',40),(75,'LAS CRUCES TONTEM','0','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.427090','-90.388584',41),(76,'LAS CRUCES TONTEM','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.427090','-90.388584',41),(77,'04 CL 8145','6','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.457231676393397','-90.38664586197011',42),(78,'10 AV. 4 -03 B','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.469066854793907','-90.3789531962486',42),(79,'11 A.V 5-02 \"A\"','3','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.468082','-90.364179',43),(80,'CANCHA BRESANI COBAN A.V','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.468082','-90.364179',43),(81,'ALDEA CHAJSAQUIL','0','Alta Verapaz','San Pedro Carcha','GUATEMALA','Dirección Personal','15.469891','90.299183',44),(82,'21 kilómetros dentro del municipio de San Pedro Carchá','0','Alta Verapaz','San Pedro Carcha','GUATEMALA','Dirección de Trabajo','15.510231346807581','-90.24121803533994',44),(84,'COLONIA 30 DE JUNIO LOTE 7','1','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.473152','-90.386242',46),(85,'CA-14, Cobán, Kilómetro 200 ruta a coban','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.397207680098767','-90.40984743958268',46),(86,'CALLE PRINCIPAL FRENTE AL CRUCE DE LA ESCUELA SECTOR 1 BARRIO CHAJSAQUIL','9','Alta Verapaz','San Pedro Carcha','GUATEMALA','Dirección Personal','15.470838879694961','-90.29921357214451',47),(87,'CALLE PRINCIPAL FRENTE AL CRUCE DE LA ESCUELA SECTOR 1 BARRIO CHAJSAQUIL','9','Alta Verapaz','San Pedro Carcha','GUATEMALA','Dirección de Trabajo','15.470838879694961','-90.29921357214451',47),(89,'COLONIA EL ESFUERZO 1','0','Alta Verapaz','FRAY BARTOLOME DE LAS CASAS','GUATEMALA','Dirección Personal','15.804837','-89.851144',49),(90,'Lote 280 calle principal barrio el Magisterio','1','Alta Verapaz','FRAY BARTOLOME DE LAS CASAS','GUATEMALA','Dirección de Trabajo','15.80352791946753','-89.86687363068678',49),(91,'8VA AV 1-12','1','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.470971','-90.378900',50),(92,'1AV 1-12','1','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.471280','-90.378845',50),(93,'4a. Avenida 8-90','8','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.468601709924162','-90.37051932170007',51),(94,'1RA CALLE1-11','1','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.470754061900358','-90.3732951423283',51),(95,'CHAMELCO, BARRIO SAN JUAN- FRENTE A RENAP','0','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.423198','-90.336279',52),(96,'FJCF+VPX, Cobán','11','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.47247534549196','-90.37558903125809',52),(97,'3a. Calle Chivencorral 11-056','12','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.468674','-90.403434',53),(98,'1ra. calle 3-13','1','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.47082562665615','-90.37487560427317',53),(99,'BARRIO CEMENTERIO, FRAY BARTOLOME DE LAS CASAS ALTA VERAPAZ','0','Alta Verapaz','FRAY BARTOLOME DE LAS CASAS','GUATEMALA','Dirección Personal','15.804588','-89.864629',54),(100,'FRAY BARTOLOME DE LAS CASAS ALTA VERAPAZ','0','Alta Verapaz','FRAY BARTOLOME DE LAS CASAS','GUATEMALA','Dirección de Trabajo','15.804588','-89.864629',54),(101,'6ta calle 4-18','3','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.467014','-90.369996',55),(102,'Desarrollos inmobiliarios Chipoc. Legado Cobán','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.470622917459478','-90.380397622742',55),(103,'COLONIA PETET A 30 METROS DE LA ESCUELA DE PARVULOS','12','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.469930','-90.404995',56),(104,'COBAN, ALTA VERAPAZ','12','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.471779666462247','-90.39537089066776',56),(105,'2.DA CALLE 0-40  BARRIO SAN SEBASTIAN','2','Alta Verapaz','San Cristobal Verapaz','GUATEMALA','Dirección Personal','15.367443','-90.479505',57),(106,'3ra. Avenida 1-05','4','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.472075953479028','-90.38575188913755',57),(107,'12 AV 3-29  BARRIO LAS CARMELITAS','10','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.479014','-90.359012',58),(108,'a 1ª calle 5-19','1','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.472875453545557','-90.37562781949691',58),(109,'9a. Avenida 16-39  Lotificación Gualom','11','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.424433','-90.328903',59),(110,'FISCALIA DE SANTA CRUZ','3','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.475976606857158','-90.37537251312678',59),(111,'9a. Avenida 16-39 Lotificación Gualom','11','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.485258','-90.378266',60),(112,'COBAN ALTA VERAPAZ','1','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.473442666754742','-90.37319987651833',60),(113,'1a Calle 7-19 chajxucub','11','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.485591','-90.372554',61),(114,'3a CALLE COBAN A.V','3','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.469740067678853','-90.37255500427321',61),(115,'Lote 58, Sectori del Río, Residenciales Raxpec, San Pedro Carchá, Alta Verapaz','5','Alta Verapaz','San Pedro Carcha','GUATEMALA','Dirección Personal','15.484345','-90.310964',62),(116,'7a. calle 1-11','6','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.464910173768567','-90.38977020242235',62),(117,'barrio la libertad, callejón al lado de la escuela, enfrente del tanque de agua','11','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.484404','-90.366752',63),(118,'1era calle 15.20','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.468934499512944','-90.38229525099365',63),(120,'5TA.CALLE 7-16','3','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.467995','-90.367817',65),(121,'2 CALLE 10-74 SAN MARCOS','5','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.472353518463779','-90.36484211682864',65),(122,'10 AVENIDA 5-11','12','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.467468704683434','-90.40133612718724',66),(123,'COBAN A.V','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.4704909630646','-90.38506265314656',66),(124,'Colonia Chichochoc Cobán','5','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.471307201070347','-90.38924712651014',67),(125,'Diagonal 4 9-27','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','16.26546572176092','-90.40506247575486',67),(126,'01 AV 01-031','3','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.470368','-90.380058',68),(127,'1RA. AVENIDA5-56','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.470612012723205','-90.37786462147817',68),(128,'4.TA AVENIDA 5-40','3','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.466779','-90.370384',69),(129,'1.A CALLE 15-12','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.473439811457947','-90.38478783269126',69),(130,'5.TA AVENIDA 8-24','3','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.468073','-90.366882',70),(131,'1A. CALLE 15-12','2','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.474736757479889','-90.38874991111976',70),(132,'05 CL A 05-081','7','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.462467','-90.369975',71),(133,'7a Avenida','1','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.471716306343453','-90.37834230427318',71),(134,'8 AVENIDA TACTIC A.V','1','Alta Verapaz','Tactic','GUATEMALA','Dirección Personal','15.316705452109375','-90.35074274988649',72),(135,'TACTIC ALTA VERAPAZ','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.326150844184701','-90.35246600289895',72),(136,'8va. Calle 11-54','10','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.477131','-90.364092',73),(137,'SAN CRISTOBAL, ALTA VERAPAZ','0','Alta Verapaz','Santa Cruz Verapaz','GUATEMALA','Dirección de Trabajo','15.31910055490628','-90.35117656256699',73),(138,'6to Acceso 6-28 B, Barrio Chajxucub Cobán A.V.','11','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.482934','-90.372380',74),(139,'8ª. Calle 1-24','11','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.480081841695764','-90.37283507709381',74),(140,'9a ave 4-25','12','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.466441853380367','-90.39878815413287',75),(141,'46 calle 21-89','12','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.4700533082554','-90.36649495824302',75),(142,'Balniario la colonia, caserio los cipresales','0','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','14.679100436374119','-91.3115140331248',76),(143,'CAMINO A CARCHA, COBAN','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.473804124034555','-90.35557172015241',76),(144,'KM 203 ALDEA TOMTEM A UN CONSTADO DE LA ESCUELA','0','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.415185803615257','-90.40279504604305',77),(145,'1A CALLE 313 COBÁN','1','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.470853606831584','-90.37477126009396',77),(146,'ESFUERZO COBAN AV','12','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.46384377200017','-90.40194786618284',78),(147,'15 AVENIDA','12','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.470722548733603','-90.37441075844957',78),(148,'11 A 11-65, colonia el esfuerzo 2','12','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.473505402404118','-90.39031546171702',79),(149,'SAN PEDRO CARCHA','0','Alta Verapaz','San Pedro Carcha','GUATEMALA','Dirección de Trabajo','15.490801445970751','-90.22322140574005',79),(151,'ALDEA TONTEM','0','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.415458461277257','-90.40241585724449',81),(152,'ALDEA LAS FLORES CHITOC','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.670057554760682','-90.47662023951565',81),(153,'06 Avenida','4','Alta Verapaz','Coban','GUATEMALA','Dirección Personal','15.473538499223691','-90.37663861534335',82),(154,'SAN PEDRO CARCHÁ','0','Alta Verapaz','Coban','GUATEMALA','Dirección de Trabajo','15.473946831890155','-90.31126508181315',82);
/*!40000 ALTER TABLE `addresses_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `addresses_departamento`
--

DROP TABLE IF EXISTS `addresses_departamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses_departamento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses_departamento`
--

LOCK TABLES `addresses_departamento` WRITE;
/*!40000 ALTER TABLE `addresses_departamento` DISABLE KEYS */;
INSERT INTO `addresses_departamento` VALUES (1,'Alta Verapaz'),(2,'Baja Verapaz'),(3,'Chimaltenango'),(4,'Chiquimula'),(5,'El Progreso'),(6,'Escuintla'),(7,'Guatemala'),(8,'Huehuetenango'),(9,'Izabal'),(10,'Jalapa'),(11,'Jutiapa'),(12,'Peten'),(13,'Quetzaltenango'),(14,'Quiche'),(15,'Retalhuleu'),(16,'Sacatepequez'),(17,'San Marcos'),(18,'Santa Rosa'),(19,'Solola'),(20,'Suchitepquez'),(21,'Totonicapan'),(22,'Zacapa');
/*!40000 ALTER TABLE `addresses_departamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `addresses_municiopio`
--

DROP TABLE IF EXISTS `addresses_municiopio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses_municiopio` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `depart_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `addresses_municiopio_depart_id_5cef7447_fk_addresses` (`depart_id`),
  CONSTRAINT `addresses_municiopio_depart_id_5cef7447_fk_addresses` FOREIGN KEY (`depart_id`) REFERENCES `addresses_departamento` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses_municiopio`
--

LOCK TABLES `addresses_municiopio` WRITE;
/*!40000 ALTER TABLE `addresses_municiopio` DISABLE KEYS */;
INSERT INTO `addresses_municiopio` VALUES (1,'Coban',1),(2,'San Pedro Carcha',1),(3,'Santa Cruz Verapaz',1),(4,'San Cristobal Verapaz',1),(5,'Tactic',1),(6,'Guatemala',7),(7,'Santa Catarina Pinula',7),(8,'San Jose Pinula',7),(9,'Mixco',7),(10,'Villa Nueva',7),(11,'Quetzaltenango',13),(12,'Salcaja',13),(13,'San Carlos Sija',13),(14,'Olintepeque',13),(15,'La Esperanza',13),(16,'Zacapa',22),(17,'Estanzuela',22),(18,'Rio Hondo',22),(19,'Teculutan',22),(20,'Usumatlan',22),(21,'FRAY BARTOLOME DE LAS CASAS',1);
/*!40000 ALTER TABLE `addresses_municiopio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=189 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Usuario',6,'add_user'),(22,'Can change Usuario',6,'change_user'),(23,'Can delete Usuario',6,'delete_user'),(24,'Can view Usuario',6,'view_user'),(25,'Can add Cliente',7,'add_customer'),(26,'Can change Cliente',7,'change_customer'),(27,'Can delete Cliente',7,'delete_customer'),(28,'Can view Cliente',7,'view_customer'),(29,'Can add Condicion Migratoria',8,'add_immigrationstatus'),(30,'Can change Condicion Migratoria',8,'change_immigrationstatus'),(31,'Can delete Condicion Migratoria',8,'delete_immigrationstatus'),(32,'Can view Condicion Migratoria',8,'view_immigrationstatus'),(33,'Can add Rol',9,'add_role'),(34,'Can change Rol',9,'change_role'),(35,'Can delete Rol',9,'delete_role'),(36,'Can view Rol',9,'view_role'),(37,'Can add Rol de Usuario',10,'add_userrole'),(38,'Can change Rol de Usuario',10,'change_userrole'),(39,'Can delete Rol de Usuario',10,'delete_userrole'),(40,'Can view Rol de Usuario',10,'view_userrole'),(41,'Can add Codigo',11,'add_code'),(42,'Can change Codigo',11,'change_code'),(43,'Can delete Codigo',11,'delete_code'),(44,'Can view Codigo',11,'view_code'),(45,'Can add Imagen',12,'add_imagen'),(46,'Can change Imagen',12,'change_imagen'),(47,'Can delete Imagen',12,'delete_imagen'),(48,'Can view Imagen',12,'view_imagen'),(49,'Can add Imagen de Dirección',13,'add_imagenaddress'),(50,'Can change Imagen de Dirección',13,'change_imagenaddress'),(51,'Can delete Imagen de Dirección',13,'delete_imagenaddress'),(52,'Can view Imagen de Dirección',13,'view_imagenaddress'),(53,'Can add Imagen del Cliente',14,'add_imagencustomer'),(54,'Can change Imagen del Cliente',14,'change_imagencustomer'),(55,'Can delete Imagen del Cliente',14,'delete_imagencustomer'),(56,'Can view Imagen del Cliente',14,'view_imagencustomer'),(57,'Can add Imagen de Garantía',15,'add_imagenguarantee'),(58,'Can change Imagen de Garantía',15,'change_imagenguarantee'),(59,'Can delete Imagen de Garantía',15,'delete_imagenguarantee'),(60,'Can view Imagen de Garantía',15,'view_imagenguarantee'),(61,'Can add Otra Imagen',16,'add_imagenother'),(62,'Can change Otra Imagen',16,'change_imagenother'),(63,'Can delete Otra Imagen',16,'delete_imagenother'),(64,'Can view Otra Imagen',16,'view_imagenother'),(65,'Can add Dirección',17,'add_address'),(66,'Can change Dirección',17,'change_address'),(67,'Can delete Dirección',17,'delete_address'),(68,'Can view Dirección',17,'view_address'),(69,'Can add Departamento',18,'add_departamento'),(70,'Can change Departamento',18,'change_departamento'),(71,'Can delete Departamento',18,'delete_departamento'),(72,'Can view Departamento',18,'view_departamento'),(73,'Can add Municipio',19,'add_municiopio'),(74,'Can change Municipio',19,'change_municiopio'),(75,'Can delete Municipio',19,'delete_municiopio'),(76,'Can view Municipio',19,'view_municiopio'),(77,'Can add Otra Fuente de Ingreso',20,'add_othersourcesofincome'),(78,'Can change Otra Fuente de Ingreso',20,'change_othersourcesofincome'),(79,'Can delete Otra Fuente de Ingreso',20,'delete_othersourcesofincome'),(80,'Can view Otra Fuente de Ingreso',20,'view_othersourcesofincome'),(81,'Can add Referencia',21,'add_reference'),(82,'Can change Referencia',21,'change_reference'),(83,'Can delete Referencia',21,'delete_reference'),(84,'Can view Referencia',21,'view_reference'),(85,'Can add Información Laboral',22,'add_workinginformation'),(86,'Can change Información Laboral',22,'change_workinginformation'),(87,'Can delete Información Laboral',22,'delete_workinginformation'),(88,'Can view Información Laboral',22,'view_workinginformation'),(89,'Can add Plan de Inversión',23,'add_investmentplan'),(90,'Can change Plan de Inversión',23,'change_investmentplan'),(91,'Can delete Plan de Inversión',23,'delete_investmentplan'),(92,'Can view Plan de Inversión',23,'view_investmentplan'),(93,'Can add Documento',24,'add_document'),(94,'Can change Documento',24,'change_document'),(95,'Can delete Documento',24,'delete_document'),(96,'Can view Documento',24,'view_document'),(97,'Can add Documeto de Banco',25,'add_documentbank'),(98,'Can change Documeto de Banco',25,'change_documentbank'),(99,'Can delete Documeto de Banco',25,'delete_documentbank'),(100,'Can view Documeto de Banco',25,'view_documentbank'),(101,'Can add Documento de dirección',26,'add_documentaddress'),(102,'Can change Documento de dirección',26,'change_documentaddress'),(103,'Can delete Documento de dirección',26,'delete_documentaddress'),(104,'Can view Documento de dirección',26,'view_documentaddress'),(105,'Can add Documento de Cliente',27,'add_documentcustomer'),(106,'Can change Documento de Cliente',27,'change_documentcustomer'),(107,'Can delete Documento de Cliente',27,'delete_documentcustomer'),(108,'Can view Documento de Cliente',27,'view_documentcustomer'),(109,'Can add Documento de Garantía',28,'add_documentguarantee'),(110,'Can change Documento de Garantía',28,'change_documentguarantee'),(111,'Can delete Documento de Garantía',28,'delete_documentguarantee'),(112,'Can view Documento de Garantía',28,'view_documentguarantee'),(113,'Can add Otro Documento',29,'add_documentother'),(114,'Can change Otro Documento',29,'change_documentother'),(115,'Can delete Otro Documento',29,'delete_documentother'),(116,'Can view Otro Documento',29,'view_documentother'),(117,'Can add Banco',30,'add_banco'),(118,'Can change Banco',30,'change_banco'),(119,'Can delete Banco',30,'delete_banco'),(120,'Can view Banco',30,'view_banco'),(121,'Can add Credito',31,'add_credit'),(122,'Can change Credito',31,'change_credit'),(123,'Can delete Credito',31,'delete_credit'),(124,'Can view Credito',31,'view_credit'),(125,'Can add Cuota',32,'add_cuota'),(126,'Can change Cuota',32,'change_cuota'),(127,'Can delete Cuota',32,'delete_cuota'),(128,'Can view Cuota',32,'view_cuota'),(129,'Can add Desembolso',33,'add_disbursement'),(130,'Can change Desembolso',33,'change_disbursement'),(131,'Can delete Desembolso',33,'delete_disbursement'),(132,'Can view Desembolso',33,'view_disbursement'),(133,'Can add Garantia',34,'add_guarantees'),(134,'Can change Garantia',34,'change_guarantees'),(135,'Can delete Garantia',34,'delete_guarantees'),(136,'Can view Garantia',34,'view_guarantees'),(137,'Can add Detalle de Garantia',35,'add_detailsguarantees'),(138,'Can change Detalle de Garantia',35,'change_detailsguarantees'),(139,'Can delete Detalle de Garantia',35,'delete_detailsguarantees'),(140,'Can view Detalle de Garantia',35,'view_detailsguarantees'),(141,'Can add Pago',36,'add_payment'),(142,'Can change Pago',36,'change_payment'),(143,'Can delete Pago',36,'delete_payment'),(144,'Can view Pago',36,'view_payment'),(145,'Can add Plan de Pago',37,'add_paymentplan'),(146,'Can change Plan de Pago',37,'change_paymentplan'),(147,'Can delete Plan de Pago',37,'delete_paymentplan'),(148,'Can view Plan de Pago',37,'view_paymentplan'),(149,'Can add Estado de Cuenta',38,'add_accountstatement'),(150,'Can change Estado de Cuenta',38,'change_accountstatement'),(151,'Can delete Estado de Cuenta',38,'delete_accountstatement'),(152,'Can view Estado de Cuenta',38,'view_accountstatement'),(153,'Can add Recibo',39,'add_recibo'),(154,'Can change Recibo',39,'change_recibo'),(155,'Can delete Recibo',39,'delete_recibo'),(156,'Can view Recibo',39,'view_recibo'),(157,'Can add Factura',40,'add_invoice'),(158,'Can change Factura',40,'change_invoice'),(159,'Can delete Factura',40,'delete_invoice'),(160,'Can view Factura',40,'view_invoice'),(161,'Can add crontab',41,'add_crontabschedule'),(162,'Can change crontab',41,'change_crontabschedule'),(163,'Can delete crontab',41,'delete_crontabschedule'),(164,'Can view crontab',41,'view_crontabschedule'),(165,'Can add interval',42,'add_intervalschedule'),(166,'Can change interval',42,'change_intervalschedule'),(167,'Can delete interval',42,'delete_intervalschedule'),(168,'Can view interval',42,'view_intervalschedule'),(169,'Can add periodic task',43,'add_periodictask'),(170,'Can change periodic task',43,'change_periodictask'),(171,'Can delete periodic task',43,'delete_periodictask'),(172,'Can view periodic task',43,'view_periodictask'),(173,'Can add periodic task track',44,'add_periodictasks'),(174,'Can change periodic task track',44,'change_periodictasks'),(175,'Can delete periodic task track',44,'delete_periodictasks'),(176,'Can view periodic task track',44,'view_periodictasks'),(177,'Can add solar event',45,'add_solarschedule'),(178,'Can change solar event',45,'change_solarschedule'),(179,'Can delete solar event',45,'delete_solarschedule'),(180,'Can view solar event',45,'view_solarschedule'),(181,'Can add clocked',46,'add_clockedschedule'),(182,'Can change clocked',46,'change_clockedschedule'),(183,'Can delete clocked',46,'delete_clockedschedule'),(184,'Can view clocked',46,'view_clockedschedule'),(185,'Can add site',47,'add_site'),(186,'Can change site',47,'change_site'),(187,'Can delete site',47,'delete_site'),(188,'Can view site',47,'view_site');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `codes_code`
--

DROP TABLE IF EXISTS `codes_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `codes_code` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `number` varchar(5) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `codes_code_user_id_2f7a75e8_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codes_code`
--

LOCK TABLES `codes_code` WRITE;
/*!40000 ALTER TABLE `codes_code` DISABLE KEYS */;
INSERT INTO `codes_code` VALUES (1,'97855',3),(2,'10146',2),(3,'61789',1),(4,'58611',4);
/*!40000 ALTER TABLE `codes_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers_customer`
--

DROP TABLE IF EXISTS `customers_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers_customer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_code` varchar(25) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `type_identification` varchar(50) NOT NULL,
  `identification_number` varchar(15) NOT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `status` varchar(75) NOT NULL,
  `date_birth` date NOT NULL,
  `number_nit` varchar(20) NOT NULL,
  `place_birth` varchar(75) NOT NULL,
  `marital_status` varchar(50) NOT NULL,
  `profession_trade` varchar(75) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `nationality` varchar(75) NOT NULL,
  `person_type` varchar(50) NOT NULL,
  `description` longtext,
  `creation_date` datetime(6) NOT NULL,
  `asesor` varchar(100) DEFAULT NULL,
  `fehca_vencimiento_de_tipo_identificacion` date DEFAULT NULL,
  `user_id_id` bigint DEFAULT NULL,
  `immigration_status_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_code` (`customer_code`),
  UNIQUE KEY `identification_number` (`identification_number`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `number_nit` (`number_nit`),
  KEY `customers_customer_user_id_id_40a1eb2d_fk_users_user_id` (`user_id_id`),
  KEY `customers_customer_immigration_status_i_d0f4f60c_fk_customers` (`immigration_status_id_id`),
  CONSTRAINT `customers_customer_immigration_status_i_d0f4f60c_fk_customers` FOREIGN KEY (`immigration_status_id_id`) REFERENCES `customers_immigrationstatus` (`id`),
  CONSTRAINT `customers_customer_user_id_id_40a1eb2d_fk_users_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers_customer`
--

LOCK TABLES `customers_customer` WRITE;
/*!40000 ALTER TABLE `customers_customer` DISABLE KEYS */;
INSERT INTO `customers_customer` VALUES (5,'2024-1','Hugo Keyner','Quib Caal','DPI','3211364031601','42136958','keynerd07@gmail.com','Aprobado','2000-07-20','108043304','Coban','SOLTER@','Bachiller en Ciencias y Letras','MASCULINO','GUATEMALTECO','Individual (PI)','','2024-12-27 20:15:02.283000','Luis Macz','2028-11-28',1,3),(7,'2024-2','MILVIA MÓNICA NATALY','CHUB VENTURA','DPI','2058132831601','48933935','Milvianatalyventura@gmail.com','Aprobado','1991-07-09','7057398','COBAN','CASAD@','PERITO CONTADOR','FEMENINO','GUATEMALTECA','Individual (PI)','','2024-12-27 20:31:01.759000','LUIS MACZ','2034-01-23',4,3),(8,'2024-3','MARCO TULIO','MAX CAAL','DPI','2252552191601','49571210','angelsofimtmx15@gmail.com','Aprobado','1989-09-15','73468835','COBAN','SOLTER@','PERITO CONTADOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2024-12-27 21:10:15.244000','LUIS MACZ','2031-11-17',4,3),(9,'2024-4','YONATHAN FERNANDO','LEAL SAGUI','DPI','2846987681601','30205136','yonathanleals@gmail.com','Aprobado','1999-07-02','102785392','coban','SOLTER@','BACHILLER EN CIENCIAS Y LETRAS','MASCULINO','GUATEMALTECO','Individual (PI)','','2024-12-30 23:31:22.731000','GRECIA','2027-10-28',4,3),(10,'2025-1','ELMER GIOVANI','QUEZADA GARCÍA','DPI','2415299561601','46926053','elmerquezada@gmail.com','Aprobado','1986-03-23','37,989,855','COBAN','SOLTER@','LIC. EN PEDAGOGIA','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-02 22:21:57.111000','LUIS MACZ','2032-05-10',4,3),(11,'2025-2','JOSÉ DAVID','PÉREZ CHENAL','DPI','2538252531601','30980857','j.d.p.ch94@gmail.com','Aprobado','1994-09-08','84893036','COBAN','SOLTER@','Bachiller en Ciencias y Letras','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-02 22:48:35.627000','HILDA VARGAS','2027-09-29',4,3),(12,'2025-3','HARY DARÍO','HUN CAAL','DPI','2488582701601','45252543','harysd23@gmail.com','Aprobado','1991-01-06','79064973','COBAN','SOLTER@','BACHILLER EN TURISMO','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-02 23:04:25.838000','LUIS MACZ','2033-01-04',4,3),(13,'2025-4','MARIO RODOLFO','ICAL BOTZOC','DPI','2058730731601','46709559','Marioical221@gmail.com','Aprobado','1987-09-07','69256764','COBAN','CASAD@','PERITO CONTADOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-02 23:22:54.129000','LUIS MACZ','2033-10-23',4,3),(14,'2025-5','MARIA ALEJANDRA','YAT LÓPEZ','DPI','3301444131609','31131442','alejayat116@gmail.com','Aprobado','1999-11-20','10335056','SAN PEDRO CARCHA','SOLTER@','PERITO EN INFORMATICA','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-03 15:08:55.192000','LUIS MACZ','2028-01-12',4,3),(15,'2025-6','ABNER JOSUE','PAAU CAAL','DPI','3225173541601','48310001','JosueC12@gmail.com','Aprobado','2001-07-29','109035208','COBAN','SOLTER@','PERITO EN RECURSOS NATURALES','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 15:18:10.447000','LUIS MACZ','2030-10-22',4,3),(16,'2025-7','MARIA DEL CARMEN','CASTAÑEDA VALDIZON','DPI','1933409171601','58436843','mccvaldizon214@yahoo.es','Aprobado','1956-04-21','5383536','COBAN','CASAD@','PEDAGOGA','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-03 15:57:11.201000','MARIA DE LOS ANGELES BOTZOC','2030-01-12',4,3),(17,'2025-8','CÉSAR JOSUÉ','CAAL MORALES','DPI','3228672741601','33667872','cesarjosuecaalmorales123@gmail.com','Aprobado','1999-07-25','105537225','COBAN','SOLTER@','PERITO CONTADOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 16:25:01.312000','LUIS MACZ','2028-01-25',4,3),(18,'2025-9','CESAR AGUSTIN','ASIG SAQUIL','DPI','2093606151615','31267157','asigcesar261@gmail.com','Aprobado','1991-10-16','73056944','FRAY BARTOLOME DE LAS CASAS','SOLTER@','PERITO CONTADOR','MASCULINO','GAUTEMALTECO','Individual (PI)','','2025-01-03 17:39:43.755000','LUIS MACZ','2027-01-01',4,3),(19,'2025-10','AURIO FROILAN','CABNAL CUCUL','DPI','2332661941710','49050037','aufroilano@gmail.com','Aprobado','1988-06-14','71052119','COBAN','CASAD@','PERITO CONTADOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 17:56:55.816000','LUIS MACZ','2032-10-05',4,3),(20,'2025-11','ROLANDO','VARGAS SIANA','DPI','1648695731601','47182315','rbs-@hotmail.com','Aprobado','1986-05-24','51481944','COBAN','CASAD@','DEPENDIENTE DE MOSTRADOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 18:16:20.812000','JESSICA TZUL','2030-10-15',4,3),(21,'2025-12','VIVIANA PRISCILA','AYALA TELLO','DPI','2654195061601','49711888','Prisciayala@hotmail.com','Aprobado','1972-12-02','47346965','COBAN','SOLTER@','COMERCIANTE','FEMENINO','GUATEMALTECO','Individual (PI)','','2025-01-03 18:36:06.525000','FLOR DE MARIA IGLESIAS PERDOMO','2023-01-27',4,3),(23,'2025-13','HERBERT ROLANDO','TAROT CASTRO','DPI','2652613681601','55634365','CHICHODJ@HOTMAIL.COM','Aprobado','1968-09-10','7656556','COBAN','CASAD@','COMERCIANTE','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 18:53:56.655000','BERNARDA AYALA','2030-10-14',4,3),(24,'2025-14','JORGE MARIO','CHUN','DPI','1916501961601','51779184','jorgemariochun@gmail.com','Aprobado','1982-12-04','19056737','DESCONOCIDO','CASAD@','GESTOR DE CREDITOS/ COMERCIANTE','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 18:58:06.191000','VICTORIA CAAL','2027-12-06',2,3),(25,'2025-15','JUAN CARLOS','MALDONADO CEL','DPI','2592188121018','30637619','pastorjuancarlos72@gmail.com','Aprobado','1972-12-11','52663930','COBAN','CASAD@','COMERCIANTE','MASCULINO','GAUTEMALTECO','Individual (PI)','','2025-01-03 19:04:14.848000','LUIS MACZ','2032-12-06',4,3),(28,'2025-16','CLAUDIA LETICIA','LÓPEZ RAMIREZ','DPI','2592189871601','39208802','claudialopez@gamil.com','Aprobado','1971-08-26','49072013','COBAN','CASAD@','COMERCIANTE','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-03 19:22:56.584000','LUIS MACZ','2033-03-06',4,3),(29,'2025-17','SERGIO ALEXANDER','CAAL CAL','DPI','2569638781607','30102636','alexanderac-dc@hotmail.com','Aprobado','1994-03-25','80885047','SAN CRISTOBAL','CASAD@','BACHILLER EN CIENCIAS Y LETRAS','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 19:25:16.866000','LUIS MACZ','2033-01-05',2,3),(30,'2025-18','CARLOS BENJAMIN','ARCHILA CHINCHILLA','DPI','1968238111609','53700472','carlosbenjachinchilla@gamil.com','Aprobado','1982-01-22','19121989','COBAN','SOLTER@','PERITO CONTADOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 19:34:57.473000','LUIS MACZ','2029-10-03',4,3),(31,'2025-19','GLENDA NATALY','DE LA CRUZ TZALAM','DPI','2618480111601','39407253','dglenda721@gmail.com','Aprobado','1986-02-06','37989502','COBAN ALTA VERAPAZ','SOLTER@','PERITO CONTADOR','MASCULINO','GUATEMALTECA','Individual (PI)','','2025-01-03 19:50:21.551000','LUIS MACZ','2028-08-09',2,3),(32,'2025-20','MARCO ANTONIO','SUN PACAY','DPI','2667938861601','42313425','sunpacaym@gamil.com','Aprobado','1994-06-11','103845011','COBAN','SOLTER@','BACHILLER EN CIENCIAS Y LETRAS','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 19:52:39.008000','LUIS MACZ','2031-09-02',4,3),(33,'2025-21','SUANY ELIZABETH','QUIB CAÁL DE POP','DPI','2600092101601','35968506','quibsuany@gmail.com','Aprobado','1990-10-12','61715654','COBAN','SOLTER@','SECRETARIA Y OFICINISTA','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 20:03:20.588000','LUIS MACZ','2033-01-05',4,3),(34,'2025-22','MARIA FERNANDA','CASASOLA TZOY','DPI','3259398451601','33690420','fernandacasasola84@gmail.com','Aprobado','2002-01-18','108931560','COBAN ALTA VERAPAZ','SOLTER@','PERITO CONTADOR','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-03 20:07:46.866000','LUIS MACZ','2030-04-29',2,3),(35,'2025-23','DEYLER HUMBERTO ABIMAEL','CACAO QUEJ','DPI','2755971481604','33229931','deylercacao11@gmail.com','Aprobado','1997-02-11','98955195','TACTIC','SOLTER@','ESTUDIANTE','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 20:22:59.042000','ANGEL ROMAN','2025-02-26',4,3),(36,'2025-24','NANCY BEATRIZ','VALDEZ ALVA DE RAMOS','DPI','1733045831603','41805123','Beavaldez@gmail.com','Aprobado','1991-03-07','67722776','SAN CRISTOBAL ALTA VERAPAZ','CASAD@','COMERCIANTE','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-03 20:47:23.474000','SONIA MORAN','2032-11-02',2,3),(37,'2025-25','BRITANY NAYELI','CIFUENTES CHOCOOJ','DPI','3213619971601','59758559','britanycifuentes@gmail.com','Aprobado','2001-02-16','108008150','COBAN','SOLTER@','SECRETARIA','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-03 21:03:52.074000','KRIZZLEY ALVARADO','2029-03-06',4,3),(38,'2025-26','BELSAZAR NATANAEL','VILLATORO GAMARRO','DPI','2520776551601','34347900','Belsazarvg1994@gmail.com','Aprobado','1994-09-12','86790617','COBAN ALTA VERAPAZ','CASAD@','PERITO EN ADMINISTRACION DE EMPRESAS','MASCULINO','GUATEMALTECA','Individual (PI)','','2025-01-03 21:04:41.538000','LUIS MACZ','2030-03-07',2,3),(40,'2025-27','RONY ADALBERTO','RAMOS RODRIGUEZ','DPI','2399458322215','59410667','ronyramos910@gmail.com','Aprobado','1987-12-20','58016619','SAN CRISTOBAL VERAPAZ','CASAD@','SUBINSPECTOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 21:31:37.930000','WILFREDO CIFUENTES','2026-06-14',2,3),(41,'2025-28','JORGE  BENEDICTO','LUCAS  PENSAMIENTO','DPI','2623602920101','57384627','jlucaspensamiento@gmail.com','Aprobado','1980-04-13','14067161','COBAN','CASAD@','AGRONOMO','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 21:36:45.529000','GRECIA RODRIGUEZ','2033-06-26',4,3),(42,'2025-29','MAYRA LUCRECIA','SIERRA','DPI','2441858161601','46817463','mayrasierra005@gmail.com','Aprobado','1984-08-05','29212596','DESCONOCIDO','SOLTER@','COMERCIANTE','MASCULINO','GUATEMALTECA','Individual (PI)','','2025-01-03 21:53:05.911000','JORGE MARIO CHUN','2028-01-30',2,3),(43,'2025-30','CESAR RATZEL YUBINI','BARRAZA SALAMA','DPI','2643490160301','42532182','Dugabarra2203@hotmail.com','Aprobado','1983-03-11','30321727','COBAN','CASAD@','ENTRENADOR DE FUTBOLL','MASCULINO','GUATEMALTECA','Individual (PI)','','2025-01-03 21:55:07.614000','WALTER CAAL','2029-08-01',4,3),(44,'2025-31','BILLY ROMAN','PONCE PINELO','DPI','1747223461601','37157511','billyponce99@gmail.com','Aprobado','1973-07-30','21117969','SAN PEDRO CARCHA','CASAD@','PLANIFICADOR Y DIGITADOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 22:16:04.856000','MARIA FERNANDA REYES','2031-08-01',2,3),(46,'2025-32','ALLAN ESTUARDO','CACAO','DPI','2329904251601','37697998','cacaoe979@gmail.com','Aprobado','1993-11-05','83915540','COBAN ALTA VERAPAZ','CASAD@','PERITO CONTADOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 22:53:34.333000','ALEJANDRA RAYMUNDO','2032-01-18',2,3),(47,'2025-33','CARLOS HUMBERTO DE JESUS','REYES GUTIERREZ','DPI','1830892511609','46418726','careygut@gamil.com','Aprobado','1950-12-25','1622951','SAN PEDRO CARCHA ALTA VERAPAZ','CASAD@','MAESTRO JUBILADO','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-03 23:48:25.725000','MARTHA REYES','2032-01-28',2,3),(49,'2025-34','ABNER BENJAMIN','OJOM CASTRO','DPI','2597867641615','24173952','abnerojom@gmail.com','Aprobado','1989-09-29','54505313','FRAY BARTOLOME DE LAS CASAS','SOLTER@','PERITO EN ADMINISTRACION DE EMPRESAS','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-04 00:14:00.895000','LUIS MACZ','2031-09-13',2,3),(50,'2025-35','VILMA ARACELY','GONZALES QUIM','DPI','2372735351601','40962743','gonzalesvilma854@gmail.com','Aprobado','1973-01-20','31157920','coban','CASAD@','TUTORA','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-04 00:26:59.720000','ARMANDO ALVARADO','2032-02-10',4,3),(51,'2025-36','GERSON ALFREDO','LEAL XE','DPI','1818961761601','59812012','gersonleal5@gmail.com','Aprobado','1976-03-08','25802976','COBAN','CASAD@','Bachiller en ciencias y letra','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-06 16:28:38.874000','ARMANDO','2023-01-15',4,3),(52,'2025-37','AXA ROXANA  MADAI','CHUB CAZ','DPI','2315704571601','31220906','roux18madi@gmail.com','Aprobado','1993-06-25','78013798','COBAN','SOLTER@','MAESTRA DE EDUCACION PRIMARIA','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-06 16:52:47.269000','ARMANDO ALVARADO','2023-03-31',4,3),(53,'2025-38','YOSELIN TAMARA','LEAL ARRIOLA','DPI','2422301481601','51619427','tamylealarriola@gmail.com','Aprobado','1993-02-14','80374697','COBAN','SOLTER@','ENCARGADA DE TIENDA/ ESTUDIANTE DE 3r AÑO DE DERECHO','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-06 17:07:15.165000','LUIS MACZ','2033-08-02',4,3),(54,'2025-39','VILMA JECENIA','TZUB GARCÍA DE PORTILLO','DPI','1816129841613','50418141','DEPORTILLOVILMA1216@GMAIL.COM','Aprobado','1990-08-16','53169727','FRAY BARTOLOME DE LAS CASAS','CASAD@','SECRETARIA BILINGUE','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-06 17:20:29.091000','LUIS MACZ','2025-05-20',4,3),(55,'2025-40','MILDRED ZULEYMA CARMELINA','JUÁREZ CATALÁN','DPI','2739481801601','55104517','milicatalan1107@gmail.com','Aprobado','1995-01-28','85557846','COBAN','SOLTER@','SECRETARIA Y OFICINISTA','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-06 17:43:22.226000','LUIS MACZ','2028-02-14',4,3),(56,'2025-41','ESTUARDO OTTONIEL','RAMIREZ PINZÓN','DPI','1658921370406','49017566','esttoniel@gmail.com','Aprobado','1983-07-11','20245807','COBAN','CASAD@','BACHILLER EN CIENCIAS Y LETRAS','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-06 18:01:56.455000','LUIS MACZ','2031-06-10',4,3),(57,'2025-42','ANGEL HUMBERTO','CU POOU','DPI','3245194271601','45218175','angelhcu-98@hotmail.com','Aprobado','1998-05-15','97080349','COBAN','SOLTER@','ENFERMERO','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-06 18:49:08.583000','LUIS MACZ','2029-08-26',4,3),(58,'2025-43','RONALD ARIALDO','POP CORONADO','DPI','2556123621601','30883842','arialdocoronado@gmail.com','Aprobado','1983-11-22','36111554','COBAN','SOLTER@','PERITO EN ADMINISTRACION DE EMPRESAS','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-06 19:05:37.303000','LUIS MACZ','2032-01-04',4,3),(59,'2025-44','ENGELVERTH  ALEXANDER','COY  CAAL','DPI','2195058611608','51119622','engelverth1228@gmail.com','Aprobado','1992-12-28','86457128','COBAN','CASAD@','PILOTO','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-06 20:31:12.953000','AXA CHUB','2033-01-05',4,3),(60,'2025-45','HEIDY LOURDES','TZUL CATUN DE COY','DPI','1659867191601','42009341','heitzuca83@gmail.com','Aprobado','1983-09-27','25764314','COBAN','CASAD@','TECNICO EN INVESTIGACION CRIMINAL Y FORENSE','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-06 21:07:48.866000','ENGELVERTH ALEXANDER COY CAAL','2032-07-13',4,3),(61,'2025-46','FREDY ELIESMO','CHOC PRADO','DPI','2059118891601','38290044','pradofredy366@gmail.com','Aprobado','1991-08-12','76335453','COBAN','SOLTER@','SEGURIDAD','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-06 21:25:02.490000','AURELIO QUEJ','2031-03-01',4,3),(62,'2025-47','EDUARDO','PUTUL CHUB','DPI','2465283891609','44923656','eduardoputulputulchub@gmail.com','Aprobado','1989-04-09','53152433','SAN PEDRO CARCHA','SOLTER@','PROFESOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-06 21:50:16.019000','ARMANDO ALVARADO','2027-06-16',4,3),(63,'2025-48','JONATHAN RONALDO','ASIG MAAS','DPI','2803862731601','51670114','jonatmaas@gmail.com','Aprobado','2000-10-06','104913369','COBAN','SOLTER@','MAESTRO INFANTIL','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-06 22:17:57.912000','LUIS MACZ','2028-11-20',4,3),(65,'2025-49','HEDDER EMILIO','CAAL BOL','DPI','2227265981601','40689250','heddka9@gmail.com','Aprobado','1986-06-14','42026008','COBAN','CASAD@','PERITO CONTADOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-07 16:05:47.077000','LUIS MACZ','2027-05-14',4,3),(66,'2025-50','JOSÉ ALEJANDRO','ACABAL DÍAZ','DPI','1993877611601','44906687','16acabaljose@gmail.com','Aprobado','1986-07-16','42026938','COBAN','CASAD@','PERITO CONTADOR','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-07 16:58:40.768000','LUIS MACZ','2031-05-13',4,3),(67,'2025-51','BRENDA LETICIA','AC CHEN','DPI','2662837131601','33165058','aclety88@gmail.com','Aprobado','1988-11-30','70022283','SAN PEDRO CARCHA','SOLTER@','ESTILISTA','MASCULINO','GUATEMALTECA','Individual (PI)','','2025-01-07 17:35:21.600000','ANA MARÍA BUENAFÉ','2023-02-04',4,3),(68,'2025-52','JOSE ESTUARDO','CAN','DPI','2605708691501','59083307','canj62324@gmail.com','Aprobado','1981-10-12','19023235','SALAMA','SOLTER@','SACERDOTE','MASCULINO','GUATEMALTECO','Individual (PI)','Domicilio alterno. 2 calle 9-35 zona 2','2025-01-07 17:56:50.346000','MARIO CHEN','2033-01-03',4,3),(69,'2025-53','ANGEL RENÉ ABINADÍ','CAAL COY','DPI','3210982851601','53722065','Abinadicaal@gmail.com','Aprobado','2001-12-28','110238583','COBAN','SOLTER@','COACH- SERVICIO AL CLIENTE','MASCULINO','GUATEMALA','Individual (PI)','','2025-01-07 18:12:19.721000','LUIS MACZ','2030-06-04',4,3),(70,'2025-54','BRANDON RODOLFO','MÉNDEZ','DPI','3222748691601','42553591','Brandonmendez04@gmail.com','Aprobado','2004-06-14','322274869','COBAN','SOLTER@','CAJERO SERVICIO AL CLIENTE','MASCULINO','GUATEMALTECA','Individual (PI)','','2025-01-07 18:24:24.270000','LUIS MACZ','2032-10-14',4,3),(71,'2025-55','DANNIA YASMIRA','LEAL ROSALES','DPI','2092012151606','59900703','dannialr1991@gmail.com','Aprobado','1991-10-12','73093467','COBAN','SOLTER@','MAESTRA DE EDUCACIÓN PREPRIMARIA','FEMENINO','GUATEMALTECO','Individual (PI)','','2025-01-07 18:40:46.953000','HILDA VARGAS','2031-10-24',4,1),(72,'2025-56','JACKELINE ELIZABETH','VÁSQUEZ GODOY','DPI','1840158201604','40258158','vasquezgodoyjacky@gmail.com','Aprobado','1978-03-12','14083760','COBAN','SOLTER@','MAESTRA DE EDUCACION PRIMARIA RURAL','MASCULINO','GUATEMALTECA','Individual (PI)','','2025-01-07 19:02:10.977000','LUIS MACZ','2030-02-20',4,3),(73,'2025-57','LUIS FERNANDO','CAAL','DPI','2261104941601','57714570','lfernando2181@gmail.com','Aprobado','1981-04-21','41816358','COBAN','SOLTER@','PERITO CONTADOR','MASCULINO','GUATEMALA','Individual (PI)','','2025-01-07 20:23:39.530000','LUIS MACZ','2031-11-14',4,3),(74,'2025-58','BLANCA LISSETH','QUEVEDO YAT','DPI','2648349251601','45558610','Blanca1983quevedo@gmail.com','Aprobado','1983-11-02','29212618','COBAN','SOLTER@','ENFERMERA','MASCULINO','GUATEMALTECA','Individual (PI)','','2025-01-07 20:37:15.085000','WILMMER POP SANCHEZ','2027-12-15',4,3),(75,'2025-59','GUILLERMO FRANCISCO','TIUL ASIG','DPI','2201359241601','57419047','Guillermotiulasig@gmail.com','Aprobado','1986-11-25','37993283','COBAN','CASAD@','PILOTO DE REPARTO','MASCULINO','GUATEMALO','Individual (PI)','','2025-01-07 20:51:51.458000','LUIS MACZ','2028-03-23',4,3),(76,'2025-60','FILIBERTO','CAAL XEP','DPI','2595461191601','2319005','filip1308@gmail.com','Aprobado','1985-08-21','51940981','COBAN','CASAD@','BACHILLER EN CIENCIAS Y LETRAS','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-07 21:11:17.160000','LUIS MACZ','2027-05-17',4,3),(77,'2025-61','MARVIN JOSÉ','COY CÚ','DPI','3215371061601','56394582','jcoy00282@gmail.com','Aprobado','1998-05-21','107410192','COBAN','SOLTER@','PERITO CONTADOR','MASCULINO','GUATEMALTECA','Individual (PI)','','2025-01-07 21:39:03.345000','LUIS MACZ','2028-10-30',4,3),(78,'2025-62','YURI ROCAEL','FERNÁNDEZ GONZALES','DPI','2680517391601','35911407','rocafer.gonzales@gmail.com','Aprobado','1984-09-20','25582097','COBAN','SOLTER@','GESTOR DE COBROS','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-07 21:56:07.570000','NATHALY CAAL','2023-04-29',4,3),(79,'2025-63','AUGUSTÍN','GARCÍA SIS','DPI','2531567771601','55436313','Agroforestexport@gmail.com','Aprobado','1988-09-02','48687480','COBAN','CASAD@','INGENIERO FORESTAL','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-07 22:10:38.616000','LUIS MACZ','2027-06-22',4,3),(81,'2025-64','LUIS DAVID','CHEN CHAJ','DPI','1951173521601','52083446','luisdavidchen7@gmail.com','Aprobado','1987-11-25','53139674','COBAN','SOLTER@','MAESTRO DE EDUCACIÓN PRIMARIA URBANA','MASCULINO','GUATEMALTECO','Individual (PI)','','2025-01-07 22:50:00.931000','LUIS MACZ','2034-01-25',4,3),(82,'2025-65','RODY LILIANA','LAJ LEAL','DPI','3251046541601','31986694','rodylaj@gmail.com','Aprobado','1996-08-23','92408672','COBAN','SOLTER@','RASTREADORA','FEMENINO','GUATEMALTECA','Individual (PI)','','2025-01-08 14:42:46.577000','LORENA GUAY','2025-06-15',4,3);
/*!40000 ALTER TABLE `customers_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers_immigrationstatus`
--

DROP TABLE IF EXISTS `customers_immigrationstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers_immigrationstatus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `condition_name` varchar(50) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `condition_name` (`condition_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers_immigrationstatus`
--

LOCK TABLES `customers_immigrationstatus` WRITE;
/*!40000 ALTER TABLE `customers_immigrationstatus` DISABLE KEYS */;
INSERT INTO `customers_immigrationstatus` VALUES (1,'Residente temporal',''),(2,'Turista o visitante',NULL),(3,'Residente permanente',NULL),(4,'Permiso de trabajo',NULL),(5,'Persona en trnsito',NULL),(6,'Permiso consular o similar',NULL),(7,'Otra',NULL);
/*!40000 ALTER TABLE `customers_immigrationstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_clockedschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_clockedschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_clockedschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `clocked_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_clockedschedule`
--

LOCK TABLES `django_celery_beat_clockedschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_clockedschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_clockedschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_crontabschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_crontabschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) NOT NULL,
  `hour` varchar(96) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(124) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  `timezone` varchar(63) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_crontabschedule`
--

LOCK TABLES `django_celery_beat_crontabschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_intervalschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_intervalschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `every` int NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_intervalschedule`
--

LOCK TABLES `django_celery_beat_intervalschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictask`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_periodictask` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `crontab_id` int DEFAULT NULL,
  `interval_id` int DEFAULT NULL,
  `solar_id` int DEFAULT NULL,
  `one_off` tinyint(1) NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `priority` int unsigned DEFAULT NULL,
  `headers` longtext NOT NULL DEFAULT (_utf8mb3'{}'),
  `clocked_id` int DEFAULT NULL,
  `expire_seconds` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` (`crontab_id`),
  KEY `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` (`interval_id`),
  KEY `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` (`solar_id`),
  KEY `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` (`clocked_id`),
  CONSTRAINT `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` FOREIGN KEY (`clocked_id`) REFERENCES `django_celery_beat_clockedschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` FOREIGN KEY (`solar_id`) REFERENCES `django_celery_beat_solarschedule` (`id`),
  CONSTRAINT `django_celery_beat_periodictask_chk_1` CHECK ((`total_run_count` >= 0)),
  CONSTRAINT `django_celery_beat_periodictask_chk_2` CHECK ((`priority` >= 0)),
  CONSTRAINT `django_celery_beat_periodictask_chk_3` CHECK ((`expire_seconds` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictask`
--

LOCK TABLES `django_celery_beat_periodictask` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictask` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictasks`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_periodictasks` (
  `ident` smallint NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictasks`
--

LOCK TABLES `django_celery_beat_periodictasks` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_solarschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_solarschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_celery_beat_solarschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event` varchar(24) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq` (`event`,`latitude`,`longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_solarschedule`
--

LOCK TABLES `django_celery_beat_solarschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (17,'addresses','address'),(18,'addresses','departamento'),(19,'addresses','municiopio'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(11,'codes','code'),(4,'contenttypes','contenttype'),(7,'customers','customer'),(8,'customers','immigrationstatus'),(46,'django_celery_beat','clockedschedule'),(41,'django_celery_beat','crontabschedule'),(42,'django_celery_beat','intervalschedule'),(43,'django_celery_beat','periodictask'),(44,'django_celery_beat','periodictasks'),(45,'django_celery_beat','solarschedule'),(24,'documents','document'),(26,'documents','documentaddress'),(25,'documents','documentbank'),(27,'documents','documentcustomer'),(28,'documents','documentguarantee'),(29,'documents','documentother'),(20,'FinancialInformation','othersourcesofincome'),(21,'FinancialInformation','reference'),(22,'FinancialInformation','workinginformation'),(38,'financings','accountstatement'),(30,'financings','banco'),(31,'financings','credit'),(32,'financings','cuota'),(35,'financings','detailsguarantees'),(33,'financings','disbursement'),(34,'financings','guarantees'),(40,'financings','invoice'),(36,'financings','payment'),(37,'financings','paymentplan'),(39,'financings','recibo'),(23,'InvestmentPlan','investmentplan'),(12,'pictures','imagen'),(13,'pictures','imagenaddress'),(14,'pictures','imagencustomer'),(15,'pictures','imagenguarantee'),(16,'pictures','imagenother'),(9,'roles','role'),(10,'roles','userrole'),(5,'sessions','session'),(47,'sites','site'),(6,'users','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'customers','0001_initial','2025-01-09 22:30:19.031721'),(2,'FinancialInformation','0001_initial','2025-01-09 22:30:19.108236'),(3,'FinancialInformation','0002_initial','2025-01-09 22:30:19.287332'),(4,'InvestmentPlan','0001_initial','2025-01-09 22:30:19.317773'),(5,'InvestmentPlan','0002_initial','2025-01-09 22:30:19.379218'),(6,'addresses','0001_initial','2025-01-09 22:30:19.447026'),(7,'addresses','0002_initial','2025-01-09 22:30:19.562529'),(8,'contenttypes','0001_initial','2025-01-09 22:30:19.602170'),(9,'contenttypes','0002_remove_content_type_name','2025-01-09 22:30:19.662151'),(10,'auth','0001_initial','2025-01-09 22:30:19.925865'),(11,'auth','0002_alter_permission_name_max_length','2025-01-09 22:30:19.993941'),(12,'auth','0003_alter_user_email_max_length','2025-01-09 22:30:20.000657'),(13,'auth','0004_alter_user_username_opts','2025-01-09 22:30:20.007355'),(14,'auth','0005_alter_user_last_login_null','2025-01-09 22:30:20.016101'),(15,'auth','0006_require_contenttypes_0002','2025-01-09 22:30:20.021423'),(16,'auth','0007_alter_validators_add_error_messages','2025-01-09 22:30:20.030727'),(17,'auth','0008_alter_user_username_max_length','2025-01-09 22:30:20.038195'),(18,'auth','0009_alter_user_last_name_max_length','2025-01-09 22:30:20.045969'),(19,'auth','0010_alter_group_name_max_length','2025-01-09 22:30:20.060707'),(20,'auth','0011_update_proxy_permissions','2025-01-09 22:30:20.074649'),(21,'auth','0012_alter_user_first_name_max_length','2025-01-09 22:30:20.083304'),(22,'users','0001_initial','2025-01-09 22:30:20.382641'),(23,'admin','0001_initial','2025-01-09 22:30:20.528385'),(24,'admin','0002_logentry_remove_auto_add','2025-01-09 22:30:20.538935'),(25,'admin','0003_logentry_add_action_flag_choices','2025-01-09 22:30:20.549545'),(26,'codes','0001_initial','2025-01-09 22:30:20.571549'),(27,'codes','0002_initial','2025-01-09 22:30:20.625458'),(28,'customers','0002_initial','2025-01-09 22:30:20.802097'),(29,'django_celery_beat','0001_initial','2025-01-09 22:30:21.005992'),(30,'django_celery_beat','0002_auto_20161118_0346','2025-01-09 22:30:21.101331'),(31,'django_celery_beat','0003_auto_20161209_0049','2025-01-09 22:30:21.127677'),(32,'django_celery_beat','0004_auto_20170221_0000','2025-01-09 22:30:21.134324'),(33,'django_celery_beat','0005_add_solarschedule_events_choices','2025-01-09 22:30:21.140264'),(34,'django_celery_beat','0006_auto_20180322_0932','2025-01-09 22:30:21.232914'),(35,'django_celery_beat','0007_auto_20180521_0826','2025-01-09 22:30:21.297749'),(36,'django_celery_beat','0008_auto_20180914_1922','2025-01-09 22:30:21.337598'),(37,'django_celery_beat','0006_auto_20180210_1226','2025-01-09 22:30:21.365355'),(38,'django_celery_beat','0006_periodictask_priority','2025-01-09 22:30:21.449659'),(39,'django_celery_beat','0009_periodictask_headers','2025-01-09 22:30:21.538999'),(40,'django_celery_beat','0010_auto_20190429_0326','2025-01-09 22:30:21.746466'),(41,'django_celery_beat','0011_auto_20190508_0153','2025-01-09 22:30:21.856108'),(42,'django_celery_beat','0012_periodictask_expire_seconds','2025-01-09 22:30:21.940451'),(43,'django_celery_beat','0013_auto_20200609_0727','2025-01-09 22:30:21.960711'),(44,'django_celery_beat','0014_remove_clockedschedule_enabled','2025-01-09 22:30:21.980456'),(45,'django_celery_beat','0015_edit_solarschedule_events_choices','2025-01-09 22:30:21.988728'),(46,'django_celery_beat','0016_alter_crontabschedule_timezone','2025-01-09 22:30:22.004798'),(47,'django_celery_beat','0017_alter_crontabschedule_month_of_year','2025-01-09 22:30:22.018862'),(48,'django_celery_beat','0018_improve_crontab_helptext','2025-01-09 22:30:22.030657'),(49,'django_celery_beat','0019_alter_periodictasks_options','2025-01-09 22:30:22.035762'),(50,'financings','0001_initial','2025-01-09 22:30:23.361285'),(51,'documents','0001_initial','2025-01-09 22:30:24.224745'),(52,'pictures','0001_initial','2025-01-09 22:30:24.962756'),(53,'roles','0001_initial','2025-01-09 22:30:25.247460'),(54,'roles','0002_initial','2025-01-09 22:30:25.335580'),(55,'sessions','0001_initial','2025-01-09 22:30:25.377005'),(56,'sites','0001_initial','2025-01-09 22:30:25.401209'),(57,'sites','0002_alter_domain_unique','2025-01-09 22:30:25.422588');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents_document`
--

DROP TABLE IF EXISTS `documents_document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents_document` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` longtext,
  `document` varchar(100) DEFAULT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents_document`
--

LOCK TABLES `documents_document` WRITE;
/*!40000 ALTER TABLE `documents_document` DISABLE KEYS */;
INSERT INTO `documents_document` VALUES (1,'FACTURA DE LUZ','documents/factura_3.pdf','2024-12-27 20:40:19.306000'),(2,'FACTURA DE LUZ','documents/factura_4.pdf','2024-12-27 21:16:20.785000'),(3,'FACTURA DE LUZ','documents/factura_6.pdf','2025-01-02 22:54:24.934000'),(4,'FACTURA DE LUZ','documents/factura_7.pdf','2025-01-02 23:11:20.177000'),(5,'FACTURA DE LUZ','documents/factura_8.pdf','2025-01-02 23:29:35.406000'),(6,'FACTURA DE LUZ','documents/factura_9.pdf','2025-01-03 15:26:04.254000'),(7,'FACTURA DE LUZ','documents/factura_9_sL32Dex.pdf','2025-01-03 15:27:54.156000'),(8,'FACTURA DE LUZ','documents/factura_10.pdf','2025-01-03 16:30:22.933000'),(9,'FACTURA DE LUZ','documents/factura_11.pdf','2025-01-03 17:42:05.616000'),(10,'FACTURA DE LUZ','documents/factura_12.pdf','2025-01-03 18:03:09.385000'),(11,'FACTURA DE LUZ','documents/factura_13.pdf','2025-01-03 18:20:12.704000'),(12,'DPI','documents/factura_14.pdf','2025-01-03 18:44:42.187000'),(13,'FACTURA DE LUZ','documents/factura_14_LYjg6IM.pdf','2025-01-03 18:54:36.073000'),(14,'FACTURA DE LUZ','documents/factura_15.pdf','2025-01-03 19:09:30.088000'),(15,'FACTURA DE LUZ','documents/factura_16.pdf','2025-01-03 19:25:05.637000'),(16,'FACTURA DE LUZ','documents/factura_4_uuCWwuL.pdf','2025-01-03 19:28:00.333000'),(17,'FACTURA DE LUZ','documents/factura_5.pdf','2025-01-03 19:31:35.744000'),(18,'FACTURA DE LUZ','documents/factura_6_NHGpkxc.pdf','2025-01-03 19:52:45.841000'),(19,'FACTURA DE LUZ','documents/factura_17.pdf','2025-01-03 19:55:23.807000'),(20,'FACTURA DE LUZ','documents/factura_18.pdf','2025-01-03 20:06:57.665000'),(21,'FACTURA DE LUZ','documents/factura_8_qE1vsJA.pdf','2025-01-03 20:10:40.912000'),(22,'FACTURA DE LUZ','documents/DEYLER.pdf','2025-01-03 20:26:22.224000'),(24,'FACTURA DE LUZ','documents/factura_9_k5260fO.pdf','2025-01-03 20:48:26.509000'),(25,'FACTURA DE LUZ','documents/factura_11_v0YHyUZ.pdf','2025-01-03 21:06:44.898000'),(26,'FACTURA DE LUZ','documents/factura_19.pdf','2025-01-03 21:07:47.329000'),(27,'FACTURA DE LUZ','documents/factura_9_qZoRaD5.pdf','2025-01-03 21:33:18.076000'),(28,'FACTURA DE LUZ','documents/factura_20.pdf','2025-01-03 21:37:22.835000'),(29,'FACTURA DE LUZ','documents/factura_4_lWwtfmh.pdf','2025-01-03 21:55:40.667000'),(30,'FACTURA DE LUZ','documents/factura_12_3IwOXZv.pdf','2025-01-03 22:19:28.276000'),(31,'FACTURA DE LUZ','documents/factura_13_0igwTix.pdf','2025-01-03 23:52:14.319000'),(32,'FACTURA DE LUZ','documents/factura_21.pdf','2025-01-04 00:27:45.775000'),(33,'FACTURA DE LUZ','documents/factura_22.pdf','2025-01-04 00:41:56.264000'),(34,'FACTURA DE LUZ','documents/factura_23.pdf','2025-01-04 00:48:27.573000'),(35,'FACTURA DE LUZ','documents/factura_24.pdf','2025-01-06 16:31:43.048000'),(36,'FACTURA DE LUZ','documents/factura_25.pdf','2025-01-06 17:11:32.752000'),(37,'FACTURA DE LUZ','documents/factura_26.pdf','2025-01-06 17:24:15.570000'),(38,'FACTURA DE LUZ','documents/factura_27.pdf','2025-01-06 17:52:12.236000'),(39,'FACTURA DE LUZ','documents/factura_28.pdf','2025-01-06 18:05:28.253000'),(40,'FACTURA DE LUZ','documents/factura_30.pdf','2025-01-06 18:52:11.507000'),(41,'FACTURA DE LUZ','documents/factura_31.pdf','2025-01-06 19:09:14.814000'),(42,'FACTURA DE LUZ','documents/factura_32.pdf','2025-01-06 21:52:51.120000'),(43,'FACTURA DE LUZ','documents/factura_33.pdf','2025-01-06 22:20:13.384000'),(44,'FACTURA DE LUZ','documents/factura_34.pdf','2025-01-07 16:07:43.030000'),(45,'FACTURA DE LUZ','documents/factura_35.pdf','2025-01-07 17:01:45.338000'),(46,'FACTURA DE LUZ','documents/factura_36.pdf','2025-01-07 17:59:15.469000'),(47,'FACTURA DE LUZ','documents/factura_37.pdf','2025-01-07 18:16:37.587000'),(48,'FACTURA DE LUZ','documents/factura_38.pdf','2025-01-07 18:44:06.191000'),(49,'FACTURA DE LUZ','documents/factura_39.pdf','2025-01-07 19:04:15.435000'),(50,'FACTURA DE LUZ','documents/factura_40.pdf','2025-01-07 20:26:16.144000'),(51,'FACTURA DE LUZ','documents/factura_42.pdf','2025-01-07 20:41:16.449000'),(52,'FACTURA DE LUZ','documents/factura_43.pdf','2025-01-07 20:54:31.568000'),(53,'FACTURA DE LUZ','documents/factura_44.pdf','2025-01-07 21:14:46.140000'),(54,'FACTURA DE LUZ','documents/factura_45.pdf','2025-01-07 21:41:19.937000'),(55,'FACTURA DE LUZ','documents/factura_46.pdf','2025-01-07 21:58:26.482000'),(56,'FACTURA DE LUZ','documents/factura_47.pdf','2025-01-07 22:13:04.811000'),(57,'FACTURA DE LUZ','documents/factura_48.pdf','2025-01-07 22:51:52.282000'),(58,'FACTURA DE LUZ','','2025-01-08 14:50:14.216000'),(59,'FACTURA DE LUZ','documents/factura_49.pdf','2025-01-08 14:50:53.083000');
/*!40000 ALTER TABLE `documents_document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents_documentaddress`
--

DROP TABLE IF EXISTS `documents_documentaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents_documentaddress` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `address_id_id` bigint NOT NULL,
  `customer_id_id` bigint NOT NULL,
  `document_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `documents_documentad_address_id_id_8c0b5f04_fk_addresses` (`address_id_id`),
  KEY `documents_documentad_customer_id_id_b5973132_fk_customers` (`customer_id_id`),
  KEY `documents_documentad_document_id_id_346f1c92_fk_documents` (`document_id_id`),
  CONSTRAINT `documents_documentad_address_id_id_8c0b5f04_fk_addresses` FOREIGN KEY (`address_id_id`) REFERENCES `addresses_address` (`id`),
  CONSTRAINT `documents_documentad_customer_id_id_b5973132_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`),
  CONSTRAINT `documents_documentad_document_id_id_346f1c92_fk_documents` FOREIGN KEY (`document_id_id`) REFERENCES `documents_document` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents_documentaddress`
--

LOCK TABLES `documents_documentaddress` WRITE;
/*!40000 ALTER TABLE `documents_documentaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `documents_documentaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents_documentbank`
--

DROP TABLE IF EXISTS `documents_documentbank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents_documentbank` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `document` varchar(100) DEFAULT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents_documentbank`
--

LOCK TABLES `documents_documentbank` WRITE;
/*!40000 ALTER TABLE `documents_documentbank` DISABLE KEYS */;
/*!40000 ALTER TABLE `documents_documentbank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents_documentcustomer`
--

DROP TABLE IF EXISTS `documents_documentcustomer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents_documentcustomer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_id_id` bigint NOT NULL,
  `document_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `documents_documentcu_customer_id_id_b03694a6_fk_customers` (`customer_id_id`),
  KEY `documents_documentcu_document_id_id_32d46eb1_fk_documents` (`document_id_id`),
  CONSTRAINT `documents_documentcu_customer_id_id_b03694a6_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`),
  CONSTRAINT `documents_documentcu_document_id_id_32d46eb1_fk_documents` FOREIGN KEY (`document_id_id`) REFERENCES `documents_document` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents_documentcustomer`
--

LOCK TABLES `documents_documentcustomer` WRITE;
/*!40000 ALTER TABLE `documents_documentcustomer` DISABLE KEYS */;
INSERT INTO `documents_documentcustomer` VALUES (1,7,1),(2,8,2),(3,11,3),(4,12,4),(5,13,5),(6,14,6),(7,15,7),(8,17,8),(9,18,9),(10,19,10),(11,20,11),(12,21,12),(13,23,13),(14,25,14),(15,28,15),(16,24,16),(17,29,17),(18,31,18),(19,32,19),(20,33,20),(21,34,21),(22,35,22),(24,36,24),(25,38,25),(26,37,26),(27,40,27),(28,41,28),(29,42,29),(30,44,30),(31,47,31),(32,50,32),(33,5,33),(34,9,34),(35,51,35),(36,53,36),(37,54,37),(38,55,38),(39,56,39),(40,57,40),(41,58,41),(42,62,42),(43,63,43),(44,65,44),(45,66,45),(46,68,46),(47,69,47),(48,71,48),(49,72,49),(50,73,50),(51,74,51),(52,75,52),(53,76,53),(54,77,54),(55,78,55),(56,79,56),(57,81,57),(58,82,58),(59,82,59);
/*!40000 ALTER TABLE `documents_documentcustomer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents_documentguarantee`
--

DROP TABLE IF EXISTS `documents_documentguarantee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents_documentguarantee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_id_id` bigint NOT NULL,
  `document_id_id` bigint NOT NULL,
  `garantia_id` bigint DEFAULT NULL,
  `investment_plan_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `documents_documentgu_customer_id_id_b6a75020_fk_customers` (`customer_id_id`),
  KEY `documents_documentgu_document_id_id_fe9bbd9a_fk_documents` (`document_id_id`),
  KEY `documents_documentgu_garantia_id_757be942_fk_financing` (`garantia_id`),
  KEY `documents_documentgu_investment_plan_id_i_9cd33a21_fk_Investmen` (`investment_plan_id_id`),
  CONSTRAINT `documents_documentgu_customer_id_id_b6a75020_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`),
  CONSTRAINT `documents_documentgu_document_id_id_fe9bbd9a_fk_documents` FOREIGN KEY (`document_id_id`) REFERENCES `documents_document` (`id`),
  CONSTRAINT `documents_documentgu_garantia_id_757be942_fk_financing` FOREIGN KEY (`garantia_id`) REFERENCES `financings_detailsguarantees` (`id`),
  CONSTRAINT `documents_documentgu_investment_plan_id_i_9cd33a21_fk_Investmen` FOREIGN KEY (`investment_plan_id_id`) REFERENCES `InvestmentPlan_investmentplan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents_documentguarantee`
--

LOCK TABLES `documents_documentguarantee` WRITE;
/*!40000 ALTER TABLE `documents_documentguarantee` DISABLE KEYS */;
/*!40000 ALTER TABLE `documents_documentguarantee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents_documentother`
--

DROP TABLE IF EXISTS `documents_documentother`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents_documentother` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` varchar(150) DEFAULT NULL,
  `customer_id_id` bigint NOT NULL,
  `document_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `documents_documentot_customer_id_id_a9a9bfe0_fk_customers` (`customer_id_id`),
  KEY `documents_documentot_document_id_id_2b689830_fk_documents` (`document_id_id`),
  CONSTRAINT `documents_documentot_customer_id_id_a9a9bfe0_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`),
  CONSTRAINT `documents_documentot_document_id_id_2b689830_fk_documents` FOREIGN KEY (`document_id_id`) REFERENCES `documents_document` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents_documentother`
--

LOCK TABLES `documents_documentother` WRITE;
/*!40000 ALTER TABLE `documents_documentother` DISABLE KEYS */;
/*!40000 ALTER TABLE `documents_documentother` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financings_accountstatement`
--

DROP TABLE IF EXISTS `financings_accountstatement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financings_accountstatement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `issue_date` date NOT NULL,
  `disbursement_paid` decimal(10,2) NOT NULL,
  `interest_paid` decimal(10,2) NOT NULL,
  `capital_paid` decimal(10,2) NOT NULL,
  `late_fee_paid` decimal(10,2) NOT NULL,
  `saldo_pendiente` decimal(12,2) NOT NULL,
  `abono` decimal(12,2) NOT NULL,
  `numero_referencia` varchar(255) NOT NULL,
  `description` longtext,
  `credit_id` bigint NOT NULL,
  `disbursement_id` bigint DEFAULT NULL,
  `payment_id` bigint DEFAULT NULL,
  `cuota_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_referencia` (`numero_referencia`),
  KEY `financings_accountst_credit_id_619f1f1b_fk_financing` (`credit_id`),
  KEY `financings_accountst_disbursement_id_8ba7c35c_fk_financing` (`disbursement_id`),
  KEY `financings_accountst_payment_id_6f997ba9_fk_financing` (`payment_id`),
  KEY `financings_accountst_cuota_id_0c01ed0d_fk_financing` (`cuota_id`),
  CONSTRAINT `financings_accountst_credit_id_619f1f1b_fk_financing` FOREIGN KEY (`credit_id`) REFERENCES `financings_credit` (`id`),
  CONSTRAINT `financings_accountst_cuota_id_0c01ed0d_fk_financing` FOREIGN KEY (`cuota_id`) REFERENCES `financings_paymentplan` (`id`),
  CONSTRAINT `financings_accountst_disbursement_id_8ba7c35c_fk_financing` FOREIGN KEY (`disbursement_id`) REFERENCES `financings_disbursement` (`id`),
  CONSTRAINT `financings_accountst_payment_id_6f997ba9_fk_financing` FOREIGN KEY (`payment_id`) REFERENCES `financings_payment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financings_accountstatement`
--

LOCK TABLES `financings_accountstatement` WRITE;
/*!40000 ALTER TABLE `financings_accountstatement` DISABLE KEYS */;
/*!40000 ALTER TABLE `financings_accountstatement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financings_banco`
--

DROP TABLE IF EXISTS `financings_banco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financings_banco` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `referencia` varchar(100) NOT NULL,
  `credito` decimal(12,2) NOT NULL,
  `debito` decimal(12,2) NOT NULL,
  `descripcion` longtext,
  `creation_date` datetime(6) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `secuencial` varchar(100) NOT NULL,
  `cheque` varchar(100) NOT NULL,
  `saldo_contable` decimal(12,2) NOT NULL,
  `saldo_disponible` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `referencia` (`referencia`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financings_banco`
--

LOCK TABLES `financings_banco` WRITE;
/*!40000 ALTER TABLE `financings_banco` DISABLE KEYS */;
/*!40000 ALTER TABLE `financings_banco` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financings_credit`
--

DROP TABLE IF EXISTS `financings_credit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financings_credit` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `proposito` longtext NOT NULL,
  `monto` decimal(15,2) NOT NULL,
  `plazo` int NOT NULL,
  `tasa_interes` decimal(5,3) NOT NULL,
  `forma_de_pago` varchar(75) NOT NULL,
  `frecuencia_pago` varchar(75) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `tipo_credito` varchar(75) NOT NULL,
  `codigo_credito` varchar(25) DEFAULT NULL,
  `creation_date` datetime(6) NOT NULL,
  `is_paid_off` tinyint(1) NOT NULL,
  `tasa_mora` decimal(15,2) NOT NULL,
  `saldo_pendiente` decimal(15,2) NOT NULL,
  `saldo_actual` decimal(15,2) NOT NULL,
  `estado_aportacion` tinyint(1) NOT NULL,
  `estados_fechas` tinyint(1) DEFAULT NULL,
  `desembolsado_completo` tinyint(1) NOT NULL,
  `plazo_restante` int DEFAULT NULL,
  `customer_id_id` bigint NOT NULL,
  `destino_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `financings_credit_customer_id_id_dd816f29_fk_customers` (`customer_id_id`),
  KEY `financings_credit_destino_id_id_e5fb34bb_fk_Investmen` (`destino_id_id`),
  CONSTRAINT `financings_credit_customer_id_id_dd816f29_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`),
  CONSTRAINT `financings_credit_destino_id_id_e5fb34bb_fk_Investmen` FOREIGN KEY (`destino_id_id`) REFERENCES `InvestmentPlan_investmentplan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financings_credit`
--

LOCK TABLES `financings_credit` WRITE;
/*!40000 ALTER TABLE `financings_credit` DISABLE KEYS */;
/*!40000 ALTER TABLE `financings_credit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financings_cuota`
--

DROP TABLE IF EXISTS `financings_cuota`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financings_cuota` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mes` int DEFAULT NULL,
  `start_date` datetime(6) NOT NULL,
  `due_date` datetime(6) DEFAULT NULL,
  `outstanding_balance` decimal(12,2) NOT NULL,
  `mora` decimal(12,2) NOT NULL,
  `interest` decimal(12,2) NOT NULL,
  `principal` decimal(12,2) NOT NULL,
  `installment` decimal(12,2) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `saldo_pendiente` decimal(12,2) NOT NULL,
  `interes_pagado` decimal(12,2) NOT NULL,
  `mora_pagado` decimal(12,2) NOT NULL,
  `fecha_limite` datetime(6) DEFAULT NULL,
  `cambios` tinyint(1) NOT NULL,
  `numero_referencia` varchar(255) DEFAULT NULL,
  `cuota_vencida` tinyint(1) NOT NULL,
  `credit_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `financings_cuota_credit_id_id_e18a5119_fk_financings_credit_id` (`credit_id_id`),
  CONSTRAINT `financings_cuota_credit_id_id_e18a5119_fk_financings_credit_id` FOREIGN KEY (`credit_id_id`) REFERENCES `financings_credit` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financings_cuota`
--

LOCK TABLES `financings_cuota` WRITE;
/*!40000 ALTER TABLE `financings_cuota` DISABLE KEYS */;
/*!40000 ALTER TABLE `financings_cuota` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financings_detailsguarantees`
--

DROP TABLE IF EXISTS `financings_detailsguarantees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financings_detailsguarantees` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo_garantia` varchar(75) NOT NULL,
  `especificaciones` json NOT NULL,
  `valor_cobertura` decimal(15,2) NOT NULL,
  `garantia_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `financings_detailsgu_garantia_id_id_5e4946d9_fk_financing` (`garantia_id_id`),
  CONSTRAINT `financings_detailsgu_garantia_id_id_5e4946d9_fk_financing` FOREIGN KEY (`garantia_id_id`) REFERENCES `financings_guarantees` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financings_detailsguarantees`
--

LOCK TABLES `financings_detailsguarantees` WRITE;
/*!40000 ALTER TABLE `financings_detailsguarantees` DISABLE KEYS */;
/*!40000 ALTER TABLE `financings_detailsguarantees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financings_disbursement`
--

DROP TABLE IF EXISTS `financings_disbursement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financings_disbursement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `forma_desembolso` varchar(75) NOT NULL,
  `monto_credito` decimal(15,2) NOT NULL,
  `monto_credito_agregar` decimal(15,2) NOT NULL,
  `monto_credito_cancelar` decimal(15,2) NOT NULL,
  `saldo_anterior` decimal(15,2) NOT NULL,
  `honorarios` decimal(15,2) NOT NULL,
  `poliza_seguro` decimal(15,2) NOT NULL,
  `monto_desembolsado` decimal(15,2) NOT NULL,
  `total_gastos` decimal(15,2) NOT NULL,
  `monto_total_desembolso` decimal(15,2) NOT NULL,
  `total_t` decimal(15,2) NOT NULL,
  `credit_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `financings_disbursem_credit_id_id_ec9319be_fk_financing` (`credit_id_id`),
  CONSTRAINT `financings_disbursem_credit_id_id_ec9319be_fk_financing` FOREIGN KEY (`credit_id_id`) REFERENCES `financings_credit` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financings_disbursement`
--

LOCK TABLES `financings_disbursement` WRITE;
/*!40000 ALTER TABLE `financings_disbursement` DISABLE KEYS */;
/*!40000 ALTER TABLE `financings_disbursement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financings_guarantees`
--

DROP TABLE IF EXISTS `financings_guarantees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financings_guarantees` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `descripcion` longtext NOT NULL,
  `suma_total` decimal(15,2) NOT NULL,
  `credit_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `financings_guarantee_credit_id_id_b1ded392_fk_financing` (`credit_id_id`),
  CONSTRAINT `financings_guarantee_credit_id_id_b1ded392_fk_financing` FOREIGN KEY (`credit_id_id`) REFERENCES `financings_credit` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financings_guarantees`
--

LOCK TABLES `financings_guarantees` WRITE;
/*!40000 ALTER TABLE `financings_guarantees` DISABLE KEYS */;
/*!40000 ALTER TABLE `financings_guarantees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financings_invoice`
--

DROP TABLE IF EXISTS `financings_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financings_invoice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `issue_date` date NOT NULL,
  `numero_factura` int NOT NULL,
  `recibo_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `financings_invoice_recibo_id_id_05aaffc8_fk_financings_recibo_id` (`recibo_id_id`),
  CONSTRAINT `financings_invoice_recibo_id_id_05aaffc8_fk_financings_recibo_id` FOREIGN KEY (`recibo_id_id`) REFERENCES `financings_recibo` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financings_invoice`
--

LOCK TABLES `financings_invoice` WRITE;
/*!40000 ALTER TABLE `financings_invoice` DISABLE KEYS */;
/*!40000 ALTER TABLE `financings_invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financings_payment`
--

DROP TABLE IF EXISTS `financings_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financings_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `monto` decimal(12,2) NOT NULL,
  `numero_referencia` varchar(255) NOT NULL,
  `fecha_emision` datetime(6) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `estado_transaccion` varchar(20) NOT NULL,
  `descripcion` longtext,
  `mora` decimal(12,2) NOT NULL,
  `interes` decimal(12,2) NOT NULL,
  `interes_generado` decimal(12,2) NOT NULL,
  `capital` decimal(12,2) NOT NULL,
  `capital_generado` decimal(12,2) NOT NULL,
  `boleta` varchar(100) DEFAULT NULL,
  `tipo_pago` varchar(75) NOT NULL,
  `descripcion_estado` longtext,
  `creation_date` datetime(6) NOT NULL,
  `credit_id` bigint DEFAULT NULL,
  `disbursement_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_referencia` (`numero_referencia`),
  KEY `financings_payment_credit_id_f9a3a746_fk_financings_credit_id` (`credit_id`),
  KEY `financings_payment_disbursement_id_21f86fb6_fk_financing` (`disbursement_id`),
  CONSTRAINT `financings_payment_credit_id_f9a3a746_fk_financings_credit_id` FOREIGN KEY (`credit_id`) REFERENCES `financings_credit` (`id`),
  CONSTRAINT `financings_payment_disbursement_id_21f86fb6_fk_financing` FOREIGN KEY (`disbursement_id`) REFERENCES `financings_disbursement` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financings_payment`
--

LOCK TABLES `financings_payment` WRITE;
/*!40000 ALTER TABLE `financings_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `financings_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financings_paymentplan`
--

DROP TABLE IF EXISTS `financings_paymentplan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financings_paymentplan` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mes` int DEFAULT NULL,
  `start_date` datetime(6) NOT NULL,
  `due_date` datetime(6) DEFAULT NULL,
  `outstanding_balance` decimal(12,2) NOT NULL,
  `mora` decimal(12,2) NOT NULL,
  `interest` decimal(12,2) NOT NULL,
  `principal` decimal(12,2) NOT NULL,
  `principal_pagado` decimal(12,2) NOT NULL,
  `installment` decimal(12,2) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `saldo_pendiente` decimal(12,2) NOT NULL,
  `interes_pagado` decimal(12,2) NOT NULL,
  `mora_pagado` decimal(12,2) NOT NULL,
  `fecha_limite` datetime(6) DEFAULT NULL,
  `cambios` tinyint(1) NOT NULL,
  `numero_referencia` varchar(255) DEFAULT NULL,
  `cuota_vencida` tinyint(1) NOT NULL,
  `interes_generado` decimal(12,2) NOT NULL,
  `capital_generado` decimal(12,2) NOT NULL,
  `interes_acumulado_generado` decimal(12,2) NOT NULL,
  `mora_acumulado_generado` decimal(12,2) NOT NULL,
  `mora_generado` decimal(12,2) NOT NULL,
  `paso_por_task` tinyint(1) NOT NULL,
  `credit_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `financings_paymentpl_credit_id_id_d27b8c8c_fk_financing` (`credit_id_id`),
  CONSTRAINT `financings_paymentpl_credit_id_id_d27b8c8c_fk_financing` FOREIGN KEY (`credit_id_id`) REFERENCES `financings_credit` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financings_paymentplan`
--

LOCK TABLES `financings_paymentplan` WRITE;
/*!40000 ALTER TABLE `financings_paymentplan` DISABLE KEYS */;
/*!40000 ALTER TABLE `financings_paymentplan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financings_recibo`
--

DROP TABLE IF EXISTS `financings_recibo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financings_recibo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `recibo` int NOT NULL,
  `interes` decimal(12,2) NOT NULL,
  `interes_pagado` decimal(12,2) NOT NULL,
  `mora` decimal(12,2) NOT NULL,
  `mora_pagada` decimal(12,2) NOT NULL,
  `aporte_capital` decimal(12,2) NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `factura` tinyint(1) NOT NULL,
  `cliente_id` bigint NOT NULL,
  `cuota_id` bigint DEFAULT NULL,
  `pago_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `financings_recibo_cliente_id_4aa46e17_fk_customers_customer_id` (`cliente_id`),
  KEY `financings_recibo_cuota_id_bc8165c5_fk_financings_paymentplan_id` (`cuota_id`),
  KEY `financings_recibo_pago_id_b161782e_fk_financings_payment_id` (`pago_id`),
  CONSTRAINT `financings_recibo_cliente_id_4aa46e17_fk_customers_customer_id` FOREIGN KEY (`cliente_id`) REFERENCES `customers_customer` (`id`),
  CONSTRAINT `financings_recibo_cuota_id_bc8165c5_fk_financings_paymentplan_id` FOREIGN KEY (`cuota_id`) REFERENCES `financings_paymentplan` (`id`),
  CONSTRAINT `financings_recibo_pago_id_b161782e_fk_financings_payment_id` FOREIGN KEY (`pago_id`) REFERENCES `financings_payment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financings_recibo`
--

LOCK TABLES `financings_recibo` WRITE;
/*!40000 ALTER TABLE `financings_recibo` DISABLE KEYS */;
/*!40000 ALTER TABLE `financings_recibo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pictures_imagen`
--

DROP TABLE IF EXISTS `pictures_imagen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pictures_imagen` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  `description` longtext,
  `uploaded_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pictures_imagen`
--

LOCK TABLES `pictures_imagen` WRITE;
/*!40000 ALTER TABLE `pictures_imagen` DISABLE KEYS */;
/*!40000 ALTER TABLE `pictures_imagen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pictures_imagenaddress`
--

DROP TABLE IF EXISTS `pictures_imagenaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pictures_imagenaddress` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `address_id_id` bigint NOT NULL,
  `customer_id_id` bigint NOT NULL,
  `image_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pictures_imagenaddre_address_id_id_b0e14d58_fk_addresses` (`address_id_id`),
  KEY `pictures_imagenaddre_customer_id_id_4bd3d5b7_fk_customers` (`customer_id_id`),
  KEY `pictures_imagenaddre_image_id_id_9596ae0d_fk_pictures_` (`image_id_id`),
  CONSTRAINT `pictures_imagenaddre_address_id_id_b0e14d58_fk_addresses` FOREIGN KEY (`address_id_id`) REFERENCES `addresses_address` (`id`),
  CONSTRAINT `pictures_imagenaddre_customer_id_id_4bd3d5b7_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`),
  CONSTRAINT `pictures_imagenaddre_image_id_id_9596ae0d_fk_pictures_` FOREIGN KEY (`image_id_id`) REFERENCES `pictures_imagen` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pictures_imagenaddress`
--

LOCK TABLES `pictures_imagenaddress` WRITE;
/*!40000 ALTER TABLE `pictures_imagenaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `pictures_imagenaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pictures_imagencustomer`
--

DROP TABLE IF EXISTS `pictures_imagencustomer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pictures_imagencustomer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_id_id` bigint NOT NULL,
  `image_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pictures_imagencusto_customer_id_id_8869748f_fk_customers` (`customer_id_id`),
  KEY `pictures_imagencusto_image_id_id_cb991545_fk_pictures_` (`image_id_id`),
  CONSTRAINT `pictures_imagencusto_customer_id_id_8869748f_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`),
  CONSTRAINT `pictures_imagencusto_image_id_id_cb991545_fk_pictures_` FOREIGN KEY (`image_id_id`) REFERENCES `pictures_imagen` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pictures_imagencustomer`
--

LOCK TABLES `pictures_imagencustomer` WRITE;
/*!40000 ALTER TABLE `pictures_imagencustomer` DISABLE KEYS */;
/*!40000 ALTER TABLE `pictures_imagencustomer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pictures_imagenguarantee`
--

DROP TABLE IF EXISTS `pictures_imagenguarantee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pictures_imagenguarantee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_id_id` bigint NOT NULL,
  `image_id_id` bigint NOT NULL,
  `investment_plan_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pictures_imagenguara_customer_id_id_37492531_fk_customers` (`customer_id_id`),
  KEY `pictures_imagenguara_image_id_id_e097d620_fk_pictures_` (`image_id_id`),
  KEY `pictures_imagenguara_investment_plan_id_i_1f0c7cc5_fk_Investmen` (`investment_plan_id_id`),
  CONSTRAINT `pictures_imagenguara_customer_id_id_37492531_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`),
  CONSTRAINT `pictures_imagenguara_image_id_id_e097d620_fk_pictures_` FOREIGN KEY (`image_id_id`) REFERENCES `pictures_imagen` (`id`),
  CONSTRAINT `pictures_imagenguara_investment_plan_id_i_1f0c7cc5_fk_Investmen` FOREIGN KEY (`investment_plan_id_id`) REFERENCES `InvestmentPlan_investmentplan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pictures_imagenguarantee`
--

LOCK TABLES `pictures_imagenguarantee` WRITE;
/*!40000 ALTER TABLE `pictures_imagenguarantee` DISABLE KEYS */;
/*!40000 ALTER TABLE `pictures_imagenguarantee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pictures_imagenother`
--

DROP TABLE IF EXISTS `pictures_imagenother`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pictures_imagenother` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` varchar(150) DEFAULT NULL,
  `customer_id_id` bigint NOT NULL,
  `image_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pictures_imagenother_customer_id_id_8c4ceb53_fk_customers` (`customer_id_id`),
  KEY `pictures_imagenother_image_id_id_cc573d0b_fk_pictures_imagen_id` (`image_id_id`),
  CONSTRAINT `pictures_imagenother_customer_id_id_8c4ceb53_fk_customers` FOREIGN KEY (`customer_id_id`) REFERENCES `customers_customer` (`id`),
  CONSTRAINT `pictures_imagenother_image_id_id_cc573d0b_fk_pictures_imagen_id` FOREIGN KEY (`image_id_id`) REFERENCES `pictures_imagen` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pictures_imagenother`
--

LOCK TABLES `pictures_imagenother` WRITE;
/*!40000 ALTER TABLE `pictures_imagenother` DISABLE KEYS */;
/*!40000 ALTER TABLE `pictures_imagenother` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_role`
--

DROP TABLE IF EXISTS `roles_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_name` varchar(100) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_role`
--

LOCK TABLES `roles_role` WRITE;
/*!40000 ALTER TABLE `roles_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_role_permissions`
--

DROP TABLE IF EXISTS `roles_role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles_role_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `roles_role_permissions_role_id_permission_id_02b8688f_uniq` (`role_id`,`permission_id`),
  KEY `roles_role_permissio_permission_id_9fa0c0ee_fk_auth_perm` (`permission_id`),
  CONSTRAINT `roles_role_permissio_permission_id_9fa0c0ee_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `roles_role_permissions_role_id_0e786fbb_fk_roles_role_id` FOREIGN KEY (`role_id`) REFERENCES `roles_role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_role_permissions`
--

LOCK TABLES `roles_role_permissions` WRITE;
/*!40000 ALTER TABLE `roles_role_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles_role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_userrole`
--

DROP TABLE IF EXISTS `roles_userrole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles_userrole` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `idRole_id` bigint NOT NULL,
  `idUser_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `roles_userrole_idRole_id_66c2fc1c_fk_roles_role_id` (`idRole_id`),
  KEY `roles_userrole_idUser_id_f96c532c_fk_users_user_id` (`idUser_id`),
  CONSTRAINT `roles_userrole_idRole_id_66c2fc1c_fk_roles_role_id` FOREIGN KEY (`idRole_id`) REFERENCES `roles_role` (`id`),
  CONSTRAINT `roles_userrole_idUser_id_f96c532c_fk_users_user_id` FOREIGN KEY (`idUser_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_userrole`
--

LOCK TABLES `roles_userrole` WRITE;
/*!40000 ALTER TABLE `roles_userrole` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles_userrole` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user`
--

DROP TABLE IF EXISTS `users_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `type_identification` varchar(50) NOT NULL,
  `identification_number` varchar(15) NOT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `user_code` varchar(25) NOT NULL,
  `nationality` varchar(75) NOT NULL,
  `profile_pic` varchar(100) DEFAULT NULL,
  `rol` varchar(50) NOT NULL,
  `creation_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `identification_number` (`identification_number`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `user_code` (`user_code`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
INSERT INTO `users_user` VALUES (1,'pbkdf2_sha256$720000$uwyxV31bqAM5toRV388iDx$Kz2oHP8ZjJGa7N8yYMP1VBFZBxng1M6rZmiNHB06GxE=','2024-12-26 21:39:42.596000',1,'choc1403','','',1,1,'2024-10-28 23:41:45.284000','DPI','',NULL,'eloicx@gmail.com',1,'MASCULINO','2024-1','Guatemala','','Administrador','2024-10-28 23:41:45.515000'),(2,'pbkdf2_sha256$720000$EEvuqArXW8Z3mbY4KUNKzu$54gL75TfPQoCF6J5jU+VqTqKNhrhXtGmXb+S1DD8Rao=','2024-12-23 22:32:51.052000',1,'l_chenof1','LUISA FERNANDA','CHEN PACAY',1,1,'2024-10-28 23:41:45.284000','DPI','3246850171601','53373687','luisachenpacay@gmail.com',1,'FEMENINO','2024-2','Guatemala','','Administrador','2024-10-28 23:41:45.515000'),(3,'pbkdf2_sha256$720000$Kvpb5uCInvweu6sBS4rXiW$0U4qhD2Ig2hh57Lc6eOKJFoNH+R1hUWveAUDjw977Bw=',NULL,1,'g_rodriguez','Grecia','Rodríguez',1,1,'2024-10-28 23:41:45.284000','DPI','3692585565','37160995','g_rodriguez@gmail.com',1,'FEMENINO','2024-3','Guatemala','','Administrador','2024-10-28 23:41:45.515000'),(4,'pbkdf2_sha256$720000$BMbn9ZMSgDcI50aI19ycPk$xS/n3y0iBeFML+qMaOQMoNxvK5+k41Glv6uaZJNQW5U=','2024-12-26 22:18:18.562000',0,'andrea_tot','Andrea','Tot',0,1,'2024-12-23 22:39:11.487000','DPI','3253514141601','38616418','totandrea58@gmail.com',1,'FEMENINO','2024-4','Guatemala','','Secretaria','2024-12-23 22:39:11.788000');
/*!40000 ALTER TABLE `users_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_groups`
--

DROP TABLE IF EXISTS `users_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_groups_user_id_group_id_b88eab82_uniq` (`user_id`,`group_id`),
  KEY `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_user_groups_user_id_5f6f5a90_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_groups`
--

LOCK TABLES `users_user_groups` WRITE;
/*!40000 ALTER TABLE `users_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_user_permissions`
--

DROP TABLE IF EXISTS `users_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_user_permissions_user_id_permission_id_43338c45_uniq` (`user_id`,`permission_id`),
  KEY `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_user_permissions_user_id_20aca447_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_user_permissions`
--

LOCK TABLES `users_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-09 22:43:11
