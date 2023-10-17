# AJAX Developer's DREAM
# https://www.w3schools.com/xml/ajax_intro.asp

import mail                                 # For lesing av mails
import Prosessering as pr                   # For utregning av poeng og, legge dette i databasen
import Prosessering_forslag as pr_forslag   # For utregning av poeng og, legge dette i databasen, gjelder et forlsag for utregning i 2023
from HTML_gen import html_generator         # For generering av en HTML-fil med data fra databasen
from HTML_gen_forslag import html_generator as html_generator_forslag # For generering av en HTML-fil med data fra databasen, gjelder et forlsag for utregning i 2023
import variabler as v
import functions as func
import datetime as dt
import diagram


# Lage database-forbindelse
try:
    mariaDB_connection, DB_cursor = func.database_connection()
    
except:
    print("Kan ikke finne databasen!")
    exit()



###########################
#  Hent gyldige GC-koder  #
###########################
sql = """SELECT Xmjosnr, GCkode
    FROM Utlegg
    WHERE GCkode is not NULL"""
DB_cursor.execute(sql)
sql_data = DB_cursor.fetchall()

GCkode_dict={}
for x in sql_data:
    Xmjosnr   = x[0]
    GCkode    = x[1]
    GCkode_dict[GCkode] = Xmjosnr




# cnOpts = pysftp.CnOpts(knownhosts='known_hosts')         #Definerer hvor known_hosts-filen ligger i konteineren!

v.debug = 0
# HTML_endret = 0
# fil_logg = open(v.filnavn_logg, "a")
# fil_errlogg = open(v.filnavn_errlogg, "a")
# fil_logg.write(f'\n\n\nNY KJØRING {dt.datetime.now().strftime("%d/%m-%Y %H:%M:%S")} \n')
melding = f'''\n\n
{"_"*100}
--  NY KJØRING {dt.datetime.now().strftime("%d/%m-%Y %H:%M:%S")}  --
{"¯"*100}\n'''
v.logging(melding,0,0)




i=0
mailIDs = mail.mail_hent_ID()
if mailIDs:
    melding = f"[MAIN]   Det er {len(mailIDs)} ulest(e) mail"
    v.logging(melding,1,1)
else:
    melding = "[MAIN]   Ingen mail ble funnet"
    v.logging(melding,1,1)

