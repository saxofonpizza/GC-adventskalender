# Kopierer filer til en delt mappe mellom HOSTS-PC og konteineren xmjos
# Dette er for å slippe å bygge imaget på nytt hver gang en endring i skriptene gjøres (KUN FOR DEBUGGINGENS DEL)
# Copy-Item .\SKRIPT\* .\containerfiles\ -Exclude "__pycache__"

# Åpner xmjos-konteineren i et interaktivt cmd/powershell-vindu
# start powershell {docker exec -it $(docker ps -aqf "name=xmjos") bash}
Start-Process cmd -Argument "/c docker exec -it $(docker ps -aqf "name=xmjos") bash"