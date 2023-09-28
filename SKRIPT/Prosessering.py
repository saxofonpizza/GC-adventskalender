# Dette skriptet skal hente informasjon fra motatte mails og regne ut hvor mange poeng som skal tildeles.
#   Hver logg legges i en egen rad i tabellen Logger. 

import datetime as dt
import mariadb as mariaDB
import variabler as v
import functions as func
import mail




def finn_NickID(Nick, URL_nick):              # Finner NickID, og hvis nicket ikke er registrert før, opprettes en ID
    DB_cursor.execute(f'SELECT EXISTS(SELECT * FROM Nicknames WHERE Nick = "{Nick}");')    # Returnerer 0 hvis nicket IKKE finnes, og 1 hvis det finnes
    Nick_eksistens = DB_cursor.fetchall()[0][0]
    
    if Nick_eksistens == 1:
        
        DB_cursor.execute(f"""
            SELECT NickID 
            FROM Nicknames
            WHERE Nick = '{Nick}'""")
        NickID = DB_cursor.fetchall()[0][0]
        melding = f"[pr]     Nicket eksisterer med ID: {NickID}"
        print(melding)
        with open(func.Variabler['filnavn_logg'], 'a') as f:
            f.write(melding + "\n")
    
        return NickID

    else:
        # Legg til Nicket
        melding = "[pr]     Nicket eksisterer IKKE, oppretter ID"
        print(melding)
        with open(func.Variabler['filnavn_logg'], 'a') as f:
            f.write(melding + "\n")
        DB_cursor.execute(f"""
            INSERT INTO Nicknames (Nick, URL_nick)
            VALUES ('{Nick}','{URL_nick}')""")
        mariaDB_connection.commit()
        DB_cursor.execute(f"""
            SELECT NickID 
            FROM Nicknames
            WHERE Nick = '{Nick}'""")
        NickID = DB_cursor.fetchall()[0][0]
        melding = f"[pr]     VELLYKKET, NickID {NickID} ble opprettet!"
        print(melding)
        with open(func.Variabler['filnavn_logg'], 'a') as f:
            f.write(melding + "\n")
        return NickID
    


def legg_til_NYcache(NickID, Publisert, Xmjosnr, Tittel, URL_cache, Geocachetype):
    melding = f"[pr]     Rad legges til i tabellen Utlegg"
    print(melding)
    with open(func.Variabler['filnavn_logg'], 'a') as f:
        f.write(melding + "\n")
    data = f"""
    UPDATE Utlegg
    SET 
        Publisert = "{Publisert}",
        Tittel = "{Tittel}",
        URL = "{URL_cache}",
        Geocachetype = "{Geocachetype}"
    WHERE
        Xmjosnr = {Xmjosnr} and
        Geocachetype != "Event"
    """
    # data = f"""
    # INSERT INTO Utlegg (NickID, Publisert, Xmjosnr, Tittel, URL, Geocachetype, Poeng)
    # VALUES
    #     ('{NickID}','{Publisert}','{Xmjosnr}','{Tittel}','{URL_cache}','{Geocachetype}','3')
    # """
    #print(data)
    DB_cursor.execute(data)
    mariaDB_connection.commit()
    melding = "[pr]     VELLYKKET"
    print(melding)
    with open(func.Variabler['filnavn_logg'], 'a') as f:
        f.write(melding + "\n")
    return


