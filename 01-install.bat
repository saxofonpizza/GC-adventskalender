@REM INSTALLASJON AV PROGRAM
@REM Gjør så æøå kan benyttes i filpath
chcp 65001

@REM "Root"-mappe for X-mjøs programmet
set WORKDIR=%cd%
@REM set WORKDIR=C:\Users\olekr\OneDrive\Ole-Kristian\Fritid\Geocaching\X-Mjøs\Egne script\

@REM For å tillate kjøring av powershell-script må følgende kommando kjøres som administrator i powershell: "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine"
@REM Dette gjelder kun for de PC-ene som IKKE har Execution-policy satt til RemoteSigned for LocalMachine. Dette kan sjekkes med "Get-ExecutionPolicy -List"

@REM Bygger x-mjos-image
docker build -t xmjos "%WORKDIR%\."

@REM Oppretter nødvedige mapper
if not exist .\containerfiles\ mkdir .\containerfiles\
set mappe=HTML
if not exist .\containerfiles\%mappe% mkdir .\containerfiles\%mappe%
set mappe=LOGS
if not exist .\containerfiles\%mappe% mkdir .\containerfiles\%mappe%

@REM Kopier alt i SKRIPT-mappen til containerfiles/SKRIPT og DB/known_hosts til containerfiles
xcopy /yqe SKRIPT\* containerfiles\SKRIPT\
@REM xcopy /yq DB\known_hosts containerfiles\       @REM !BRUKES FOR pysftp!


@REM Setter opp docker-konteinerne
docker compose -f "%WORKDIR%\docker-compose.yml" up  -d


@REM Lager regel på at et skript kjøres hvert 15. minutt.
schtasks.exe /Create ^
/SC MINUTE ^
/MO 15 ^
/ST 00:03 ^
/ED 07/12/2023 ^
/TN "X-MJØS updater" ^
/TR %windir%\system32\WindowsPowerShell\v1.0\powershell.exe" -windowstyle hidden -File '%WORKDIR%\run\01-registrering.ps1'" ^
/f  

@REM Gjør så Docker åpnes ved oppstart! Egen innstilling i docker Desktop
pause