-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 09, 2023 at 04:04 AM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `colegio`
--

-- --------------------------------------------------------

--
-- Table structure for table `usuario`
--

CREATE TABLE `usuario` (
  `id` int(10) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `password` char(102) DEFAULT NULL,
  `NOMBRES` varchar(30) DEFAULT NULL,
  `APELLIDOS` varchar(30) DEFAULT NULL,
  `EDAD` int(2) DEFAULT NULL,
  `GRADO` int(2) DEFAULT NULL,
  `ROL` varchar(30) DEFAULT NULL,
  `ID_HUELLA` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `usuario`
--

INSERT INTO `usuario` (`id`, `username`, `password`, `NOMBRES`, `APELLIDOS`, `EDAD`, `GRADO`, `ROL`, `ID_HUELLA`) VALUES
(1, 'jeospino', '+Mf0*eWKYZX+G2u0BPnrhzL9olw==*IKTK1l7/6Hbp9qOB7zNqjg==*c5AU7Oc55Ts+oOACfO3/ZA==', 'Jesly Paola', 'Ospino Porras', 20, 0, 'ADMINISTRADOR', 1),
(2, 'mjortiz', 'J5z/*mKkan29BV04UF/AyMtD8HQ==*mTG2HLwqxBwd0dzLD/5HnA==*l1h2UV1XAR9Cswb4J6hPBA==', 'MIGUEL JOSE', 'ORTIZ ORTIZ', 13, 6, 'ESTUDIANTE', 2),
(3, 'magonzalo', '/zBe*tw5pCE8fRuSLVRSn9fVJUQ==*xoBNNMMbdVxcDWJDCeI35w==*pv4iSE9U+bEC8+YCW4gaHg==', 'marco', 'GONZALO', 15, 9, 'ESTUDIANTE', 3),
(4, 'bavillanueva', 'hf4R*eFg3afeMbJ3XaDMAC15+RA==*wiOPw6Tb5q0no1WhoRFsHg==*qZuXK+PjVXDUtAHq9mfAuw==', 'Bryan Alfonso', 'VILLANUEVA RIVAS', 18, 11, 'ESTUDIANTE', 4),
(5, 'elepalza', 'zljJ*jayfAbw/YrAkEU41bLoAcQ==*JHcGLEa1vknsm1QMBhRJDg==*ARDS8SLCgwczhE7YzCaZwQ==', 'EDUARDO LORA', 'EPALZA OSPINO', 16, 10, 'ESTUDIANTE', 5),
(6, 'jaepalza', 's63M*bGdOKoa89wAxKfDyKkS6Bg==*eZ41/O5ZGl+2HTq6q6x70w==*Sm1eM3EcfaSoSz55cRSTXA==', 'JHOSTIN ALEXANDER', 'EPALZA MANJARREZ', 20, 0, 'ADMINISTRADOR', 6),
(7, 'jomarco', 'p4Jq*jYPeRtb3PflPJ4jkXZ+DCw==*D/y2r1g9KAFczHVMPi2Klg==*Tl/z3OCofVMjasNXcGMfDg==', 'JOSE JOSE', 'MARCO FABIAN', 20, 10, 'ESTUDIANTE', 7),
(8, 'kepalza', '+gbY*BOeXMUgr0zkz8T4r1wEKsA==*Ez7S/VY2CdWlmwZO7GOwcQ==*ojYyV8KF/C2fd+60R1m/tw==', 'KEWIN JESUS', 'EPALZA MANJARREZ', 17, 0, 'EGRESADO', 8),
(9, 'wemanjarrez', 'W8FU*ITrhGlf7PXwPFXRnwZMq8w==*ryaz9hGpb4Kb5eWn+wLB9g==*E9Q21HBKK0aqPoz0ff3qTA==', 'WENDY JOHANA', 'MANJARREZ NOVOA', 41, 0, 'ACUDIENTE', 9),
(10, 'prueba1', 'giHE*d/R5TATIMixUFhEABgwqQg==*FRn1fQVzw0dKHMDAJBZYXg==*quqmxSuw3KZ4iwSGnK7eRw==', 'prueba1', 'prueba1', 20, 10, 'ESTUDIANTE', NULL),
(11, 'prueba2', 'hZmV*IjjGYLx8OtVWzyOnbPU3Iw==*fnbtk04Q9zNtKJOjt5x3gg==*Naj+jYnBHstr51rDe3IveQ==', 'prueba2', 'prueba2', 20, 10, 'ESTUDIANTE', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
