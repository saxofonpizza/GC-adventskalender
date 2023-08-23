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
  `Epost_mottatt` datetime NOT NULL DEFAULT current_timestamp(),
  `Registrert` datetime NOT NULL on UPDATE current_timestamp() DEFAULT current_timestamp(),
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


--
-- Tabellstruktur for tabell `settings`
--
CREATE TABLE `settings` (
  `ID` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `Variabel` varchar(70) NOT NULL,
  `Verdi` text DEFAULT NULL,
  `Type` varchar(10) DEFAULT NULL,
  `Kommentar` text DEFAULT NULL,
  `Oppdatert` datetime NOT NULL on UPDATE current_timestamp() DEFAULT current_timestamp(),
  CONSTRAINT Unike_Variabler UNIQUE (Variabel),
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Data for tabell `settings` med standardverdier
--
INSERT INTO `settings` (`ID`, `Variabel`, `Verdi`, `Type`, `Kommentar`, `Oppdatert`) 
VALUES (NULL, 'Forkortelse_Traditional'     ,'TRAD',                 'streng'           ,'Forkortelse på traditionell cache. Brukes i scoreboard-tabellen', current_timestamp()), 
(NULL, 'Forkortelse_Multi',         'MULTI',                         'streng'           ,'Forkortelse på multi-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Mystery',       'MYST',                          'streng'           ,'Forkortelse på mystery-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Letterbox',     'LETTER',                        'streng'           ,'Forkortelse på letter-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Earth',         'EARTH',                         'streng'           ,'Forkortelse på earth-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Wherigo',       'WHERI',                         'streng'           ,'Forkortelse på wherigo-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Lab',           'LAB',                           'streng'           ,'Forkortelse på lab-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Virt',          'VIRT',                          'streng'           ,'Forkortelse på virtuell-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'EndeligResultat',           'false',                         'true/false'       ,'Hvis denne settes til true, vil "Endelig resultat" vises rett over scoreboard-tabellen.', current_timestamp()),
(NULL, 'IMAP_srv',                  '<IMAP-mailserver>',             'URL'              ,'IMAP-server til mailadressen som skal motta mails angående nytt utlegg eller ny logg ', current_timestamp()),
(NULL, 'IMAP_brukernavn',           '<brukernavn/mailadresse>',      'streng'           ,'Brukernavn for å logge på IMAP-serveren', current_timestamp()),
(NULL, 'IMAP_passord',              '<passord>',                     'streng'           ,'Passord for å logge på IMAP-serveren', current_timestamp()),
(NULL, 'SMTP_srv',                  '<SMTP-mailserver>',             'streng'           ,'SMTP-server til mailadressen som skal sende påminnelser', current_timestamp()),
(NULL, 'STMP_port',                 '465',                           'tall'             ,'Port for SMTP-serveren', current_timestamp()),
(NULL, 'SMTP_brukernavn',           '<brukernavn/mailadresse>',      'streng'           ,'Brukernavn for å logge på SMTP-serveren', current_timestamp()),
(NULL, 'SMTP_passord',              '<passord>',                     'streng'           ,'Passord for å logge på SMTP-serveren', current_timestamp()),
(NULL, 'info_mail',                 '<mailadresse>',                 'mail'             ,'Epostadresse hvor påminnelse om publisert cache vil sendes', current_timestamp()),
(NULL, 'sftp_hostname',             '<url / sftp-server>',           'URL'              ,'URL til sftp-serveren', current_timestamp()),
(NULL, 'sftp_port',                 '22',                            'tall'             ,'Standard SFTP-port er: 22', current_timestamp()),
(NULL, 'sftp_username',             '<brukernavn>',                  'streng'           ,'Brukernavn til sftp-pålogging', current_timestamp()),
(NULL, 'sftp_password',             '<passord>',                     'streng'           ,'Passord til sftp-pålogging', current_timestamp()),
(NULL, 'sftp_mappe',                '<filpath>',                     'streng'           ,'Mappe hvor X-Mjøs-filer lastes opp til!', current_timestamp()),
(NULL, 'mailbox_Feilet',            '"<mailbox>"',                   'streng'           ,'Mailboks som fylles med mails som feiler, f.eks. hvis en mail kommer og skriptet ikke klarer å lese variabelen', current_timestamp()),
(NULL, 'mailbox_Prosessert',        '"<mailbox>"',                   'streng'           ,'Mailboks som fylles med mails som er behandlet av skriptet og lagt inn i databasen suksessfullt', current_timestamp()),
(NULL, 'mailbox_IKKExmjos',         '"<mailbox>"',                   'streng'           ,'Mailboks som fylles med mails som ikke er en del av XMJØS ', current_timestamp()),
(NULL, 'mailbox_UtenforINTERVALL',  '"<mailbox>"',                   'streng'           ,'Mailboks som fylles med mails som ble logget eller funnet etter endt frist spesifisert under i delen "Poenggiving"', current_timestamp()),
(NULL, 'KonkurranseStart',          '2023-12-01',                    'dato'             ,'Fra og med denne datoen registreres poeng for funn av cache', current_timestamp()),
(NULL, 'KonkurranseSlutt',          '2023-12-24',                    'dato'             ,'Dato på når konkurransen er ferdig (yyyy-mm-dd). Funn etter dette tidspunktet vil ikke telle med i konkurransen', current_timestamp()),
(NULL, 'FristLogging',              '2024-01-06',                    'dato'             ,'Dato på når det er frist å logge på nett (yyyy-mm-dd). Logger etter denne fristen vil ikke telles med i konkurransen.', current_timestamp()),
(NULL, 'TRE_poeng',                 '0',                             'tall'             ,'Hvor mange dager etter utleggsdato skal det gis 3poeng', current_timestamp()),
(NULL, 'TO_poeng',                  '4',                             'tall'             ,'Hvor mange dager etter utleggsdato skal det gis 2poeng (1poeng gis resterende dager)', current_timestamp()),
(NULL, 'Årets_år',                  '2023',                          'tall'             ,'Dette er året som xmjøs arrangeres og brukes for å telle riktig poeng basert på datoen folk logger', current_timestamp()),
(NULL, 'streber_antall_cachefunn',  '24',                            'tall'             ,'Hvor mange cacher må en person finne for å bli "streber". Event telles ikke!', current_timestamp()),
(NULL, 'tid_oppdatert_poengtabell',  NULL,                           'datetime'         ,'Tid på når forrige oppdatering av poenglisten var, enten om det har kommet ny logg, om en ny cache har blitt lagt ut eller om poeng er oppdatert. Denne variabelen vil oppdatere seg selv', current_timestamp())
-- (NULL, '', '', '', '', current_timestamp())



-- Fra Applikasjonensfilen "variabler.py.example" er variablene frem til INTERVALL-LENGDE skrevet inn her!


COMMIT;