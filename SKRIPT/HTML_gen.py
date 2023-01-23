# Dette skriptet lager en HTML fil som viser et Scoreboard av lagrede mails!

import mariadb as mariaDB
import variabler as v
import datetime as dt



# Denne funksjonen sjekker returnerer ingenting, hvis en liste er "tom" eller mangler en verdi
def objekt_i_liste(liste, plass):
  try:
    objekt = liste[0][plass]            # Hvis det tilfeldigvis er lagt ut to cacher samme dag, velges kun den ene!
    
    return objekt
  except:
    return ""

def streng_rotering(forkortelse):
    x=0
    i = []
    for bokstav in forkortelse:
        i.insert(x,"<br>" + bokstav)
        x+=1
    return ''.join(i)

# Funksjonen legger til poeng for et nick i hver celle. Funksjonen trenger å vite hvilke X-mjos-dager den skal ta for seg
def cache(dag):
    
    # Repetiv for hver dag som går. Legger inn en dag om gangen
    # logg_sql returnerer en liste med (nick, Xmjosnr, URL_logg, Poeng)   
    if i == 0:              # i er en teller, som blir 1 med en gang 1. nick er blitt gjennomført. Dette er så tittel-raden kun lages én gang
        DB_cursor.execute(f"SELECT Geocachetype,URL FROM {v.SQL_tabell_Utlegg} WHERE Xmjosnr = '{dag}'")
        Utlegg = DB_cursor.fetchall()
        if len(Utlegg) > 0:
            Geocachetype = objekt_i_liste(Utlegg,0)
            URL_cache = Utlegg[0][1]
        else:
            Geocachetype = ""
            URL_cache    = ""
        
        if Geocachetype == "Traditional Cache":
            Geocachetype = v.Traditional
        elif Geocachetype == "Multi-cache":
            Geocachetype = v.Multi
        elif Geocachetype == "Unknown (Mystery) Cache":
            Geocachetype = v.Mystery
        elif Geocachetype == "Letterbox Hybrid":
            Geocachetype = v.Letterbox
        elif Geocachetype == "Earthcache":
            Geocachetype = v.Earth
        elif Geocachetype == "Wherigo Caches":
            Geocachetype = v.Wherigo
        elif Geocachetype == "Lab Cache":
            Geocachetype = v.Lab
        elif Geocachetype == "Virtual Cache":
            Geocachetype = v.Virt
        else:
            Geocachetype = ""

        html_cachetype = f"""
    <th class="poeng_kolonne Geocachetype">
        <a href="{URL_cache}">{streng_rotering(Geocachetype)}</a>
    </th>"""
        fil_cachetype.write(html_cachetype)

        html_tittel = f"""
    <th class="poeng_kolonne Tittel_rad">
        {dag}
    </th>"""
        fil_tabell_tittel.write(html_tittel)
        
    
    # Kommando som søker i både Utlegg og Logger tabellen. Utleggere får U, mens logger viser poengsum
    logg_SQL = f"""
    SELECT NickID,Xmjosnr,URL,"U" as Poeng
    FROM {v.SQL_tabell_Utlegg}
    WHERE
        Publisert IS NOT NULL AND
        NickID = '{NickID}' AND 
        Xmjosnr = '{dag}' AND 
        (
            Geocachetype != 'Event' OR
            Geocachetype IS NULL
        )
    UNION ALL
    SELECT NickID,Xmjosnr,URL_logg,Poeng
    FROM {v.SQL_tabell_Logger}
    WHERE
        Loggtype = 'Found it' AND
        NickID = '{NickID}' AND
        Xmjosnr = '{dag}'
    """
    DB_cursor.execute(logg_SQL)
    en_logg = DB_cursor.fetchall()
    
    if debug == 1 and len(en_logg) > 0:
        print(en_logg)

    # Legger inn poengsummen for riktig dag
    html_dag = f"""
    <td class="Data poeng_kolonne poeng">
        <a href="{objekt_i_liste(en_logg,2)}">{objekt_i_liste(en_logg,3)}</a>
    </td>"""
    fil_tabell_data.write(html_dag)

