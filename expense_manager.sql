-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: expense_manager
-- ------------------------------------------------------
-- Server version	8.0.44

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

--
-- Table structure for table `boi_transactions`
--

DROP TABLE IF EXISTS `boi_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `boi_transactions` (
  `transaction_id` int NOT NULL,
  `time_stamp` datetime NOT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boi_transactions`
--

LOCK TABLES `boi_transactions` WRITE;
/*!40000 ALTER TABLE `boi_transactions` DISABLE KEYS */;
INSERT INTO `boi_transactions` VALUES (1051,'2022-12-03 10:15:00'),(1052,'2022-12-03 17:00:00'),(1053,'2022-12-04 10:00:00'),(1054,'2022-12-04 14:00:00'),(1055,'2022-12-05 08:59:00'),(1056,'2022-12-05 16:01:00'),(1057,'2022-12-06 09:00:00'),(1058,'2022-12-06 15:59:00'),(1059,'2022-12-07 12:00:00'),(1060,'2022-12-08 09:00:00'),(1061,'2022-12-09 10:00:00'),(1062,'2022-12-10 11:00:00'),(1063,'2022-12-10 17:30:00'),(1064,'2022-12-11 12:00:00'),(1065,'2022-12-12 08:59:00'),(1066,'2022-12-12 16:01:00'),(1067,'2022-12-25 10:00:00'),(1068,'2022-12-25 15:00:00'),(1069,'2022-12-26 09:00:00'),(1070,'2022-12-26 14:00:00'),(1071,'2022-12-26 16:30:00'),(1072,'2022-12-27 09:00:00'),(1073,'2022-12-28 08:30:00'),(1074,'2022-12-29 16:15:00'),(1075,'2022-12-30 14:00:00'),(1076,'2022-12-31 10:00:00');
/*!40000 ALTER TABLE `boi_transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `expense_date` date NOT NULL,
  `amount` float NOT NULL,
  `category` varchar(255) NOT NULL,
  `notes` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (1,'2026-03-10',450,'Entertainment','Movie'),(2,'2026-03-10',50,'Shopping','Vegetables'),(3,'2026-03-10',150,'Food','Chinese Food'),(4,'2026-03-10',20,'Others','Pencils'),(5,'2026-03-10',1500,'Utilities','Electricity bill'),(6,'2026-03-11',120,'Food','Sandwich'),(7,'2026-03-11',20,'Others','Pencils');
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `support_agent_logins`
--

DROP TABLE IF EXISTS `support_agent_logins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `support_agent_logins` (
  `login_id` int NOT NULL,
  `agent_id` int DEFAULT NULL,
  `login_time` datetime NOT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `support_agent_logins`
--

LOCK TABLES `support_agent_logins` WRITE;
/*!40000 ALTER TABLE `support_agent_logins` DISABLE KEYS */;
INSERT INTO `support_agent_logins` VALUES (1,101,'2025-01-06 07:50:00'),(2,101,'2025-01-06 08:15:00'),(3,102,'2025-01-07 18:10:00'),(4,103,'2025-01-08 12:00:00'),(5,104,'2025-01-11 09:30:00'),(6,104,'2025-01-11 10:05:00'),(7,105,'2025-01-11 14:30:00'),(8,106,'2025-01-12 10:00:00'),(9,107,'2025-01-09 17:59:00'),(10,108,'2025-01-10 18:05:00');
/*!40000 ALTER TABLE `support_agent_logins` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-12 10:11:29