def legg_til_logg(mailID, NickID, Loggtype, Dato_logget, Xmjosnr, URL_logg, Epost_mottatt):
    melding = f"[pr]     Rad legges til i tabellen Logger"
    print(melding)
    with open(func.Variabler['filnavn_logg'], 'a') as f:
        f.write(melding + "\n")
    # Tabell som må opprettes for at dette skriptet skal fungere!
    # CREATE TABLE 'Logger' ('ID' INT NOT NULL AUTO_INCREMENT , 'Nick' VARCHAR(50) NOT NULL , 'Loggtype' VARCHAR(15) NOT NULL , 'Dato_logget' DATE NOT NULL , 'Xmjosnr' TINYINT UNSIGNED NOT NULL , 'URL_logg' TEXT NOT NULL , 'Poeng' TINYINT UNSIGNED NOT NULL , PRIMARY KEY ('ID')) ENGINE = InnoDB;


    #################### Regler ####################
    # Funn samme dag                = 3p           #
    # Funn dag 2 < x ≤ 5            = 2p           #
    # Funn dag 5 < x < 6.januar     = 1p           #
    #                                              #
    #                                              #
    ################################################

    # Hvor mange dager etter utleggsdato skal det gis hhv. 3p, 2p? 1p gis de resterende dagene
    TRE_poeng   = func.Variabler['TRE_poeng']
    TO_poeng    = func.Variabler['TO_poeng']
    Årets_år    = func.Variabler['Årets_år']
    Poeng       = 0                     # Må ikke fjernes eller endres!

    
    if Xmjosnr == 1:
        TRE_poeng   = TRE_poeng+1
        TO_poeng    = TO_poeng+1
    
    
    # Xmjosnr     = f"{Xmjosnr}/12/2022"



    # Omgjør strings til datoformat
    Dato_logget_dato = dt.datetime.strptime(Dato_logget, '%d/%m/%Y').date()
    Xmjosnr_dato = dt.datetime.strptime(str(Xmjosnr) + f"/12/{Årets_år}", '%d/%m/%Y').date()

    # Variabler for if-statements for å lage intervall for når ulike poeng skal tildeles
    TRE_poenger_bunn    = Dato_logget_dato >= Xmjosnr_dato
    TRE_poenger_topp    = Dato_logget_dato <= Xmjosnr_dato + dt.timedelta(days=TRE_poeng)
    TO_poenger_bunn     = Dato_logget_dato > Xmjosnr_dato + dt.timedelta(days=TRE_poeng)
    TO_poenger_topp     = Dato_logget_dato <= Xmjosnr_dato + dt.timedelta(days=TO_poeng)
    ETT_poeng_bunn      = Dato_logget_dato > Xmjosnr_dato + dt.timedelta(days=TO_poeng)
    ETT_poeng_topp      = Dato_logget_dato <= dt.date(Årets_år+1,1,6)


    # Definerer hvor mange poeng som skal gis, basert på når cachen er funnet!
    if str(Loggtype).lower() == "found it":
        if  (TRE_poenger_bunn) and (TRE_poenger_topp):
            melding =f"[pr]     FUNNET SAMME DAG eller innen {TRE_poeng} dag(er)!"
            print(melding)
            with open(func.Variabler['filnavn_logg'], 'a') as f:
                f.write(melding + "\n")
            Poeng = 3

        elif (TO_poenger_bunn) and (TO_poenger_topp):
            melding = f"[pr]     FUNNET INNEN {TO_poeng} DAG(ER)!"
            print(melding)
            with open(func.Variabler['filnavn_logg'], 'a') as f:
                f.write(melding + "\n")
            Poeng = 2

        elif (ETT_poeng_bunn) and (ETT_poeng_topp):
            melding = "[pr]     Funnet ila desember/januar!"
            print(melding)
            with open(func.Variabler['filnavn_logg'], 'a') as f:
                f.write(melding + "\n")
            Poeng = 1
    elif str(Loggtype).lower() == "attended":
        Poeng = 3

    data = f"""
    INSERT INTO Logger (NickID, Loggtype, Dato_logget, Xmjosnr, URL_logg, Poeng, Epost_mottatt)
    VALUES
        ('{NickID}',"{Loggtype}",'{Dato_logget_dato}','{Xmjosnr}','{URL_logg}','{Poeng}', '{Epost_mottatt}')
    """
    #print(data)
    try:
        DB_cursor.execute(data)
        mariaDB_connection.commit()
        melding = "[pr]     VELLYKKET"
        v.logging (melding,0,1)
        return 1
    except:
        melding = f"[pr]     Klarte ikke å legge til LOGG i tabellen Logger. Kan være pga. dupliserte rader (kombinasjon av nickID og Xmjosnr finnes fra før, sjekk DB)"
        v.logging(melding,0,1)
        mail.flytt_mail(mailID, func.Variabler['mailbox_Feilet'])
        mail.slett_mail(v.debug,mailID)
        return 0
    


if __name__ == "__main__":
    tekst = """
Dette skriptet skal ikke kjøres direkte, men importeres til et annet script!
    """
    print(tekst)
else:
    print('[pr]     Skriptet "Prosessering" er importert på riktig måte')
    
    # Definere en cursor
    mariaDB_connection, DB_cursor = func.database_connection()