def event(eventdag):
    if i == 0:              # i er en teller, som blir 1 med en gang 1. nick er blitt gjennomført. Dette er så tittel-raden kun lages én gang
        DB_cursor.execute(f"SELECT Geocachetype,URL FROM {v.SQL_tabell_Utlegg} WHERE Xmjosnr = '{eventdag}' AND Geocachetype = 'Event'")
        Utlegg = DB_cursor.fetchall()
        if len(Utlegg) > 0:
            Geocachetype = objekt_i_liste(Utlegg,0)
            URL_event = Utlegg[0][1]
        else:
            Geocachetype = ""
            URL_event    = ""
    if i==0:
        html_cachetype = f"""  
        <th class="poeng_kolonne Geocachetype Event">
            <a href="{URL_event}">{streng_rotering(Geocachetype.upper())}</a>
        </th>"""
        fil_cachetype.write(html_cachetype)
        html_tittel = f"""
        <th class="poeng_kolonne Tittel_rad Event">
            {eventdag}*
        </th>"""
        fil_tabell_tittel.write(html_tittel)
    logg_SQL = f"""
    SELECT nickID,Xmjosnr,URL_logg,Poeng
    FROM {v.SQL_tabell_Logger}
    WHERE
        Loggtype = 'Attended' AND
        NickID = '{NickID}' AND
        Xmjosnr = '{eventdag}'
    """
    # Legg til disse linjene i SQL-forespørselene over for å sette "U" på des om står som utlegger for events
    # SELECT NickID,Xmjosnr,URL,"U" as Poeng
    # FROM {v.SQL_tabell_Utlegg}
    # WHERE
    #     NickID = '{NickID}' AND 
    #     Xmjosnr = '{eventdag}' AND
    #     Geocachetype = 'Event'
    # UNION ALL

    DB_cursor.execute(logg_SQL)
    en_logg = DB_cursor.fetchall()
    if debug == 1 and len(en_logg) > 0:
        print(en_logg)

    # Legger inn poengsummen for riktig dag
    html_dag = f"""
        <td class="Data poeng_kolonne poeng Event">
            <a href="{objekt_i_liste(en_logg,2)}">{objekt_i_liste(en_logg,3)}</a>
        </td>"""
    fil_tabell_data.write(html_dag)


# -----------------------------------------------------------------------------------------------------------------------------------------
# HTML-GENERATOR
# -----------------------------------------------------------------------------------------------------------------------------------------
def html_generator(debugger):
    print("[HTML]   HTML-generatoren starter!")
    
    # Definering av globale variable
    global i
    global fil_tabell_tittel
    global NickID
    global Nick
    global fil_cachetype
    global fil_tabell_data
    global DB_cursor
    global debug
    debug = debugger

    rekkefølge_utlegg = []
    current_time = dt.datetime.now().strftime("%d/%m-%Y kl. %H:%M")
    # print("Current Time =", current_time)


    # Lage database-forbindelse
    try:
        mariaDB_connection = mariaDB.connect(
            user      = v.DB_user,
            password  = v.DB_password,
            host      = v.DB_host,
            port      = v.DB_port,
            database  = v.DB_database
        )

        # Definere en cursor
        DB_cursor = mariaDB_connection.cursor()
    except:
        print("Kan ikke finne databasen!")
        exit()




    i=0            # Denne variabelen sikrer at tittelen på tabellen kun skrives én gang!

    # Filer i dette dokumentet
    filnavn_tabell_tittel       = v.filnavn_tabell_tittel
    filnavn_tabell_data         = v.filnavn_tabell_data
    filnavn_tabell_cachetype    = v.filnavn_tabell_cachetype
    filnavn_HTML_komplett       = v.filnavn_HTML_komplett
    filnavn_utleggs_tabell      = v.filnavn_utleggs_tabell


