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
options.add_argument('--ignore-ssl-errors=yes')

#options.add_argument("--headless") #execute le navigateur en arriere plan 

# Initialisation du navigateur Chrome
driver = webdriver.Chrome(service=service_obj, options=options)
#driver.maximize_window()

# Accès à la page Web
driver.get("https://coinmarketcap.com/currencies/bitcoin/historical-data/")

# Création et écriture des en-têtes dans le fichier CSV
with open("btc_historical_data.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["count", "date", "price_open", "price_high",
                     "price_low", "price_close", "volume", "market_cap"])


# Configuration de l'attente explicite
wait = WebDriverWait(driver,20)
load_more = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[2]/div/div[2]/div/div/div[2]/div/p[1]/button")))
driver.execute_script("arguments[0].scrollIntoView();", load_more)

#pour load le data complet 
while (load_more):
        try:

            # Tenter de localiser le bouton "Load More"
            load_more.click()
            print("click done ")  
        except:
            # Si le bouton n'est plus trouvé, on sort de la boucle
            print("Le bouton 'Load More' n'est plus visible. Toutes les données ont été chargées.")
            break


table_of_data = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='history']/div[2]/table/tbody/tr")))
print(len(table_of_data))

def get_btc_info():
    for index, row in enumerate(table_of_data, start=1):
        try:
            # Utilisation de wait pour chaque cellule dans la ligne
            date = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[1]"))).text
            price_open = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[2]"))).text
            price_high = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[3]"))).text
            price_low = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[4]"))).text
            price_close = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[5]"))).text
            volume = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[6]"))).text
            market_cap = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='history']/div[2]/table/tbody/tr[{index}]/td[7]"))).text

            # Affichage des données extraites
            #print(f" Ligne {index} : Date= {date}, Open= {price_open}, High= {price_high}, Low= {price_low}, Close= {price_close}, Volume= {volume}, Market Cap= {market_cap}")
            btcDataList = [
                 index,
                 date,
                 price_open,
                 price_high,
                 price_low,
                 price_close,
                 volume,
                 market_cap
            ]

            with open("btc_historical_data.csv", "a", newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(btcDataList)

            print(btcDataList)

        except Exception as e:
            print(f"Erreur dans la ligne {index} : {e}")

get_btc_info()