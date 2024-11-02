import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


# Initialisation du service ChromeDriver
service_obj = Service(ChromeDriverManager().install())

# Configuration des options du navigateur
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("detach", True)
#options.add_argument("--") #execute le navigateur en arriere plan 

# Initialisation du navigateur Chrome
driver = webdriver.Chrome(service=service_obj, options=options)
driver.maximize_window()

# Accès à la page Web
driver.get("https://coinmarketcap.com/currencies/bitcoin/historical-data/")

# Configuration de l'attente explicite
wait = WebDriverWait(driver,20)