# Watchlist
__Innholdsfortegnelse__
* [Installasjon](#Installasjon)
* [Avinstallasjon](#Avinstallasjon)
* [Krav](#Krav)
* [Test om WATCHLIST fungerer](#Test-om-WATCHLIST-fungerer)
* [Kjøring av skript](#Kjøring-av-skript)




## Installasjon
Skriptet bør kjøres ofte for å sjekke om en ny geocache er blitt publisert. For at dette skal skje bør det opprettes en oppgave i Windows sitt program "Oppgaveplanlegging / Task Scheduler". Dette kan gjøres ved å kjøre skriptet [01-install.bat](./01-install.bat). Denne kjører også en rask test for å se om watchlist har det den trenger for å fungere på maskinen.

### Konfigurasjon
Databaseforbindelsen må konfigureres. Dette gjøres i filen [functions.py](./functions.py). Der settes:
* brukeren
* passordet
* database-serveren
* database-porten
* databasen

## Avinstallasjon
For å fjerne den automatiske kjøringen fra Oppgaveplanleggingen kan skriptet [02-uninstall.bat](./02-uninstall.bat) kjøres.

## Krav
[watchlist.py](./watchlist.py)-skriptet legger publiserte geocacher som tilhører kalenderen til watchlist!

Skriptet [watchlist.py](./watchlist.py) må kjøres på Windows maskin, og trenger python, med "mariadb" og "selenium" bibliotekene.
Disse kan lastes ned med:

`pip install mariadb selenium`

## Test om WATCHLIST fungerer
Kjør `python dependencies_tester.py`. Denne vil gi info om Windows-maskinen har det den trenger av program, bibliotek og variabler for at [watchlist.py](./watchlist.py) skal fungere! Testen bør alltid gjøres ved bruk av watchlist på ny maskin, og for feilsøking hvis [watchlist.py](./watchlist.py) ikke fungerer.

## Kjøring av skript
Når [watchlist.py](./watchlist.py) kjøres, vil den se etter publiserte cacher i xmjos-databasen. Hvis den finner en publisert cache vil den sette den på watchlist. Da legges X-Mjøs-nummeret til i filen publiserte_cacher.txt *(Denne filen opprettes ved kjøring av [watchlist.py](./watchlist.py) og en cache har blitt publisert)*.
Når cachen er lagt til i publiserte_cacher.txt, vil denne cachen ignoreres av [watchlist.py](./watchlist.py) ettersom den allerede er lagt til watchlist. Med andre ord, vil X-Mjøs-nummerne som ligger i publiserte_cacher.txt bli ignorert av [watchlist.py](./watchlist.py)

