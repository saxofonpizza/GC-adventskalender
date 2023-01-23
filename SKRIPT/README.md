# README-fil for SKRIPT
**Innhold**
1. [Beskrivelse av skript](#1-beskrivelse-av-skript)
2. [FORSLAG TIL XMJØS](#2-forslag-til-xmjøs)
3. [Info](#3-info)

Denne mappen inneholder alle skript som benyttes. Det meste er pythonskript. 

<br>
<br>
<br>


## 1. Beskrivelse av skript
Skriptene er fordelt over flere filer med ulik funksjonalitet. Skriptene er:
* [variabler.py](#variablerpy)
* [main.py](#mainpy)
* [mail.py](#mailpy)
* [Prosessering.py](#prosesseringpy)
* [HTML_gen.py](#html_genpy)
* [diagram.py](#diagrampy)

<br>
<br>

### variabler.py
Denne filen inneholder ulike variabler som kan endres for å tilpasse adventskalenderen best mulig. Dette er blant annet påloggingsinformasjon til epost-servere, sftp-server osv. I tillegg kan antall poeng som gis for funn på samme dag, andre dag, tredje dag osv endres.

Kjøres dette skriptet direkte, vil ingen ting skje!
<br>
<br>

### main.py
Dette skriptet starter alt, og importerer nødvendige skript.
<br>
<br>

### mail.py
Dette skriptet henter mails fra en IMAP-server og laster ned innholdet(payloaden). Dette skriptet henter også ut viktige nøkkelpunkter i mailen som nicknames, dato logget, nummer på geocachen osv.

Kjøres dette skriptet direkte vil det være mulig å lagre mails i innboksen som en HTML-fil. I tillegg er det mulig å liste alle mapper i mailboksen.
<br>
<br>

### Prosessering.py
Dette skriptet sjekker nøkkelpunktene som kommer fra mail-skriptet og tildeler riktig poeng til hver logg før det legges til i databasen. Dette skriptet inneholder derfor mange databasespørringer som oppdaterer databasen!

Kjøres dette skriptet direkte, vil ingen ting skje!
<br>
<br>

### HTML_gen.py
Dette skriptet lager en HTML-side basert på data som ligger i databasen. HTML-filen som lages lastes opp til en SFTP-server for publisering på nett.

Hvis dette skriptet kjøres direkte, vil HTML-filen opprettes. Derfor krever dette skriptet forbindelse med databasen.
<br>
<br>

### diagram.py
Dette skriptet lager diagrammet for "antall funn per cache" og lagrer dette til en .png-fil

Kjøres dette skriptet direkte, vil et test-diagram opprettes!
<br>
<br>
<br>



## 2. FORSLAG TIL XMJØS
Noen filer ender med _forslag.py. Disse filene er noe endret ift. hovedskriptet, men kun små endringer for å tilpasse poenggiving og utseende!

<br>
<br>
<br>


##  3. Info
Denne mappen inneholder spesifikke skript for poengutregning hvor det gis
5 poeng for funn på utleggsdag
4 poeng dagen deretter
3 poeng for funn 2 dager etter utleggsdato
2 poeng for 3. dag
1 poeng resten av desember