#######################
#   Utlegg - TABELL   #
#######################
    fil_utlegg = open(filnavn_utleggs_tabell, "w",encoding="utf8")
    fil_utlegg.write("""
<table class="Utlegg">
    <tr>
        <th class ="Tittel Dato">
        </th>
        <th class="Tittel Nick">
            Nick
        </th>
        <th class="Tittel Publisert">
            Publisert
        </th>
        <th class="Tittel Xmjos">
            Cachenavn og link
        </th>
        <th class="Tittel Bosted">
            Bosted*
        </th>
    </tr>
""")
    fil_utlegg.close()
    fil_utlegg = open(filnavn_utleggs_tabell, "a",encoding="utf8")
    
    # Rekkefølgen på utleggstabellen bestemmes av hvilken rekkefølge utleggene ligger i databasen.
    Utlegg_SQL = f"""
    SELECT Xmjosnr, N.NickID, N.Nick, N.URL_nick, Publisert, Tittel, URL, N.Bosted, Geocachetype
    FROM {v.SQL_tabell_Utlegg} U 
    INNER JOIN {v.SQL_tabell_Nicknames} N ON U.NickID = N.NickID
    ORDER BY Xmjosnr
    """
    DB_cursor.execute(Utlegg_SQL)   
    for rad in DB_cursor.fetchall():                # Henter ut alle radene i SQL-forespørselen og går igjennom hver linje
        Xmjosnr     = rad[0]
        NickID      = rad[1]
        Nick        = rad[2]
        URL_nick    = rad[3]
        Publisert   = rad[4] 
        Tittel      = rad[5]
        URL_cache   = rad[6]
        Bosted      = rad[7]
        Geocachetype = rad[8]

        rekkefølge_utlegg.append((Xmjosnr,Geocachetype))

        if Publisert:
            Publisert = Publisert.strftime("%H:%M")
        else:
            Publisert = ""
        if str(URL_cache) == "None":         # Hvis det ikke finnes URL for cachen enda (den er ikke lagt ut)
            URL_cache = ""
        if Geocachetype == "Event":
            HTML_Utlegg = f"""
    <tr class="Data">
        <td class="Xmjosnr Data Event">
            {Xmjosnr}
        </td>
        <td class="Nick Data Event">
            <a href="{URL_nick}">{Nick}</a>
        </td>
        <td class="Publisert Data Event">
            {Publisert}
        </td>
        <td class="Xmjos Data Event">
            <a href="{URL_cache}">{Tittel}</a>
        </td>
        <td class="Utlegger Data Event">
            <i>{Bosted}</i>
        </td>
    </tr>""" 
        else: 
            HTML_Utlegg = f"""
    <tr class="Data">
        <td class="Xmjosnr Data">
            {Xmjosnr}
        </td>
        <td class="Nick Data">
            <a href="{URL_nick}">{Nick}</a>
        </td>
        <td class="Publisert Data">
            {Publisert}
        </td>
        <td class="Xmjos Data">
            <a href="{URL_cache}">{Tittel}</a>
        </td>
        <td class="Utlegger Data">
            <i>{Bosted}</i>
        </td>
    </tr>"""
        fil_utlegg.write(HTML_Utlegg)
    fil_utlegg.write("</table>")
    
    # Finner tall på antall nick som har skrevet en funn logg
    Antall_nick_SQL = f"""
    SELECT count(DISTINCT(NickID)) as 'Antall nick som funnet cache', count(NickID) as 'Antall funn-logger'
    FROM {v.SQL_tabell_Logger}
    WHERE
        Loggtype = 'Found it'
"""
    DB_cursor.execute(Antall_nick_SQL)
    Oppsummeringsdata  = DB_cursor.fetchall()
    Antall_nick        = Oppsummeringsdata[0][0]
    Antall_funn_logger = Oppsummeringsdata[0][1]

    a = v.Dato_kalender_slutt.split("/")
    b = v.Dato_xmjos_ferdig.split("/")
    Dato_kalender_slutt = f'{a[0]}/{a[1]}-{a[2]}'
    Dato_xmjos_ferdig = f'{b[0]}/{b[1]}-{b[2]}'


    # Tekst mellom UTLEGGs-tabellen og SCOREBOARD-tabellen
    TEKST = f"""
<center>
<div class="tabell_footer_Utlegg">
    <em>
        <strong style="color: #E2B842;">*</strong> Innholdet i denne ruta sier noe om hvor cacheutleggeren holder til. Det sier ingenting om hvor cachen vil komme. Siden vårt geografiske område spenner opp til 300 kilometer i ytterpunktene (luftlinje), har vi valgt å gjøre det på denne måten.
    </em>
</div>    
</center>
<br><br><br>
<div class="row">
        <center>
            <p class="tittel2" id="Poengliste">POENGLISTE</p>
            <hr class="tittel2">
        </center>
    <div class="column1">
        <a href="https://www.gcinfo.no/x-mjos-2022/">
            <div class="knapp normal_tekst">
                <span>Til reglement</span>
            </div>
        </a>
    </div>
    <div class="column2 normal_tekst">
        <ul>
            <li>3 p. for utlegg</li>
            <li>3 p. for funn på utleggsdag</li>
            <li>2 p. for funn 2-5 dager etter utleggsdato</li>
            <li>1 p. for funn i desember</li>
            <li>Årets strebere markeres i <span class="streber"><strong>GRØNT</strong></span>!</li>
        </ul>
    </div>
</div>

<div style="margin: 2em;"></div>

<center><i class="normal_tekst">Konkurransen gjelder t.o.m. {Dato_kalender_slutt}, og frist for logging på nett er {Dato_xmjos_ferdig}.</i></center>
"""
    
    if v.endelig_resultat == 1:
        TEKST2 = f"""
<div class="divTable">
	<div class="divTableBody">
		<div class="divTableRow">
			<div class="divTableCell oppsummering oppe">&nbsp;<p><b class="antall" style="margin-right:0.6em;">{Antall_nick}</b>nick har til nå logget en X-Mjøs-cache, og det har blitt skrevet<b class="antall" style="margin: 0 0.6em;">{Antall_funn_logger}</b>"funn" logger</p></div>
		</div>
		<div class="divTableRow">
			<div class="divTableCell farge_svart bunn">&nbsp;RESULTATET ER ENDELIG</div>
		</div>
	</div>
</div>
"""
    else:
        TEKST2 = f"""
<div class="divTable">
	<div class="divTableBody">
		<div class="divTableRow">
			<div class="divTableCell oppsummering oppe bunn">&nbsp;<p><b class="antall" style="margin-right:0.6em;">{Antall_nick}</b>nick har til nå logget en X-Mjøs-cache, og det har blitt skrevet<b class="antall" style="margin: 0 0.6em;">{Antall_funn_logger}</b>"funn" logger</p></div>
        </div>
	</div>
</div>
"""
    TEKST3 = f"""
<!--
<div class="oppsummering farge_lilla">
    <p><b class="antall" style="margin-right:0.6em;">{Antall_nick}</b></p><p>nick har til nå logget en X-Mjøs-cache, og det har blitt skrevet</p><p><b class="antall" style="margin: 0 0.6em;">{Antall_funn_logger}</b></p><p>"funn" logger</p>
</div>
-->
<div style="margin: 1em;"></div>
"""
    TEKST_tot = TEKST + TEKST2 + TEKST3
    fil_utlegg.write(TEKST_tot)
    fil_utlegg.close()