for mailID in mailIDs:
    i=i+1
    melding = "-"*100
    v.logging(melding,0,1)   
    melding = "MAIL NR: " + str(i)
    v.logging(melding,0,1) 

    if func.Variabler['Eksempeldata'] == 2:
        melding = "Eksempeldata er påskrudd! [2]"
        v.logging(melding,0,0)
        Epost_mottatt = dt.datetime.now()-dt.timedelta(hours=2, minutes=30)
        subject,body = mail.hent_fil_cache()                              #Hvis denne returnerer en error, vil neste if-setning kjøre da?
    else:
        Epost_mottatt,subject,body = mail.hent_mail_cache(v.debug, mailID)      #Hvis denne returnerer en error, vil neste if-setning kjøre da?

    Dato_xmjos_ferdig = dt.datetime.strptime(func.Variabler['FristLogging'], '%Y-%m-%d').date()    
    if Epost_mottatt.date() <= Dato_xmjos_ferdig:                              # Er cachen logget INNEN fristen?
        variabler = mail.hent_variabler(subject,body,GCkode_dict)                          #Hvis denne returnerer en error, vil neste if-setning kjøre da?
        melding = "[MAIN]   Variabler fra mail-script: " + str(variabler)
        v.logging(melding,0,1)

        if variabler[0] == 160:     # Nytt utlegg!
            Nick            = variabler[1]
            Xmjosnr         = variabler[2]
            Tittel          = variabler[3]
            URL_cache       = variabler[4]
            Geocachetype    = variabler[5]
            URL_nick        = variabler[6]
            
            # Send mail om nytt utlegg. Hvis mailsendingen feiler, fortsett med prosesseringen!
            try:
                mail.send_mail_publisert(URL_cache,Tittel)
                melding = "[MAIN]   Mail om utlegg er sendt!"
                v.logging(melding,0,1)
            except:
                melding = "[MAIN]   Sending av mail ved utlegg feilet. Forsetter med å legge utlegget til i databasen"
                v.logging(melding,0,1)

            NickID = pr.finn_NickID(Nick,URL_nick)                                                           # Finner NickID, og hvis nicket ikke er registrert før, opprettes en ID
            pr.legg_til_NYcache(NickID, Epost_mottatt, Xmjosnr, Tittel, URL_cache, Geocachetype)             # Legger dataen i en database
            pr.oppdater_tidspunkt()                                                                         # Oppdater tidspunkt for når databasen er endret
            # mail.marker_mail_lest(v.debug,mailID)
            mail.flytt_mail(mailID, func.Variabler['mailbox_Prosessert'])
            mail.slett_mail(v.debug,mailID)
            # HTML_endret = 1

        elif variabler[0] == 270:   # Ny logg!
            Nick        = variabler[1]
            Loggtype    = variabler[2]
            Dato_funnet = variabler[3]
            Xmjosnr     = variabler[4]
            URL_logg    = variabler[5]
            URL_nick    = variabler[6]

            # Er cachen funnet i INTERVALLET angitt i variabler.py (i desember)?
            # Isåfall skal ikke loggen telles i poenggivingen!
            Dato_kalender_start = dt.datetime.strptime(func.Variabler['KonkurranseStart'], '%Y-%m-%d').date()
            Dato_kalender_slutt = dt.datetime.strptime(func.Variabler['KonkurranseSlutt'], '%Y-%m-%d').date()
            Dato_logget_dato = dt.datetime.strptime(Dato_funnet, '%d/%m/%Y').date()
            if Dato_kalender_start <= Dato_logget_dato <= Dato_kalender_slutt:
                NickID = pr.finn_NickID(Nick,URL_nick)                                             # Finner NickID, og hvis nicket ikke er registrert før, opprettes en ID
                vellykket = pr.legg_til_logg(mailID, NickID, Loggtype, Dato_funnet, Xmjosnr, URL_logg, Epost_mottatt)        #Legger dataen i en database
                if vellykket:
                    mail.marker_mail_lest(v.debug,mailID)
                    mail.flytt_mail(mailID, func.Variabler['mailbox_Prosessert'])
                    mail.slett_mail(v.debug,mailID)
                    try:
                        # Legg til i Logg_forslag-tabellen!
                        pr_forslag.legg_til_logg(mailID, NickID, Loggtype, Dato_funnet, Xmjosnr, URL_logg, Epost_mottatt)        # Legger dataen i en database, for forslag 2023
                    except:
                        # Send mail at det ikke fungerte!
                        print("FEILET: Klarte ikke å legge til rad i Logger_forslag 2023-tabellen")
                    pr.oppdater_tidspunkt()                                                                                     # Oppdater tidspunkt for når databasen er endret
                    

                    # HTML_endret = 1

            else:
                mail.marker_mail_lest(v.debug,mailID)
                mail.flytt_mail(mailID, func.Variabler['mailbox_UtenforINTERVALL'])
                mail.slett_mail(v.debug,mailID)

            
        # Hvis variablene ikke hentes riktig vil en feilmelding returneres og en beskrivelse av feilen oppgis under
        elif variabler[0] > 1 and not(variabler[0] in [260,270,280]):                   # Hvis mail.variabel-skriptet returnerer med kode mellom 161 og 269, eller 271 og oppover, kjøres denne if-setningen 
            if variabler[0] == 100:
                melding = "X-mjosnummer kunne ikke leses utifra emnet. Er X-mjøs-prefiksen feil"
            elif variabler[0] == 161:
                melding = v.FEIL_161
            elif variabler[0] == 162:
                melding = v.FEIL_162
            elif variabler[0] == 163:
                melding = v.FEIL_163
            elif variabler[0] == 164:
                melding = v.FEIL_164
            elif variabler[0] == 165:
                melding = v.FEIL_165
            elif variabler[0] == 271:   
                melding = v.FEIL_271
            elif variabler[0] == 272:   
                melding = v.FEIL_272
            elif variabler[0] == 273:   
                melding = v.FEIL_273
            elif variabler[0] == 274:   
                melding = v.FEIL_274
            elif variabler[0] == 275:   
                melding = v.FEIL_275
            elif variabler[0] == 276:   
                melding = v.FEIL_276
            elif variabler[0] == 277:
                melding = v.FEIL_277
            elif variabler[0] == 278:
                melding = v.FEIL_278
            elif variabler[0] == 279:
                melding = v.FEIL_279
            else:
                melding = "UKJENT FEILKODE"
            melding = '[MAIN]   ' + f'{melding}'
            v.logging(melding,0,1)
            
            # FLYTT MAIL TIL EGEN FEILET-MAPPE?
            # Viktig at emnet (evt mial mottatt) blir loggført til en fil så man kan finne riktig mail for feilsøking :D
            mail.flytt_mail(mailID, func.Variabler['mailbox_Feilet'])
            mail.slett_mail(v.debug,mailID)
            melding = '[MAIN]   VELLYKKET, registrering av FEIL'
            v.logging(melding,0,1)
                
        else:
            melding = "[MAIN]   Ingen rader blir lagt til databasen ettersom mailen IKKE er en NY cache eller en LOGG!"
            v.logging(melding,0,1)
            mail.marker_mail_lest(v.debug,mailID)
            mail.flytt_mail(mailID, func.Variabler['mailbox_IKKExmjos'])
            mail.slett_mail(v.debug,mailID)
            melding = '[MAIN]   VELLYKKET, registrering av mail som ikke er en del av X-Mjøs'
            v.logging(melding,0,1)

        print()
        if func.Variabler['Eksempeldata'] == 2:
            melding = f"""[MAIN]   Skriptet slutter fordi Eksempeldata=2, og det eksisterer kun én "{func.Variabler['filnavn_eksempelmail_logg']}"-fil\n"""
            v.logging(melding,0,1)
            exit()
        # if HTML_endret:
        #     html_generator(v.debug)
            # melding = "[MAIN]   Laster opp HTML-fil til internett"
            # v.logging(melding,0,1)
            # with pysftp.Connection(v.sftp_hostname, port=v.sftp_port, username=v.sftp_username, password=v.sftp_password, cnopts=cnOpts) as sftp:
            #         sftp.cwd(v.sftp_mappe)
            #         sftp.put(v.filnavn_HTML_komplett, preserve_mtime=True)  	# upload file to allcode/pycode on remote
            # melding = "[MAIN]   VELLYKKET Opplastning"
            # v.logging(melding,0,1)
            # melding = "<><>  HTML-SIDE OPPDATERT  <><>"
            # v.logging(melding,0,1)
        else:
            melding = '''[MAIN]   Ingen ny data er lagt inn i databasen. HTML-filen vil derfor ikke oppdateres\n[MAIN]   VELLYKKET, og HTML-siden er IKKE oppdatert!'''

    else:
        melding = "[MAIN]   Denne cachen ble logget ETTER godkjent frist og vil derfor IKKE være tellende i årets X-Mjøs!"
        v.logging(melding,0,0)
        mail.marker_mail_lest(v.debug,mailID)

