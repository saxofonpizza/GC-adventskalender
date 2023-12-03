# Dette skriptet kan kjøres på en windows-maskin med Google Chrome installert.
# Maskinen må ha tilgang til xmjos-databasen!

import mariadb as mariaDB
import os.path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import functions as func

# Lage database-forbindelse
try:
    mariaDB_connection, DB_cursor = func.database_connection()
    
except:
    print("Kan ikke finne databasen!")
    exit()


publiserte_cacher=[]
publiserte_cacher_streng="''"
filnavn_publiserte_cacher = r"publiserte_cacher.txt"
eksisterer_fil_publiserte_cacher=os.path.isfile(filnavn_publiserte_cacher)

if eksisterer_fil_publiserte_cacher == True:
    fil_publiserte_cacher=open(filnavn_publiserte_cacher, "r",encoding="utf8")
    publiserte_cacher=fil_publiserte_cacher.read().split("\n")
    fil_publiserte_cacher.close()
    publiserte_cacher_streng=",".join(publiserte_cacher)

    if not publiserte_cacher_streng:        # Er strengen tom?
        publiserte_cacher_streng = "''"
        eksisterer_fil_publiserte_cacher=False

sql = f"""
SELECT Xmjosnr,GCkode
FROM Utlegg
WHERE 
    Xmjosnr NOT IN ({publiserte_cacher_streng}) AND
    (
        Geocachetype != 'Event' OR
        Geocachetype IS NULL
    ) AND
    Publisert IS NOT NULL
    """

DB_cursor.execute(sql)
result = DB_cursor.fetchall()

for x in result:
    URL_cache=f"https://coord.info/{x[1]}"

    
    # LEGG CACHE TIL WATCHLIST
    sql = f"""
    SELECT Verdi
    FROM settings
    WHERE Variabel='cookie_gspkauth'
    """
    DB_cursor.execute(sql)
    cookie_gspkauth = DB_cursor.fetchone()[0]

    cookie_CookieConsent    = '{stamp:%271CtlSsUPhzZvTyXXL9YBMsaL2weIO8PrhPNa7+52HVlkRS4sVpGcVw==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:3%2Cutc:1695676040196%2Cregion:%27no%27}'

    s = Service(f'{os.path.dirname(__file__)}\..\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=s)

    driver.get(URL_cache)

    # Add Cookies
    driver.add_cookie({"name": "CookieConsent", "value": cookie_CookieConsent})
    driver.add_cookie({"name": "gspkauth", "value": cookie_gspkauth})
    driver.refresh()


    # watchlist = driver.find_element(by=By.ID, value="watchlistLinkMount")
    watchlist = driver.find_element(by=By.ID, value="ctl00_ContentBody_GeoNav_uxWatchlistBtn")
    time.sleep(3)
    watchlist.click()
    time.sleep(1)


    # Noter ned at cachen er lagt til watchlist
    fil_publiserte_cacher = open(filnavn_publiserte_cacher, "a",encoding="utf8")
    
    if eksisterer_fil_publiserte_cacher == False:
        fil_publiserte_cacher.write(f"{x[0]}")
        eksisterer_fil_publiserte_cacher=True
    else:
        fil_publiserte_cacher.write(f"\n{x[0]}")    
    fil_publiserte_cacher.close()