##########################
#   TEKST UNDER HEADER   #
##########################
#HER KAN TEKST OVER TABELLEN SKRIVES I HTML
    TEKST = f"""
    <center>
        <p class="tittel1" id="Tittel">X-Mjøs 2022 - ADVENTSKALENDER</p>
        <p class="font_times test"><i>OPPDATERT: </i>{current_time}</p>
        <hr class="tittel1">
        <br>
            <div class="row">
                <p>Denne siden gir oversikt over utlegg og poenggiving for X-Mjøs adventskalender 2022. På denne nettsiden finnes det én tabell for cache-utlegg ila. desember, 
                og én tabell som viser status på hvor mange poeng de ulike deltakerne har samlet.</p>
                <br>
                <p>Cellene i tabellene under er klikkbare. Trykkes det på brukernavnet til en deltager, vil man komme inn på deltagerens profil hos Geocaching. 
                Trykkes det på poenget til en deltager i tabellen POENGLISTE, vil dette ta deg til deltagerens cache-logg.</p>
                <br>
                <p>Nye logger vil legges til i poenglisten ila. 20 min etter logging hos <a href="https://geocaching.com">Geocaching.com</a></p>
                <br>
                <p>Siden tabellene utregnes automatisk, kan feil oppstå. Mener du noe er feil, send en mail til <a href="mailto:post@geocachen.no">post@geocachen.no</a></p>
                <br>
                <br>
                <p><strong>VIKTIG INFO:</strong>
                    <ul>
                        <li>X-Mjøs#01 ble publisert 2. desember. Derfor vil poengene som blir utdelt for å finne denne cachen bli forskjøvet. Poeng vil bli gitt som om denne cachen ble publisert 2. desember!</li>    
                        <li>For at en logg skal bli registrert, må det opprinnelig logges som et funn. Hvis det skirves en "note" på cachesiden, bør man ikke endre denne "noten" til å bli et funn. Da vil ikke loggen telles. Lag istedet en ny logg. </li>
                </ul></p>
                <br>
                <br>
                <div class="page">
                    <a href="#Utlegg">
                        <div class="knapp knapp_mellomrom normal_tekst">
                            <span>Tabell UTLEGG</span>
                        </div>
                    </a>
                    <a href="#Poengliste">
                        <div class="knapp knapp_mellomrom normal_tekst">
                            <span>Tabell POENGLISTE</span>
                        </div>
                    </a>
                    <a href="#Antall_funn">
                        <div class="knapp knapp_mellomrom normal_tekst">
                            <span>Graf FUNN per DAG</span>
                        </div>
                    </a>
                </div>
            </div>
        <br>
        <br>
        <br>
        <br>
        <p class="tittel2" id="Utlegg">UTLEGG</p>
        <hr class="tittel2">
    </center>
"""

    # Se om cahce er lagt ut i dag

    dato_idag   = dt.date.today()             # Gir dagens dato
    Dato_cacheutlegg_slutt = dt.datetime.strptime(v.Dato_cacheutlegg_slutt, '%d/%m/%Y').date()

    if dato_idag <= Dato_cacheutlegg_slutt:
        dato_dagens_dag = int(dato_idag.strftime("%d"))         # Brukes for å se etter riktig X-Mjøs
        SQL = f"""
        SELECT Publisert, Tittel, URL
        FROM {v.SQL_tabell_Utlegg}
        WHERE
            Xmjosnr = {dato_dagens_dag} and
            Geocachetype != "Event"
    """
        DB_cursor.execute(SQL)
        Utlegg = DB_cursor.fetchall()
        Tid_publisert = Utlegg[0][0]
        Tittel = Utlegg[0][1]
        URL_cache = Utlegg[0][2]
        if Tid_publisert:
            Tid_publisert = Tid_publisert.strftime("%H:%M")
            # Tittel, URL_cache = DB_cursor.execute(Utlegg_SQL)[0]
            TEKST2 = f"""<div class="oppsummering farge_lysebla oppe bunn">
    <p style="font-size:1.5em;"><strong>Dagens X-Mjøs,</strong> "<i><a href="{URL_cache}">{Tittel}</a></i>"<strong>, ble publisert {Tid_publisert}!</strong></p>
</div>
    """
        else:
            TEKST2 = """<div class="oppsummering farge_lysebla oppe bunn">
    <p style="font-size:1.5em;"><strong>Dagens X-Mjøs er ikke publisert enda!</strong></p>
</div>    
    """
    else:       # Kalenderen er ferdig 
        TEKST2 = """<div class="oppsummering farge_lysebla oppe bunn">
    <p style="font-size:1.5em;"><strong>Alle geocacher er publisert!</strong></p>
</div>    
    """

 
    #-- Starten av en HTML-fil ------------------------------------------------------------------------------------------V
    html_header = """<!DOCTYPE html>
    <html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-5WHWEBEE45"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-5WHWEBEE45');
        </script>
        <title>Poengtavle</title>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="300">
        <link rel="stylesheet" href="styles.css?version=1.7">
    </head>"""
    
    # Her ligger tittelen til Utleggstabellen!
    html_body_start =f"""
    <body class="bakgrunnsfarge">
    {TEKST}
    {TEKST2}
<div style="margin: 1em;"></div>"""



