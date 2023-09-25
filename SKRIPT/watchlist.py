import mariadb as mariaDB
import variabler as v
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


# Lage database-forbindelse
mariaDB_connection = mariaDB.connect(
    user      = v.DB_user,
    password  = v.DB_password,
    host      = v.DB_host,
    port      = v.DB_port,
    database  = v.DB_database
)

# Definere en cursor
DB_cursor = mariaDB_connection.cursor()


sql = f"""
    SELECT Verdi
    FROM settings
    WHERE Variabel='cookie_gspkauth'
    """
DB_cursor.execute(sql)
cookie_gspkauth = DB_cursor.fetchone()[0]

cookie_CookieConsent    = '{stamp:%271CtlSsUPhzZvTyXXL9YBMsaL2weIO8PrhPNa7+52HVlkRS4sVpGcVw==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:3%2Cutc:1695676040196%2Cregion:%27no%27}'


driver = webdriver.Chrome()

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