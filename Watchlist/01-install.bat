@echo off
@REM Gjør så æøå kan benyttes i filpath
chcp 65001

@REM "Root"-mappe for Watchlist-programmet
set WORKDIR=%cd%

python dependencies_tester.py

@REM Lag 05-run.ps1 for at Oppgaveplanleggeren skal ha skript å kjøre
echo cd %WORKDIR% > 05-run.ps1
echo python watchlist.py >> 05-run.ps1


@REM @REM Lager regel på at et skript kjøres hvert 5. minutt.
echo.
echo Setter opp automatisk kjøring av skript
schtasks.exe /Create ^
/SC MINUTE ^
/MO 5 ^
/ST 00:03 ^
/ED 07/12/2023 ^
/TN "X-MJØS Watchlist" ^
/TR %windir%\system32\WindowsPowerShell\v1.0\powershell.exe" -windowstyle hidden -File '%WORKDIR%\05-run.ps1'" ^
/f  
echo Ferdig
echo.


pause