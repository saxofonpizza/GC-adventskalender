import mariadb as mariaDB
import variabler as v
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import functions as func

# Lage database-forbindelse
try:
    mariaDB_connection, DB_cursor = func.database_connection()
    
except:
    print("Kan ikke finne databasen!")
    exit()


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

driver.get("#LENKE_TIL_GEOCACHE")

# Add Cookies
driver.add_cookie({"name": "CookieConsent", "value": cookie_CookieConsent})
driver.add_cookie({"name": "gspkauth", "value": cookie_gspkauth})
driver.refresh()


# watchlist = driver.find_element(by=By.ID, value="watchlistLinkMount")
watchlist = driver.find_element(by=By.ID, value="ctl00_ContentBody_GeoNav_uxWatchlistBtn")
time.sleep(3)
watchlist.click()
time.sleep(1)