# Last opp LOGG-filer til internett!
# melding = "\nFor alle prosesserte mails:\n[MAIN]   Laster opp LOGG-filer til internett"
# v.logging(melding,0,1)
# with pysftp.Connection(v.sftp_hostname, port=v.sftp_port, username=v.sftp_username, password=v.sftp_password, cnopts=cnOpts) as sftp:
#     sftp.cwd(f"{v.sftp_mappe}/LOGS")
#     sftp.put(v.filnavn_logg, preserve_mtime=True)
#     sftp.put(v.filnavn_errlogg, preserve_mtime=True)
# melding = "[MAIN]   VELLYKKET opplastning"
# v.logging(melding,0,1)


diagram.antall_funn()
melding = "[MAIN]   Diagram (antall funn) oppdatert!"
v.logging(melding,0,1)


#######################
#   HTML Generator    #
#######################
# html_generator(v.debug)
# melding = "<><>  HTML-SIDE OPPDATERT  <><>"
# v.logging(melding,0,1)

# try:
#     # Generer HTML_forslag
#     html_generator_forslag(v.debug)
# except:
#     # Send mail på at generering feilet
#     print("FEILET: html_generator_forslag")

melding = "<><>  SKRIPT FERDIG  <><>"
v.logging(melding,0,1)
exit()          # Stopper skriptet fra å kjøre
