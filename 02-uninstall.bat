@REM AVINSTALLASJON AV PROGRAM
@REM Avinstallerer IKKE docker-volumes som benyttes!

@REM Gjør så æøå kan benyttes i filpath
chcp 65001

@REM "Root"-mappe for X-mjøs programmet
set WORKDIR=%cd%
@REM set WORKDIR=C:\Users\olekr\OneDrive\Ole-Kristian\Fritid\Geocaching\X-Mjøs\Egne script\


@REM Setter opp docker-konteinerne
docker compose -f "%WORKDIR%\docker-compose.yml" down


@REM Lager regel på at et skript kjøres hvert x minutt.
schtasks.exe /Delete /TN "X-MJØS updater" /F

@REM Sletter containerfiles-mappen
@REM rmdir /Q /S ./containerfiles


pause