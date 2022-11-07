/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.4.21-MariaDB : Database - parkingreservation
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`parkingreservation` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `parkingreservation`;

/*Table structure for table `bookslot` */

DROP TABLE IF EXISTS `bookslot`;

CREATE TABLE `bookslot` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `slotid` varchar(100) DEFAULT NULL,
  `hourcost` varchar(100) DEFAULT NULL,
  `nameoncard` varchar(100) DEFAULT NULL,
  `cvv` varchar(100) DEFAULT NULL,
  `expiredate` varchar(100) DEFAULT NULL,
  `totalhours` varchar(100) DEFAULT NULL,
  `totalamount` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `useremail` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `bookslot` */

/*Table structure for table `customerreg` */

DROP TABLE IF EXISTS `customerreg`;

CREATE TABLE `customerreg` (
  `Id` int(200) NOT NULL AUTO_INCREMENT,
  `customername` varchar(200) DEFAULT NULL,
  `customeremail` varchar(200) DEFAULT NULL,
  `customerpassword` varchar(200) DEFAULT NULL,
  `customercontact` varchar(200) DEFAULT NULL,
  `customeraddress` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `customerreg` */

/*Table structure for table `parkingslots` */

DROP TABLE IF EXISTS `parkingslots`;

CREATE TABLE `parkingslots` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Parkingslot` varchar(100) NOT NULL,
  `Cost` varchar(100) NOT NULL,
  `Address` varchar(100) NOT NULL,
  `Imagename` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'unlocked',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `parkingslots` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
