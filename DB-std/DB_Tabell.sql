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
  PRIMARY KEY (NickID),
  CONSTRAINT UC_Nick UNIQUE (Nick)
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
  `NickID` int DEFAULT NULL,
  `Publisert` datetime DEFAULT NULL,
  `Xmjosnr` tinyint UNSIGNED NOT NULL,
  `Tittel` varchar(70) NOT NULL,
  `GCkode` varchar(25) DEFAULT NULL,
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
  `Kategori` varchar(70) NOT NULL,
  `Type` varchar(10) DEFAULT NULL,
  `Kommentar` text DEFAULT NULL,
  `Oppdatert` datetime NOT NULL on UPDATE current_timestamp() DEFAULT current_timestamp(),
  CONSTRAINT Unike_Variabler UNIQUE (Variabel),
  PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Data for tabell `settings` med standardverdier
--
INSERT INTO `settings` (`ID`, `Variabel`,  `Verdi`, `Kategori`, `Type`, `Kommentar`, `Oppdatert`) 
VALUES (NULL, 'Forkortelse_Traditional'     ,'TRAD'                            ,'Forkortelse'              ,'streng'           ,'Forkortelse på traditionell cache. Brukes i scoreboard-tabellen', current_timestamp()), 
(NULL, 'Forkortelse_Multi'                  ,'MULTI'                           ,'Forkortelse'              ,'streng'           ,'Forkortelse på multi-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Mystery'                ,'MYST'                            ,'Forkortelse'              ,'streng'           ,'Forkortelse på mystery-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Letterbox'              ,'LETTER'                          ,'Forkortelse'              ,'streng'           ,'Forkortelse på letter-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Earth'                  ,'EARTH'                           ,'Forkortelse'              ,'streng'           ,'Forkortelse på earth-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Wherigo'                ,'WHERI'                           ,'Forkortelse'              ,'streng'           ,'Forkortelse på wherigo-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Lab'                    ,'LAB'                             ,'Forkortelse'              ,'streng'           ,'Forkortelse på lab-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'Forkortelse_Virt'                   ,'VIRT'                            ,'Forkortelse'              ,'streng'           ,'Forkortelse på virtuell-cache. Brukes i scoreboard-tabellen', current_timestamp()),
(NULL, 'EndeligResultat'                    ,'false'                           ,'Annet'                    ,'true/false'       ,'Hvis denne settes til true, vil "Endelig resultat" vises rett over scoreboard-tabellen.', current_timestamp()),
(NULL, 'IMAP_srv'                           ,'<IMAP-mailserver>'               ,'Mailoppsett'              ,'streng'           ,'IMAP-server til mailadressen som skal motta mails angående nytt utlegg eller ny logg ', current_timestamp()),
(NULL, 'IMAP_brukernavn'                    ,'<brukernavn/mailadresse>'        ,'Mailoppsett'              ,'streng'           ,'Brukernavn for å logge på IMAP-serveren', current_timestamp()),
(NULL, 'IMAP_passord'                       ,'<passord>'                       ,'Mailoppsett'              ,'streng'           ,'Passord for å logge på IMAP-serveren', current_timestamp()),
(NULL, 'SMTP_srv'                           ,'<SMTP-mailserver>'               ,'Mailoppsett'              ,'streng'           ,'SMTP-server til mailadressen som skal sende påminnelser', current_timestamp()),
(NULL, 'STMP_port'                          ,'465'                             ,'Mailoppsett'              ,'tall'             ,'Port for SMTP-serveren', current_timestamp()),
(NULL, 'SMTP_brukernavn'                    ,'<brukernavn/mailadresse>'        ,'Mailoppsett'              ,'streng'           ,'Brukernavn for å logge på SMTP-serveren', current_timestamp()),
(NULL, 'SMTP_passord'                       ,'<passord>'                       ,'Mailoppsett'              ,'streng'           ,'Passord for å logge på SMTP-serveren', current_timestamp()),
(NULL, 'info_mail'                          ,'<mailadresse>'                   ,'Mailoppsett'              ,'mail'             ,'Epostadresse hvor påminnelse om publisert cache vil sendes', current_timestamp()),
(NULL, 'sftp_hostname'                      ,'<url / sftp-server>'             ,'SFTP'                     ,'URL'              ,'URL til sftp-serveren', current_timestamp()),
(NULL, 'sftp_port'                          ,'22'                              ,'SFTP'                     ,'tall'             ,'Standard SFTP-port er: 22', current_timestamp()),
(NULL, 'sftp_username'                      ,'<brukernavn>'                    ,'SFTP'                     ,'streng'           ,'Brukernavn til sftp-pålogging', current_timestamp()),
(NULL, 'sftp_password'                      ,'<passord>'                       ,'SFTP'                     ,'streng'           ,'Passord til sftp-pålogging', current_timestamp()),
(NULL, 'sftp_mappe'                         ,'<filpath>'                       ,'SFTP'                     ,'streng'           ,'Mappe hvor X-Mjøs-filer lastes opp til!', current_timestamp()),
(NULL, 'mailbox_Feilet'                     ,'"<mailbox>"'                     ,'Mailoppsett'              ,'streng'           ,'Mailboks som fylles med mails som feiler, f.eks. hvis en mail kommer og skriptet ikke klarer å lese variabelen', current_timestamp()),
(NULL, 'mailbox_Prosessert'                 ,'"<mailbox>"'                     ,'Mailoppsett'              ,'streng'           ,'Mailboks som fylles med mails som er behandlet av skriptet og lagt inn i databasen suksessfullt', current_timestamp()),
(NULL, 'mailbox_IKKExmjos'                  ,'"<mailbox>"'                     ,'Mailoppsett'              ,'streng'           ,'Mailboks som fylles med mails som ikke er en del av XMJØS ', current_timestamp()),
(NULL, 'mailbox_UtenforINTERVALL'           ,'"<mailbox>"'                     ,'Mailoppsett'              ,'streng'           ,'Mailboks som fylles med mails som ble logget eller funnet etter endt frist spesifisert under i delen "Poenggiving"', current_timestamp()),
(NULL, 'KonkurranseStart'                   ,'2023-12-01'                      ,'Tid'                      ,'dato'             ,'Fra og med denne datoen registreres poeng for funn av cache', current_timestamp()),
(NULL, 'KonkurranseSlutt'                   ,'2023-12-31'                      ,'Tid'                      ,'dato'             ,'Dato på når konkurransen er ferdig (yyyy-mm-dd). Funn etter dette tidspunktet vil ikke telle med i konkurransen', current_timestamp()),
(NULL, 'FristLogging'                       ,'2024-01-06'                      ,'Tid'                      ,'dato'             ,'Dato på når det er frist å logge på nett (yyyy-mm-dd). Logger etter denne fristen vil ikke telles med i konkurransen.', current_timestamp()),
(NULL, 'TRE_poeng'                          ,'0'                               ,'Poeng'                    ,'tall'             ,'Hvor mange dager etter utleggsdato skal det gis 3poeng', current_timestamp()),
(NULL, 'TO_poeng'                           ,'4'                               ,'Poeng'                    ,'tall'             ,'Hvor mange dager etter utleggsdato skal det gis 2poeng (1poeng gis resterende dager)', current_timestamp()),
(NULL, 'Årets_år'                           ,'2023'                            ,'Tid'                      ,'tall'             ,'Dette er året som xmjøs arrangeres og brukes for å telle riktig poeng basert på datoen folk logger', current_timestamp()),
(NULL, 'streber_antall_cachefunn'           ,'24'                              ,'Annet'                    ,'tall'             ,'Hvor mange cacher må en person finne for å bli "streber". Event telles ikke!', current_timestamp()),
(NULL, 'tid_oppdatert_poengtabell'          , NULL                             ,'Tid'                      ,'datetime'         ,'Tid på når forrige oppdatering av poenglisten var, enten om det har kommet ny logg, om en ny cache har blitt lagt ut eller om poeng er oppdatert. Denne variabelen vil oppdatere seg selv', current_timestamp()),
(NULL, 'cookie_gspkauth'                    ,''                                ,'Cookie'                   ,'streng'           ,'Denne variabelen må inneholde en gyldig auth-cookie fra geocaching.com. Cookien heter "gspkauth"', current_timestamp()),
(NULL, 'Intervall1_poeng'                   ,'05'                              ,'Intervall'                ,'tall'             ,'Hvor mange poeng skal gis for funn av cache i intervall 1 (første periode)?', current_timestamp()),
(NULL, 'Intervall2_poeng'                   ,'04'                              ,'Intervall'                ,'tall'             ,'Hvor mange poeng skal gis for funn av cache i intervall 2 (andre periode)?', current_timestamp()),
(NULL, 'Intervall3_poeng'                   ,'03'                              ,'Intervall'                ,'tall'             ,'Hvor mange poeng skal gis for funn av cache i intervall 3 (tredje periode)?', current_timestamp()),
(NULL, 'Intervall4_poeng'                   ,'02'                              ,'Intervall'                ,'tall'             ,'Hvor mange poeng skal gis for funn av cache i intervall 4 (fjerde periode)?', current_timestamp()),
(NULL, 'IntervallSTD_poeng'                 ,'00'                              ,'Intervall'                ,'tall'             ,'Hvor mange poeng skal gis for funn av cache i etter de fire intervallene?', current_timestamp()),
(NULL, 'Intervall1'                         ,'00'                              ,'Intervall'                ,'tall'             ,'Her settes lengden på intervall 1. Til og med hvor mange dager etter utleggsdato skal intervallet gjelde?', current_timestamp()),
(NULL, 'Intervall2'                         ,'01'                              ,'Intervall'                ,'tall'             ,'Her settes lengden på intervall 2. Til og med hvor mange dager etter utleggsdato skal intervallet gjelde?', current_timestamp()),
(NULL, 'Intervall3'                         ,'02'                              ,'Intervall'                ,'tall'             ,'Her settes lengden på intervall 3. Til og med hvor mange dager etter utleggsdato skal intervallet gjelde?', current_timestamp()),
(NULL, 'Intervall4'                         ,'03'                              ,'Intervall'                ,'tall'             ,'Her settes lengden på intervall 4. Til og med hvor mange dager etter utleggsdato skal intervallet gjelde?', current_timestamp()),
(NULL, 'filnavn_mail'                       ,'mail.html'                       ,'Filnavn'                  ,'streng'           ,'Fil som benyttes når mail lastes ned fra mailboksen med mail.py-skriptet og legges i en fil', current_timestamp()),
(NULL, 'filnavn_eksempelmail_logg'          ,'eksempelmail-LOGG.html'          ,'Filnavn'                  ,'streng'           ,'Fil som benyttes når Eksempelmail=2, som benytter en HTML fil i stedet for å laste ned mails!', current_timestamp()),
(NULL, 'filnavn_logg'                       ,'LOGS/log.log'                    ,'Filnavn'                  ,'streng'           ,'Filpath/filnavn til log-loggen for utregningsskriptene', current_timestamp()),
(NULL, 'filnavn_errlogg'                    ,'LOGS/error.log'                  ,'Filnavn'                  ,'streng'           ,'Filpath/filnavn til error-loggen for utregningsskriptene', current_timestamp()),
(NULL, 'Eksempeldata'                       ,'false'                           ,'Eksempeldata'             ,'true/false'       ,'Hovedverdi for eksempeldata. Hvis denne er true, vil eksempeldata definert i eksempeldata-variablene benyttes', current_timestamp()),
(NULL, 'Eksempeldata_tittel'                ,'<TITTEL>'                        ,'Eksempeldata'             ,'streng'           ,'Eksempelverdi (brukes for testing) på geocachetittel', current_timestamp()),
(NULL, 'Eksempeldata_nick'                  ,'<Nickname>'                      ,'Eksempeldata'             ,'streng'           ,'Eksempelverdi (brukes for testing) på nickname', current_timestamp()),
(NULL, 'Eksempeldata_dato'                  ,'<Dato>'                          ,'Eksempeldata'             ,'dato'             ,'Eksempelverdi (brukes for testing) på dato logget/utlagt. [dd/mm/åååå]', current_timestamp()),
(NULL, 'Eksempeldata_loggtype'              ,'<Loggtype>'                      ,'Eksempeldata'             ,'streng'           ,'Eksempelverdi (brukes for testing) på loggtype: [Found it, Attended, Will attend]', current_timestamp()),
(NULL, 'Eksempeldata_geocachetype'          ,'<Geocachetype>'                  ,'Eksempeldata'             ,'streng'           ,'Eksempelverdi (brukes for testing) på geocachetype: [Traditional Cache, Multi-cache, Unknown (Mystery) Cache, Letterbox Hybrid, Earthcache, Wherigo Caches, Lab Cache, Virtual Cache]', current_timestamp()),
(NULL, 'Eksempeldata_GCkode'                ,'<GCkode>'                        ,'Eksempeldata'             ,'streng'           ,'Eksempelverdi (brukes for testing) på gckode: GCxxxxx - 5 unike tall/bokstaver', current_timestamp())


-- (NULL, '', '', '', '', current_timestamp())



-- Fra Applikasjonensfilen "variabler.py.example" er variablene frem til INTERVALL-LENGDE skrevet inn her!


COMMIT;