# INFO
# Dette skriptet endrer poengene som blir gitt til deltagerne basert på reglene vist under!
# Skriptet endrer tabellen som defineres i variabelen "SQL_tabell_Logger_forslag"
# 
#################### Regler ####################
# Funn samme dag                = 5p           #
# Funn dag 2                    = 4p           #
# Funn dag 3                    = 3p           #
# Funn dag 4                    = 2p           #
# Funn dag 5 til 31. desember   = 1p           #
################################################

import mariadb as mariaDB
import variabler as v

# Lage database-forbindelse
try:
    mariaDB_connection = mariaDB.connect(
        user      = v.DB_user,
        password  = v.DB_password,
        host      = "localhost",
        port      = v.DB_port,
        database  = v.DB_database
    )

    # Definere en cursor
    DB_cursor = mariaDB_connection.cursor()
except:
    print("Kan ikke finne databasen!")
    exit()


# Intervall 1
data = f"""
UPDATE {v.SQL_tabell_Logger_forslag}
SET Poeng = {v.Intervall1_poeng}
WHERE
    ((day(Dato_logget) >= Xmjosnr) and (day(Dato_logget) <= Xmjosnr+{v.Intervall1})) and
    Loggtype = "Found it"
"""
DB_cursor.execute(data)


# Intervall 2
data = f"""
UPDATE {v.SQL_tabell_Logger_forslag}
SET Poeng = {v.Intervall2_poeng}
WHERE
    (not (day(Dato_logget) <= Xmjosnr+{v.Intervall1}) and (day(Dato_logget) <= Xmjosnr+{v.Intervall2})) and
    Loggtype = "Found it"
"""
DB_cursor.execute(data)


# Intervall 3
data = f"""
UPDATE {v.SQL_tabell_Logger_forslag}
SET Poeng = {v.Intervall3_poeng}
WHERE
    (not (day(Dato_logget) <= Xmjosnr+{v.Intervall2}) and (day(Dato_logget) <= Xmjosnr+{v.Intervall3})) and
    Loggtype = "Found it"
"""
DB_cursor.execute(data)


# Intervall 4
data = f"""
UPDATE {v.SQL_tabell_Logger_forslag}
SET Poeng = {v.Intervall4_poeng}
WHERE
    (not (day(Dato_logget) <= Xmjosnr+{v.Intervall3}) and (day(Dato_logget) <= Xmjosnr+{v.Intervall4})) and
    Loggtype = "Found it"
"""
DB_cursor.execute(data)


# IntervallSTD
data = f"""
UPDATE {v.SQL_tabell_Logger_forslag}
SET Poeng = {v.IntervallSTD_poeng}
WHERE
    not (day(Dato_logget) <= Xmjosnr+{v.Intervall4}) and
    Loggtype = "Found it"
"""
DB_cursor.execute(data)
mariaDB_connection.commit()