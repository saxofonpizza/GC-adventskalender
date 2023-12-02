# https://www.thepythoncode.com/article/reading-emails-in-python
# https://docs.python.org/3/library/email.html

# Dette skriptet skal hente data fra mails og legge dette i variabler!
# Så flyttes mailene i egne mapper

# DEL 1: https://www.youtube.com/watch?v=bbPwv0TP2UQ
# DEL 2: https://www.youtube.com/watch?v=Jt8LizzxkPU




import imaplib
import email
from email.header import decode_header
import variabler as v
import functions as func
import pytz
import datetime as dt
import smtplib, ssl                             # Brukes for å sende mails
from email.mime.text import MIMEText            # Brukes for å sende mails
from email.mime.multipart import MIMEMultipart  # Brukes for å sende mails

mail = imaplib.IMAP4_SSL(func.Variabler['IMAP_srv'])
mail.login(func.Variabler['IMAP_brukernavn'], func.Variabler['IMAP_passord'])



def send_mail_publisert (URL_cache, Tittel):
# https://realpython.com/python-send-email/
    message = MIMEMultipart("alternative")
    message["Subject"] = "NY publisering"
    message["From"] = func.Variabler['SMTP_brukernavn']
    message["To"] = func.Variabler['info_mail']

    # Create the plain-text and HTML version of your message
    text = f"""\
Ny geocache er publisert
Tittel: {Tittel}
GCkode: {URL_cache.rsplit("/",1)[1]}
Link:   {URL_cache}
"""
    html = f"""\
<html>
<body>
    <p>
        <h2>Ny geocache er publisert</h2>
        <br>
        <strong>Tittel:</strong> <a href="{URL_cache}">{Tittel}</a>
        <br>
        <strong>GCkode:</strong> {URL_cache.rsplit("/",1)[1]}
    </p>
</body>
</html>
"""
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)


    # Lag sikker forbindelse til serveren og send eposten!
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(func.Variabler['SMTP_srv'], func.Variabler['STMP_port'], context=context) as server:
        server.login(func.Variabler['SMTP_brukernavn'], func.Variabler['IMAP_passord'])
        server.sendmail(
            func.Variabler['SMTP_brukernavn'], func.Variabler['info_mail'], message.as_string()
        )


def hent_mailboxes():
    for i in mail.list()[1]:
        print(i.decode("utf-8"))


def mail_hent_ID():
        # Velger mappe
    a = mail.select("INBOX")


    # Henter IDen til alle mails i den valgte mappen. IDen lagres i "data" og lagres som en streng
    #  Result lagrer status på spørringen (OK eller "FAILED")
    #  Siste argumentet i mail.uid: ALL     - Henter all epost i valgt mailbox
    #                               UNSEEN  - Henter all ulest epost i valgt mailbox
    #result, data = mail.uid('search', None, "ALL")
    result, data = mail.uid('search', None, "UNSEEN")


    # Gjør strengen "data" om til en list, hvor man separerer IDene vha. mellomrommet mellom de
        # data              = [b'1 2 3 4 5'], ved å benytte split vil dette bli til 
        # mailIDs_i_bytes   = [b'1', b'2', b'3', b'4', b'5']
        # mailID            = [1, 2, 3, 4, 5]
    mailIDs_i_bytes = data[0].split()
    if len(mailIDs_i_bytes):
        mailIDs = b' '.join(mailIDs_i_bytes).decode("utf-8").split(" ")
    else:
        mailIDs = []
    
    return mailIDs

# Denne funksjonen lister opp mail-IDs sammen med subjectet.
# Brukes til feilsøking for å finne ut hvilke mails som har hvilke IDer
def hent_subject(debug,mailID):

    # result2 inneholder meldingen fra ID som siste_mail inneholder
    # FETCH-kommandoen "leser" eposten, og fjerner ulest-markeringen!
    result2, email_data = mail.uid('fetch', mailID, '(RFC822)')
    marker_mail_ulest(debug,mailID)

    for response in email_data:
        if isinstance(response, tuple):     
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            

            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            print("ID:",mailID)
            print("Subject:", subject)
            print()