########################
# INITSIERING AV FILER #
########################
    fil_tabell_tittel = open(filnavn_tabell_tittel, "w",encoding="utf8")
    fil_tabell_tittel.write("""
    <tr>
        <th class="pl_kolonne Tittel_rad">
            Pl.
        </th>
        <th class="nick_kolonne Tittel_rad">
            Nick
        </th>
        <th class="sum_kolonne Tittel_rad">
            SUM
        </th>
    """)
    fil_tabell_tittel.close()
    fil_tabell_data = open(filnavn_tabell_data, "w",encoding="utf8")   # Tømmer filen
    fil_tabell_data.close()                           # Tømmer filen

    fil_cachetype = open(filnavn_tabell_cachetype, "w",encoding="utf8")
    fil_cachetype.write("""
    <tr> 
        <th class="bakgrunnsfarge"></th>
        <th class="bakgrunnsfarge"></th>
        <th class="bakgrunnsfarge"></th>""")
    fil_cachetype.close()

#--------------------------------------------------------------------------------------------------------------------^
#######################
# SCOREBOARD - TABELL #
#######################
    fil_tabell_tittel = open(filnavn_tabell_tittel, "a",encoding="utf8")
    fil_tabell_data = open(filnavn_tabell_data, "a",encoding="utf8")
    fil_cachetype = open(filnavn_tabell_cachetype, "a",encoding="utf8")

    # Gir en tabell med nick som har logget "found it"/"attended" og lagt ut cacher og gir
    #  rekkefølgen basert på hvor mange poeng hvert nick har
    rekkefølge_nick_SQL = f"""
    SELECT N.NickID, N.Nick, N.URL_nick, SUM(Poeng) as Totalsum, SUM(Poeng=3) as Antall_3Poeng, SUM(Poeng=2) as Antall_2Poeng, SUM(Poeng=1) as Antall_1Poeng
    FROM
    (
    SELECT NickID,Poeng
    FROM {v.SQL_tabell_Logger}
    WHERE
        Loggtype = 'Found it' OR
        Loggtype = 'Attended'
    UNION ALL
    SELECT NickID, Poeng
    FROM {v.SQL_tabell_Utlegg}
    WHERE Publisert IS NOT NULL
    ) t
    INNER JOIN {v.SQL_tabell_Nicknames} N
    ON N.NickID = t.NickID
    GROUP BY Nick
    ORDER BY Totalsum DESC, Antall_3poeng DESC, Antall_2poeng DESC, Antall_1poeng DESC
    """                                 # ORDER BY Totalsum DESC, vil gjøre rekkefølgen på de med lik sum tilfeldig
    ## Radene under gjør så utleggerne av event listes i Scoreboard-tabellen!
    # UNION ALL
    # SELECT NickID, Poeng
    # FROM {v.SQL_tabell_Utlegg}
    # WHERE Geocachetype = "Event"   


    DB_cursor.execute(rekkefølge_nick_SQL)
    rekkefølge_nick = DB_cursor.fetchall()
    if len(rekkefølge_nick) == 0:
        rekkefølge_nick = [("","","","")]       # Denne gjør så SCOREBOARD-tabellen vises riktig, selv om ingen logger har kommet enda!

    # -----------------------------------------------------------------------------------------------------
    # Her kan tabellen justeres, med når det skal være event osv!
    # cache(): Legger til X-antall dager med cachefunn. Verdiene (1,2) legger til DAG 1-2
    # event(): Legger til dag X med event. Verdien (3) legger til DAG 3 som event!
    plass = 1
    forrige_poengsum = 0
    forrige_plassering = 0
    for x in rekkefølge_nick:           # Ett nick om gangen
        NickID      = x[0]
        Nick        = x[1]
        URL_nick    = x[2]
        Poeng       = x[3]
        fil_tabell_data.write('\n    <tr class="Data">')
        if debug == 1:
            print("\n")
            print("--------------- Nytt nick ---------------")
            print(Nick)

        # Er plasseringen delt med flere nick, eller ikke?
        if forrige_poengsum == Poeng:                    # Delt plassering
            html_nick = f"""
        <td class="Data pl_kolonne delt">
            {forrige_plassering}
        </td>"""

        else:                                           # Ny plassering
            forrige_poengsum = Poeng
            forrige_plassering = plass
            html_nick = f"""
        <td class="Data pl_kolonne">
            {plass}
        </td>"""

        fil_tabell_data.write(html_nick)



        

        # ÅRETS STREBER, Henter alle funn-logger og utlegg for å se om personen er en streber
        SQL_antall_funn = f"""
        SELECT NickID, count(Xmjosnr)
        FROM 
        (
            SELECT NickID, Xmjosnr
            FROM {v.SQL_tabell_Logger}
            WHERE 
                NickID = {NickID} AND
                Loggtype = 'Found it'
            UNION ALL
            SELECT NickID, Xmjosnr
            FROM Utlegg
            WHERE 
                NickID = {NickID} AND 
                (
                    Geocachetype != 'Event' OR
                    Geocachetype IS NULL
                )
        ) t
        """
        DB_cursor.execute(SQL_antall_funn)
        result = DB_cursor.fetchall()
        antall_funnede_cacher = result[0][1]        # Gir tall på hvor mange cacher/utlegg personen har    
        
        # Er geocacheren en streber vil nicket få annen farge her:
        if antall_funnede_cacher >= v.streber_antall_cachefunn:                                    #Hvis geocacheren er streber
            html_nick = f"""
        <td class="Data nick_kolonne nick_rad">
            <strong><a class="streber" href="{URL_nick}">{Nick}</a></strong>
        </td>
        <td class="Data sum_kolonne poeng">
            {Poeng}
        </td>"""
            fil_tabell_data.write(html_nick)
        
        else:                                       #Hvis geocacheren IKKE er en streber
            html_nick = f"""
        <td class="Data nick_kolonne nick_rad">
            <a href="{URL_nick}">{Nick}</a>
        </td>
        <td class="Data sum_kolonne poeng">
            {Poeng}
        </td>"""
            fil_tabell_data.write(html_nick)


        for Xmjosnr,Geocachetype in rekkefølge_utlegg:
            if Geocachetype in "Event":
                event(Xmjosnr)
            else:
                cache(Xmjosnr)


        if i == 0:
            fil_tabell_tittel.write("\n    </tr>")
            fil_cachetype.write("\n    </tr>")
        fil_tabell_data.write("\n    </tr>")
        i=1
        plass += 1


    fil_tabell_tittel.close()
    fil_tabell_data.close()
    fil_cachetype.close()




    # For å lese filen som er opprettet
    # #open and read the file after the appending:
    fil_tabell_tittel   = open(filnavn_tabell_tittel, "r",encoding="utf8")
    fil_tabell_data     = open(filnavn_tabell_data, "r",encoding="utf8")
    fil_cachetype       = open(filnavn_tabell_cachetype, "r",encoding="utf8")
    fil_utlegg          = open(filnavn_utleggs_tabell, "r",encoding="utf8")
    tabell_tittel       = fil_tabell_tittel.read()
    tabell_data         = fil_tabell_data.read()
    tabell_cachetype    = fil_cachetype.read()
    fil_utlegg          = fil_utlegg.read()


    #-- Avslutter filen -------------------------------------------------------------------------------------------------V
    html_footer = f"""
    </table>
    <br>
    <br>
    <center>
        <div class="tabell_box" id="Antall_funn">
            <img src="{v.filnavn_GRAF_antall_funn_per_dag.rsplit("/",1)[1]}" class="tabell_antall_funn_per_cache"></img>
        </div>
    </center>
    <div class="footer"></div>
    </body>
    </html>
    """
    #--------------------------------------------------------------------------------------------------------------------^


    # Setter de ulike filene sammen til ÉN fil
    html = html_header + html_body_start + fil_utlegg + '<table class="Scoreboard">' + tabell_cachetype + tabell_tittel + tabell_data + html_footer
    fil_komplett = open(filnavn_HTML_komplett, "w",encoding="utf8")
    fil_komplett.write(html)

    fil_tabell_tittel.close()
    fil_tabell_data.close()
    fil_komplett.close()
    fil_cachetype.close()
    print("[HTML]   VELLYKKET generering!")


if __name__ == "__main__":
    html_generator(0)