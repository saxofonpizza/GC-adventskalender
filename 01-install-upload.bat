@echo off
@REM INSTALLASJON AV OPPLASTNINGS-PROGRAM
@REM Gjør så æøå kan benyttes i filpath
chcp 65001

@REM "Root"-mappe for X-mjøs programmet
set WORKDIR=%cd%


set skript=run\03-Last_opp_filer.bat
set skript_full_path=%WORKDIR%\%skript%

@REM !!! Lager skriptet for opplasting !!!
@REM  ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
echo @echo off > "%skript%"
echo chcp 65001 >> "%skript%"
echo cd %WORKDIR% >> "%skript%"

@REM Samler alle filene som skal lastes opp til en mappe
echo xcopy /yqe containerfiles\HTML\xmjos-2022.html          .TilOpplastning\ >> "%skript%"
echo xcopy /yqe containerfiles\HTML\xmjos-2022_forslag.html  .TilOpplastning\ >> "%skript%"
echo xcopy /yqe containerfiles\HTML\antall_funn.png          .TilOpplastning\ >> "%skript%"
echo xcopy /yqe containerfiles\LOGS\                         .TilOpplastning\LOGS\ >> "%skript%"

@REM Opplasting til WEBSERVER
echo scp -i PKI\key.priv -o PasswordAuthentication=no -r .TilOpplastning\* cx3zqdiu6_w519073+r519087@ssh.cx3zqdiu6.service.one:/customers/8/a/7/cx3zqdiu6/webroots/r519087/xmjos >> "%skript%"

@REM !!! Her er skriptet ferdig !!!
@REM  ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



@REM Lager regel på at et skript kjøres hvert 15. minutt.
schtasks.exe /Create ^
/SC MINUTE ^
/MO 15 ^
/ST 00:04 ^
/ED 07/12/2023 ^
/TN "X-MJØS uploader" ^
/TR "%skript_full_path%" ^
/f  


@REM Husk å aktiver så Docker åpnes ved oppstart! Egen innstilling i docker Desktop
pause