def hent_fil_cache():           # Denne funksjonen simulerer at en HTML-fil er en mottatt mail! Brukes for DEBUGGING og TESTING
    try:
        with open(func.Variabler['filnavn_eksempelmail_logg'], 'r') as f:
            f = f.read()
    except:
        melding = f"[MAIL]   Finner ikke {func.Variabler['filnavn_eksempelmail_logg']}, Kjør mail.py for å generere denne filen"
        v.logging(melding,0,1)
        exit()
    f = f.split("#4A3841JFD#",1)
    subject = f[0].replace("#&NICK&#", func.Variabler['Eksempeldata_nick']).replace("#&TITTEL&#", func.Variabler['Eksempeldata_tittel']).replace("#&GEOCACHETYPE&#",func.Variabler['Eksempeldata_geocachetype'])
    body    = f[1].replace("#&NICK&#",func.Variabler['Eksempeldata_nick']).replace("#&LOGGTYPE&#",func.Variabler['Eksempeldata_loggtype']).replace("#&DATO&#",func.Variabler['Eksempeldata_dato']).replace("#&GEOCACHETYPE&#",func.Variabler['Eksempeldata_geocachetype']).replace("#&GCKODE&#",func.Variabler['Eksempeldata_GCkode'])

    #Sette inn egne verdier:

    return subject,body                      #Hvis to/flere sespons i email_data gir subject/body vil det ikke være sikkert at riktig body/subject blir valgt
    

def hent_mail_cache(debug, mailID):
    # # Velger siste ID som har kommet i mailboksen (baseres på siste IDen i listen)
    # siste_mail = mails[-1]
    

    # result2 inneholder meldingen fra ID som siste_mail inneholder
    # FETCH-kommandoen "leser" eposten, og fjerner ulest-markeringen!
    result2, email_data = mail.uid('fetch', mailID, '(RFC822)')
    marker_mail_ulest(debug,mailID)

    i=0
    x=0

    # Res
    for response in email_data:
        #response = email_data[0]       #Bruk denne linjen, når for-løkken er kommentert ut
        if debug > 1:
            i=i+1
            print(i)
        if isinstance(response, tuple):
            if debug > 1:
                print("IS INSTANCE TUPLE")         
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            
            # Dato og tid på motatt mail
            # Dato, encoding = decode_header(msg["Date"])[0]
            Dato = msg["Date"]                                                                                              # Henter Dato fra epost-headeren
            Dato_tilfeldig_tidssone = email.utils.parsedate_to_datetime(Dato)                                               # Gjør om dato-streng til datetime-format
            Tid_epost_motatt    = Dato_tilfeldig_tidssone.astimezone(pytz.timezone("Europe/Oslo")).replace(tzinfo=None) # Konverterer date-timeformatet til riktig tidssone og fjerner tidssonen fra DATETIME-formatet!

            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                if debug > 1:
                    print("SUBJEKTET ER I Bytes")
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            if debug > 0:
                print("Subject:", subject)
            
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                if debug > 1:
                    print("FRA ER I Bytes")
                From = From.decode(encoding)
            if debug > 1:
                print("Fra:", From)
            if debug > 0:
                print()
        
            # if the email message is multipart
            if msg.is_multipart():
                if debug > 1:
                    print("MELDINGEN ER EN MULTIPART")
                
                # iterate over email parts     
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    x=x+1
                    if debug > 1:
                        print(f"Meldingsdel WALK: {x}")
                        print(f"Content_type: {content_type}")
                        print(f"Content_disposition: {content_disposition}")
                    if content_type == "text/html":
                        try:
                            charset = part.get_charsets()[0]
                            if debug > 1:
                                print(charset)
                            # get the email body
                            body = part.get_payload(decode=True).decode(charset)                # Ved videresendt mail feiler denne .decode("utf-8").... Dette er fordi mailen ikke trenger å dekodes
                            # f = open("CACHE.html", "w")
                            # f.write(body)
                            # f.close()
                        except:
                            melding = "Noe er feil når det kommer til dekoding av mail-body"
                            print(melding)
                            with open(func.Variabler['filnavn_errlogg'], 'a') as f:
                                f.write(melding + "\n")
                    if debug > 1:
                        print()
                        print()
            else:
                if debug > 1:
                    print("MELDINGEN ER IKKE EN MULTIPART")
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode("utf-8")
                if content_type == "text/html":
                    # print only text email parts
                    print("HTML")
            return Tid_epost_motatt,subject,body                      #Hvis to/flere sespons i email_data gir subject/body vil det ikke være sikkert at riktig body/subject blir valgt
        if debug > 1:
            print("="*100)
            print()


