@REM OPPDATERER SKRIPTENE SOM BENYTTES I KONTEINEREN
@REM Da slipper man å bygge xmjos på nytt
@REM Gjør så æøå kan benyttes i filpath
chcp 65001


@REM Kopier alt i SKRIPT-mappen til containerfiles/SKRIPT og DB/known_hosts til containerfiles
xcopy /yq SKRIPT\* containerfiles\SKRIPT\