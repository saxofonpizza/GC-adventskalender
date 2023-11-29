# Dette skriptet skal hente informasjon fra motatte mails og regne ut hvor mange poeng som skal tildeles.
#   Hver logg legges i en egen rad i tabellen Logger. 

import datetime as dt
import mariadb as mariaDB
import variabler as v
import functions as func


def legg_til_logg(mailID, NickID, Loggtype, Dato_funnet, Xmjosnr, URL_logg, Epost_mottatt):
    # melding = f"[pr]     Rad legges til i tabellen {v.SQL_tabell_Logger_forslag}"
    # v.logging(melding,0,1)
    Poeng       = 0                     # Må ikke fjernes eller endres!


    ################## NYE Regler ##################
    # Funn samme dag                = 5p           #
    # Funn dag 2                    = 4p           #
    # Funn dag 3                    = 3p           #
    # Funn dag 4                    = 2p           #
    # Funn dag 5 til 6. januar      = 1p           #
    #                                              #
    #                                              #
    ################################################
    Intervall1_poeng = int(func.Variabler['Intervall1_poeng'])    # Dag 1
    Intervall2_poeng = int(func.Variabler['Intervall2_poeng'])    # Dag 2
    Intervall3_poeng = int(func.Variabler['Intervall3_poeng'])    # Dag 3
    Intervall4_poeng = int(func.Variabler['Intervall4_poeng'])    # Dag 4
    IntervallSTD_poeng = int(func.Variabler['IntervallSTD_poeng'])    # Resten av desember (standardintervall), gjelder til man ikke skal få poeng 

    # Hvor mange dager etter utleggsdato skal poengene for hvert intervall utgis?
    Intervall1 = int(func.Variabler['Intervall1'])
    Intervall2 = int(func.Variabler['Intervall2'])
    Intervall3 = int(func.Variabler['Intervall3'])
    Intervall4 = int(func.Variabler['Intervall4'])

    
    if Xmjosnr == 1:
        Intervall1   = Intervall1+1
        Intervall2   = Intervall2+1
        Intervall3   = Intervall3+1
        Intervall4   = Intervall4+1
    
    # Xmjosnr     = f"{Xmjosnr}/12/2022"
    # Omgjør strings til datoformat
    Dato_funnet_dato = dt.datetime.strptime(Dato_funnet, '%d/%m/%Y').date()
    Xmjosnr_dato = dt.datetime.strptime(str(Xmjosnr) + f"/12/{func.Variabler['Årets_år']}", '%d/%m/%Y').date()

    # Intervaller hvor "bunn" i intervallet er tidspunktet nærmest utleggsdato og "topp" er tidspunktet lengst unna utleggsdatoen
    Intervall1_bunn = Dato_funnet_dato >=   Xmjosnr_dato                                      # Sann hvis cachen ble funnet samme dag, eller etter utleggsdato
    Intervall1_topp = Dato_funnet_dato <=   Xmjosnr_dato + dt.timedelta(days=Intervall1)      # Sann hvis cachen ble funnet innen x antall dager ETTER utleggsdato, hvor x bestemmes av Intervall1-variabelen
    Intervall2_topp = Dato_funnet_dato <=   Xmjosnr_dato + dt.timedelta(days=Intervall2)      # Sann hvis cachen ble funnet innen x antall dager ETTER utleggsdato, hvor x bestemmes av Intervall2-variabelen
    Intervall3_topp = Dato_funnet_dato <=   Xmjosnr_dato + dt.timedelta(days=Intervall3)      # Sann hvis cachen ble funnet innen x antall dager ETTER utleggsdato, hvor x bestemmes av Intervall3-variabelen
    Intervall4_topp = Dato_funnet_dato <=   Xmjosnr_dato + dt.timedelta(days=Intervall4)      # Sann hvis cachen ble funnet innen x antall dager ETTER utleggsdato, hvor x bestemmes av Intervall4-variabelen
    IntervallSTD_topp = Dato_funnet_dato <= dt.datetime.strptime(func.Variabler['KonkurranseSlutt'], '%Y-%m-%d').date()  # Sann hvis cachen blir funnet FØR xmjøs-poenggiving er ferdig
    

    # Definerer hvor mange poeng som skal gis, basert på når cachen er funnet!
    if str(Loggtype).lower() == "found it":
        if  (Intervall1_bunn) and (Intervall1_topp):
            # melding =f"[pr]     FUNNET SAMME DAG eller innen {Intervall1} dag(er)!"
            # v.logging(melding,0,1)
            Poeng = Intervall1_poeng
        elif not (Intervall1_topp) and (Intervall2_topp):
            # melding = f"[pr]     FUNNET INNEN {Intervall2} DAG(ER)!"
            # v.logging(melding,0,1)
            Poeng = Intervall2_poeng
        elif not (Intervall2_topp) and (Intervall3_topp):
            # melding = f"[pr]     FUNNET INNEN {Intervall3} DAG(ER)!"
            # v.logging(melding,0,1)
            Poeng = Intervall3_poeng        
        elif not (Intervall3_topp) and (Intervall4_topp):
            # melding = f"[pr]     FUNNET INNEN {Intervall4} DAG(ER)!"
            # v.logging(melding,0,1)
            Poeng = Intervall4_poeng
        elif not (Intervall4_topp) and (IntervallSTD_topp):
            # melding = f"[pr]     Funnet etter {Intervall4} dager!"
            # v.logging(melding,0,1)
            Poeng = IntervallSTD_poeng
    elif str(Loggtype).lower() == "attended":
        Poeng = 3

    data = f"""
    INSERT INTO Logger_forslag (NickID, Loggtype, Dato_logget, Xmjosnr, URL_logg, Poeng, Epost_mottatt)
    VALUES
        ('{NickID}',"{Loggtype}",'{Dato_funnet_dato}','{Xmjosnr}','{URL_logg}','{Poeng}', '{Epost_mottatt}')
    """
    #print(data)
    DB_cursor.execute(data)
    mariaDB_connection.commit()
    # melding = "[pr]     VELLYKKET"
    # v.logging (melding,0,1)
    return 1
    


if __name__ == "__main__":
    tekst = """
Dette skriptet skal ikke kjøres direkte, men importeres til et annet script!
    """
    print(tekst)
else:
    # print('[pr]     Skriptet "Prosessering" er importert på riktig måte')
    # Definere en cursor
    mariaDB_connection, DB_cursor = func.database_connection()