def hent_variabler(subject, body,Tillatte_GCkoder):
    ##############   INFO OM .split() OG .rsplit()   ##############
    # .split() og .rsplit() benyttes for å dele en streng
    #   split-kommandoen lager en liste som har x antall items. Dette baseres på hvor mange ganger split() splitter strengen
    #   Hvis .split("-") benyttes, vil strengen bli splittet for alle tilfeller hvor "-" befinner seg
    #   For å begrense hvor mange ganger .split() skal splitte strengen kan "maxsplit" argumentet settes. Da vil .split() splitte fra venstre mot høyre og .rsplit() fra høyre mot venstre
    #   MAXSPLIT: .split("-", 3)    -    3 er "maxsplit"-nummeret og sier at strengen skal splittes maks 3 ganger!
    NY_eller_EKSISTERENDE_cache = subject.split(" ")

    GyldigCache=0
 
    melding = "[MAIL]   EMNE på mail: " + subject
    v.logging(melding,0,1)

    #####################################
    #           Mail = Utlegg           #
    #####################################
    if NY_eller_EKSISTERENDE_cache[1] == "Ny":
        melding = "[MAIL]   Denne mailen er en ny cache"
        v.logging(melding,0,1)
        
        if func.Variabler['Eksempeldata'] == 1:
            melding = "[MAIL]   Bruker eksempeldata for ny cache"
            v.logging(melding,0,1)
            # ------------------------ #
            #      Eksempeldata:
            # ------------------------ #
            Nick,Geocachetype,Xmjosnr,Tittel,URL_cache,Publisert = ["kattaisekken","Traditional Cache", 1, "X-Mjøs#01 - Trekatter","https://coord.info/GC9JF2","2022-12-01 14:01"]
            # Nick,Geocachetype,Xmjosnr,Tittel,URL_cache,Publisert = ["ubraland","Multi-cache", 2, "X-Mjøs#02 - Regnstorm","https://coord.info/GC9JF2","2022-12-02 04:01"]
            # Nick,Geocachetype,Xmjosnr,Tittel,URL_cache,Publisert = ["nittira","Traditional Cache", 3, "X-Mjøs#03 - Ansistor","https://coord.info/GC9JF2","2022-12-03 20:01"]
            # Nick,Geocachetype,Xmjosnr,Tittel,URL_cache,Publisert = ["tiramisju","Unknown Cache", 4, "X-Mjøs#04 - Tre nøtter til Askepott","https://coord.info/GC9JF2","2022-12-04 16:03:00"]
            URL_nick = "#Opera"
        else:
            for x in Tillatte_GCkoder:                                  # Sjekker om cachen faktisk er en X-mjøs-cache!
                if x.replace("0","O")  in subject.replace("0","O"):     # Gjør om 0 til O for å hindre skrivefeil i GC-kode
                    GyldigCache = 1
                    Xmjosnr = Tillatte_GCkoder[x]
                    GCkode = x
            
            if GyldigCache != 1: 
                melding = "[MAIL]   Mailen er ikke en del av X-Mjøs, EMNE: " + subject
                v.logging(melding,0,1)
                return [0,"Dette er ikke en X-Mjøs-cache"]

            try:
                Nick = body.split("Opprettet av:</strong> ",1)[1].split("</li>",1)[0]
            except:
                return [161]
            
            try:
                Geocachetype = body.split("Type:</strong> ",1)[1].split("</li>",1)[0]
            except:
                return [162]
            
            try:
                Tittel = subject.split(" (GC")[0].rsplit(f"{Geocachetype}: ",1)[1]
            except:
                return [163]
            
            URL_cache = f"https://coord.info/{GCkode}" 
            # try:
            #     URL_cache = "https://coord.info/GC" + subject.split(' (GC',1)[1].split('),', 1)[0]
            # except:        
            #     return [164]
            
            URL_nick = '#'

            # Send epost:

        return 160, Nick, Xmjosnr, Tittel, URL_cache, Geocachetype, URL_nick



    #####################################
    #            Mail = Logg            #
    #####################################
    elif NY_eller_EKSISTERENDE_cache[1] =="[LOG]":                                              # NY_eller_EKSISTERENDE_cache er 1 fordi logger-mail blir videresendt. Derdor er plass 0 "Vs:" og plass 1 "[LOG]"
        melding = "[MAIL]   Denne mailen er en logg"
        v.logging(melding,0,1)
        
        if func.Variabler['Eksempeldata'] == 1:
            melding = "[MAIL]   Bruker eksempeldata for logg"
            v.logging(melding,0,1)
            # ------------------------ #
            #      Eksempeldata:
            # ------------------------ #
            Nick,Loggtype,Dato_funnet,Xmjosnr,URL_logg,URL_nick = ['Teonline','Found it','02/12/2022','1','https://www.geocaching.com/seek/log.aspx?LUID=c0b89ddb-7674-4c06-b27e-5850defb682f','https://oracle.com']
            # Nick,Loggtype,Dato_logget,Xmjosnr,URL_logg = ['Clown_09','Found it','15/12/2022','2','https://www.geocaching.com/seek/log.aspx?LUID=243ddc94-e556-42c5-9d24-f6c1138c0442']
            # Nick,Loggtype,Dato_logget,Xmjosnr,URL_logg = ['Eliastm','Found it','03/12/2022','3','https://www.geocaching.com/seek/log.aspx?LUID=a01045ce-95aa-46e4-ab30-ede713ec24df']
            # Nick,Loggtype,Dato_logget,Xmjosnr,URL_logg = ['jukejoma','Found it','04/12/2022','4','https://www.geocaching.com/seek/log.aspx?LUID=8b16a2f6-bff6-41d8-a335-1b4afca5178c']
            # Nick,Loggtype,Dato_logget,Xmjosnr,URL_logg = ['alex543216','Found it','07/12/2022','5','https://www.geocaching.com/seek/log.aspx?LUID=bef0de36-61ce-45d2-85df-938055dfecd6']
            # Nick,Loggtype,Dato_logget,Xmjosnr,URL_logg = ['Nubbis', 'Attended', '09/12/2022', '6', 'https://tv2.no']
            # Nick,Loggtype,Dato_logget,Xmjosnr,URL_logg = ['Teonline','Found it','11/12/2022','7','https://vg.no']

            URL_nick = "#tabata"
        else:
            try:
                GCkode    = "GC" + body.split("http://coord.info/GC",1)[1].split('">',1)[0]         #Finn GCkode til logg
            except:
                return [279]
            
            for x in Tillatte_GCkoder:                                                              # Sjekker om cachen faktisk er en X-mjøs-cache!
                if x == GCkode:
                    GyldigCache = 1
                    Xmjosnr = Tillatte_GCkoder[x]
                
            if GyldigCache != 1: 
                melding = "[MAIL]   Mailen er ikke en del av X-Mjøs, EMNE: " + subject
                v.logging(melding,0,1)
                return [0,"Dette er ikke en X-Mjøs-cache"]
        
            try:
                Loggtype    = body.split("<strong>Loggtype:</strong> ",1)[1].split("</li>",1)[0]
            except:
                return [272]
            if Loggtype == 'Found it':
                try:
                    Nick        = subject.split(" found")[0].rsplit(": ",1)[1]
                except:
                    return [271]
            elif Loggtype == "Didn't find it":
                try:
                    # Nick        = subject.split(" couldn't find")[0].rsplit(": ",1)[1]
                    Nick        = subject.split(" found")[0].rsplit(": ",1)[1]
                except:
                    return [276]
            elif Loggtype == 'Attended':
                try:
                    Nick        = subject.split(" attended")[0].rsplit(": ",1)[1]
                except:
                    return [277]
            else:
                return [278]
            try:
                Dato_funnet = body.split("<strong>Dato:</strong> ")[1].split("</li>",1)[0]
            except:
                return [273]
            try:
                URL_logg    = body.split('">Logg</a>:</strong>')[0].rsplit('href="',1)[1]
            except:
                return [274]
            try:
                URL_nick    = body.split('<strong>Logget av:</strong>', 1)[1].split('<a href="',1)[1].split('">',1)[0]
            except:
                return [275]
        return 270, Nick, Loggtype, Dato_funnet, Xmjosnr, URL_logg, URL_nick
        # return 270, Nick, Loggtype, Dato_logget_dato, Xmjosnr, URL_logg, URL_nick

    
    # Denne inntreffer hvis mailen klassifiseres som x-mjøs, men programmet ikke forstår om det er ny cache eller en logg 
    else:         
            melding = "[MAIL]   Dette er et ukjent format på en cache, EMNE: " + subject
            print(melding)
            with open(func.Variabler['filnavn_errlogg'], 'a') as f:
                f.write(melding + "\n")
            return [0,"Ukjent format"]


