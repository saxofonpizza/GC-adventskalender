import functions as func

# Testing av dependencies. Denne kan kjøres når som helst og vil ikke endre/ødelegge noe! (non-destructive script)
Avstand_status = 50


##############################################
#           Nødvendige libraries             #
##############################################
print("Bibliotek-krav:")
libraries = (
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