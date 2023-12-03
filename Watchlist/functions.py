# functions.py innholder funksjoner som benyttes i flere ulike skript!


######################################
#   OPPRETTELSE AV DB-FORBINDELSE    #
######################################
def database_connection ():
    import mariadb as mariaDB

    # Lage database-forbindelse
    try:
        mariaDB_connection = mariaDB.connect(
            user      = 'root',                     # Bruker med r/w-rettigheter i databasen [std:root]
            password  = '1234',                     # Passordet til brukeren                 [std:1234]
            host      = 'localhost',                # IP-adresse til DB-serveren, (localhost) kan benyttes (mariaDB benyttes hvis konteineren kjører skriptene) [std:mariaDB]
            port      =  3305,                      # Port databasen benytter seg av [std:3306]
            database  = 'xmjos'                     # DATABASEN som inneholder alle tabellene [std:xmjos]
        )

        # Definere en cursor
        DB_cursor = mariaDB_connection.cursor()
    except:
        print("[FUNC]   Kan ikke finne databasen!")
        exit()


    return mariaDB_connection, DB_cursor

# ---------------------------------------------------------------------



######################################
#    HENTE VARIABLER FRA DATABASE    #
######################################
def hent_variabler():
    sql = f"""
    SELECT Variabel,Verdi
    FROM settings
    """
    mariaDB_connection, DB_cursor = database_connection()
    DB_cursor.execute(sql)
    sql_data = DB_cursor.fetchall()

    Variabler_dict={}
    for x in sql_data:
        Variabel = x[0]
        Verdi    = x[1]
        Variabler_dict[Variabel] = Verdi

    return Variabler_dict                   #Returnerer en dictionery med [Variabelnavn: Verdi]





Variabler = hent_variabler()
# print(Variabler['tid_oppdatert_poengtabell'])