def flytt_mail(mail_ID, mailbox_mappe):
    # https://coderzcolumn.com/tutorials/python/imaplib-simple-guide-to-manage-mailboxes-using-python#10
    
    copy = mail.uid('copy', mail_ID, mailbox_mappe)
    melding = f'[MAIL]   Mail er flyttet til {mailbox_mappe}, status: {copy}'
    v.logging(melding,0,1)


def slett_mail(debug,mail_ID):    
    mail.uid('STORE', mail_ID, '+FLAGS', '(\Deleted)')
    mail.expunge()
    if debug > 0:
        melding = f"[MAIL]   GAMMEL MAIL er slettet: {mail_ID}"
        v.logging(melding,0,1)

def marker_mail_ulest(debug,mail_ID):
    mail.uid('STORE', mail_ID, '-FLAGS', '(\Seen)')
    if debug > 0:
        melding = f"[MAIL]   MAIL er markert ulest: {mail_ID}"
        v.logging(melding,0,1)

def marker_mail_lest(debug,mail_ID):
    mail.uid('STORE', mail_ID, '+FLAGS', '(\Seen)')
    if debug > 0:
        melding =f"[MAIL]   MAIL er markert lest: {mail_ID}"
        v.logging(melding,0,1)

def mail_logout():
    mail.logout()
    print()
    print("[MAIL]   Forbindelse til mailboksen avsluttes!")


