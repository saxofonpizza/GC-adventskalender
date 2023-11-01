# Testing av variabler!
Avstand_status = 50


##############################################
#           Nødvendige libraries             #
##############################################
print("Bibliotek-krav:")
libraries = (
    "imaplib",
    "smtplib",
    "ssl",
    "email.mime.text",
    "email.mime.multipart",
    "datetime",
    "mariadb",
    "selenium",             # For watchlist 
    "time"                  # For watchlist
)
for x in libraries:
    print(f"  {x}:",end="")
    try:
        __import__(x)
        print(int(Avstand_status-len(f"  {x}:"))*" " + "[\x1b[32m VELLYKKET \x1b[0m]")
    except:
        print(int(Avstand_status-len(f"  {x}:"))*" " + "[\x1b[31m FEILET \x1b[0m]")
        print(f"    \x1b[3;30mSjekk om biblioteket {x} er installert\x1b[0m")



##############################################
#              Importeringer                 #
##############################################
try:
    import functions as func
    import imaplib
    import smtplib, ssl                             # Brukes for å sende mails
    from email.mime.text import MIMEText            # Brukes for å sende mails
    from email.mime.multipart import MIMEMultipart  # Brukes for å sende mails
except Exception as error:
    print("\nNødvendige bibliotek ble IKKE importert. Last ned alle nødvendige bibliotek før dette skriptet kjøres på nytt\n\n \
          ERROR-melding:")
    print(error)
    exit()


##############################################
#              Database-testing              #
##############################################
try:
    print("Databaseforbindelse:", end="")
    mariaDB_connection, DB_cursor = func.database_connection()
    print(int(Avstand_status-len("Databaseforbindelse:"))*" " + "[\x1b[32m VELLYKKET \x1b[0m]")

    # Sjekk at alle tabeller er tilgjengelige
    sql="SHOW tables"
    DB_cursor.execute(sql)    

except:
    print(int(Avstand_status-len("Databaseforbindelse:"))*" " + "[\x1b[31m FEILET \x1b[0m]")
    print("    \x1b[3;30mSjekk brukernavn, passord etc for db-forbindelsen\x1b[0m")



##################################################
# Test av mailforbindelse (mottakelse av logger) #
##################################################
print("Mailserver (IMAP):")
mailforbindelse = 0
try:
    print("  Serverpålogging:", end="")
    mail = imaplib.IMAP4_SSL(func.Variabler['IMAP_srv'])
    mail.login(func.Variabler['IMAP_brukernavn'], func.Variabler['IMAP_passord'])
    print(int(Avstand_status-len("  Serverpålogging:"))*" " + "[\x1b[32m VELLYKKET \x1b[0m]")
    mailforbindelse = 1
except:
    print(int(Avstand_status-len("  Serverpålogging:"))*" " + "[\x1b[31m FEILET \x1b[0m]")
    print("    \x1b[3;30mSjekk variabel: IMAP_srv, IMAP_brukernavn og IMAP_passord\x1b[0m")


# Sjekk at alle mailbokser kan åpnes
if mailforbindelse == 1:
    for mailbox in (('mailbox_Feilet',func.Variabler['mailbox_Feilet']),('mailbox_Prosessert',func.Variabler['mailbox_Prosessert']),('mailbox_IKKExmjos',func.Variabler['mailbox_IKKExmjos']),('mailbox_UtenforINTERVALL',func.Variabler['mailbox_UtenforINTERVALL'])): 
        mailstatus = mail.select(f'{mailbox[1]}')[0]
        
        print(f"  Mailbox ({mailbox[0]}):",end="")
        if mailstatus == "OK":
            print(int(Avstand_status-len(f"  Mailbox ({mailbox[0]}):"))*" " + "[\x1b[32m VELLYKKET \x1b[0m]")

        else:
            print(int(Avstand_status-len(f"  Mailbox ({mailbox[0]}):"))*" " + "[\x1b[31m FEILET \x1b[0m]")
            print(f"    \x1b[3;30mSjekk variabel: {mailbox[0]}\x1b[0m")
    mail.logout()



##############################################
# Test av mailforbindelse (sending av mails) #
##############################################
print("Mailserver (SMTP):")
message = MIMEMultipart("alternative")
message["Subject"] = "Testmail"
message["From"] = func.Variabler['SMTP_brukernavn']
message["To"] = func.Variabler['info_mail']

# Create the plain-text and HTML version of your message
text = f"""Dette er en testmail"""
html = f"""\
<html>
<body>
<p>
    <strong>Dette er kun en test</strong>
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
    try:
        print("  Serverpålogging:",end="")
        server.login(func.Variabler['SMTP_brukernavn'], func.Variabler['IMAP_passord'])
        print(int(Avstand_status-len(f"  Serverpålogging:"))*" " + "[\x1b[32m VELLYKKET \x1b[0m]")

    except:
        print(int(Avstand_status-len(f"  Serverpålogging:"))*" " + "[\x1b[31m FEILET \x1b[0m]")
        print("    \x1b[3;30mSjekk variabel: SMTP_srv, STMP_port\x1b[0m")


    try:
        print("  Sending av testmail:",end="")
        server.sendmail(
        func.Variabler['SMTP_brukernavn'], func.Variabler['info_mail'], message.as_string()
    )
        print(int(Avstand_status-len(f"  Sending av testmail:"))*" " + "[\x1b[32m VELLYKKET \x1b[0m]")
        
    except:
        print(int(Avstand_status-len(f"  Sending av testmail:"))*" " + "[\x1b[31m FEILET \x1b[0m]")
        print("    \x1b[3;30mSjekk variabel: SMTP_brukernavn, info_mail\x1b[0m")



##############################################
#           Variabel for watchlist           #
##############################################
print("Watchlist-variabel:",end="")
if len(func.Variabler['cookie_gspkauth']) > 10:
    print(int(Avstand_status-len(f"Watchlist-variabel:"))*" " + "[\x1b[32m VELLYKKET \x1b[0m]")
else:
    print(int(Avstand_status-len(f"Watchlist-variabel:"))*" " + "[\x1b[31m FEILET \x1b[0m]")
    print("  \x1b[3;30mSjekk variabel: cookie_gspkauth\x1b[0m")



print()
print(10*"-" + " Testskript ferdig " + 10*"-")