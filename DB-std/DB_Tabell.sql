-- Kjør disse linjene inne i en database, eventuelt kan de f.eks. importeres

--                CMD:  docker exec -it <containerID for DB> bash
-- Inne i konteineren:  mysql -p
--
--
-- Gjeldende verdier for tabeller: (skal dette erstattes, bruk "search & replace all")
-- __________________________
-- Nicktabell:    Nicknames
-- Utleggstabell: Utlegg
-- Loggertabell:  Logger
--
--

CREATE DATABASE IF NOT EXISTS `xmjos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `xmjos`;


-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Nicknames`
--

CREATE TABLE `Nicknames` (
  `NickID` int NOT NULL AUTO_INCREMENT,
  `Nick` varchar(50) NOT NULL,
  `URL_nick` text NOT NULL,
  `Bosted` varchar(20) DEFAULT NULL,
  `Registrert` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (NickID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Logger`
--

CREATE TABLE `Logger` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `NickID` int NOT NULL,
  `Loggtype` varchar(15) NOT NULL,
  `Dato_logget` date NOT NULL,
  `Xmjosnr` tinyint UNSIGNED NOT NULL,
  `URL_logg` text NOT NULL,
  `Poeng` tinyint UNSIGNED NOT NULL,
  `Kommentar` text DEFAULT NULL,
  `Epost_mottatt` datetime NOT NULL,
  `Registrert` datetime on UPDATE current_timestamp() DEFAULT current_timestamp(),
  PRIMARY KEY (ID),
  CONSTRAINT UC_LoggingAvNick UNIQUE (NickID,Loggtype,Xmjosnr),
  FOREIGN KEY (NickID)
    REFERENCES Nicknames(NickID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------


--
-- Tabellstruktur for tabell `Logger`
--

CREATE TABLE `Logger_forslag` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `NickID` int NOT NULL,
  `Loggtype` varchar(15) NOT NULL,
  `Dato_logget` date NOT NULL,
  `Xmjosnr` tinyint UNSIGNED NOT NULL,
  `URL_logg` text NOT NULL,
  `Poeng` tinyint UNSIGNED NOT NULL,
  `Epost_mottatt` datetime NOT NULL,
  `Registrert` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (ID),
  CONSTRAINT UC_LoggingAvNick UNIQUE (NickID,Loggtype,Xmjosnr),
  FOREIGN KEY (NickID)
    REFERENCES Nicknames(NickID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `Utlegg`
--

CREATE TABLE `Utlegg` (
  `ID` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `NickID` int NOT NULL,
  `Publisert` datetime DEFAULT NULL,
  `Xmjosnr` tinyint UNSIGNED NOT NULL,
  `Tittel` varchar(70) NOT NULL,
  `URL` text DEFAULT NULL,
  `Geocachetype` varchar(25) DEFAULT NULL,
  `Poeng` tinyint UNSIGNED NOT NULL DEFAULT '3',
  `Registrert` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (ID),
  FOREIGN KEY (NickID)
    REFERENCES Nicknames(NickID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SET GLOBAL time_zone = 'Europe/Oslo';

--
-- Tabellstruktur for tabell `Historikk`
--

CREATE TABLE `Historikk` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `NickID` int(11) NOT NULL,
  `Loggtype` varchar(15) NOT NULL,
  `Dato_logget` date NOT NULL,
  `Xmjosnr` tinyint(3) UNSIGNED NOT NULL,
  `URL_logg` text NOT NULL,
  `Poeng` tinyint(3) UNSIGNED NOT NULL,
  `Kommentar` text DEFAULT NULL,
  `Registrert` datetime NOT NULL,
  PRIMARY KEY (`ID`),
  FOREIGN KEY (`NickID`)
    REFERENCES `Nicknames` (`NickID`) 
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



COMMIT;