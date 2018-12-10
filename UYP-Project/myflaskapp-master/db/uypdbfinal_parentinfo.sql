-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: uypdbfinal
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `parentinfo`
--

DROP TABLE IF EXISTS `parentinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `parentinfo` (
  `StudentID` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Address_Line1` varchar(255) DEFAULT NULL,
  `Address_Line2` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `Zip` varchar(255) DEFAULT NULL,
  `HomePhone` varchar(255) DEFAULT NULL,
  `WorkPhone` varchar(255) DEFAULT NULL,
  `CellPhone` varchar(255) DEFAULT NULL,
  KEY `parentinfo_ibfk_1` (`StudentID`),
  CONSTRAINT `parentinfo_ibfk_1` FOREIGN KEY (`StudentID`) REFERENCES `student` (`studentid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parentinfo`
--

LOCK TABLES `parentinfo` WRITE;
/*!40000 ALTER TABLE `parentinfo` DISABLE KEYS */;
INSERT INTO `parentinfo` VALUES ('78f8f60e-0571-45fe-b14b-b1b32cddb8b2','Sheila Jones','182 Pecan Rd.','Unit 1','Fort Worth','Texas','76231','8264529174','7123245436','5125253334'),('78f8f60e-0571-45fe-b14b-b1b32cddb8b2','John Jones','821 Walnut St','Unit 1','Lampasas','Texas','76550','7123245436','8721274391','9816253407');
/*!40000 ALTER TABLE `parentinfo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-09 20:31:34