if __name__ == "__main__":
    print("""
Dette skriptet skal ikke kjøres direkte, men importeres til et annet script!""")
    x = input("For feilsøking, fortsett dette programmet. Er dette noe du ønsker? (y/n): ")
    if x.lower() in ["yes","y"]:
        print("""
01 - List opp alle mailbokser som kan benyttes.
02 - Finn "emnet" til mail_ID-ene av uleste mails i innboksen.
""")
        y = int(input("Hva ønsker du å kjøre? [1,2,3, osv.]: "))
        if y == 1:
            hent_mailboxes()
            print("\n\n")
            z=1
            while z!=0:
                mailbox=input("Skriv inn navnet på mailboxen du ønsker å teste (uten apostrofer): ")
                a = mail.select(f'"{mailbox}"')
                print(f"{a}\n\n")
                z=int(input("Ønsker du å forsøke på nytt? [0 = Nei, 1 = ja]: "))
        elif y == 2:
            print()
            mails = mail_hent_ID()
            i = 0
            for en_mail in mails:
                mails[i] = en_mail
                i+=1
            print("Uleste mails:",mails)
            for en_mail in mails:
                print()
                hent_subject(0,en_mail)
            
            mailID = input(f"Neste prosedyre vil overskrive filen {func.Variabler['filnavn_mail']}. Endre filnavnet på variabelen 'filnavn_mail' i databasen hvis du ikke ønsker dette!!!!\nOppgi mailID-nummeret på mailen du ønsker å legge i {func.Variabler['filnavn_mail']}: {mails} ")
            mailID,subject,body=hent_mail_cache(0,mailID)
            with open(func.Variabler['filnavn_mail'], 'w') as f:
                f.write(subject + "#4A3841JFD#\n" + body)
        mail_logout()
else:
    if v.debug > 0:
        print('[MAIL]   Skriptet "mail" er importert på riktig måte')


        # Lage database-forbindelse
        try:
            mariaDB_connection, DB_cursor = func.database_connection()
            
        except:
            print("Kan ikke finne databasen!")
            exit()