from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import shutil

# Diretório de download para GitHub Actions
download_dir = "/tmp"

# Cria o diretório, se não existir
os.makedirs(download_dir, exist_ok=True)

# Configurações do Chrome para ambiente headless do GitHub Actions
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Configurações de download
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Inicializa o driver
driver = webdriver.Chrome(options=chrome_options)

def login(driver):
    driver.get("https://spx.shopee.com.br/")
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@placeholder="Ops ID"]')))
        driver.find_element(By.XPATH, '//*[@placeholder="Ops ID"]').send_keys('Ops35683')
        driver.find_element(By.XPATH, '//*[@placeholder="Senha"]').send_keys('@Shopee123')
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[1]/div[3]/form/div/div/button'))
        ).click()

        time.sleep(15)
        try:
            popup = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ssc-dialog-close"))
            )
            popup.click()
        except:
            print("Nenhum pop-up foi encontrado.")
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    except Exception as e:
        print(f"Erro no login: {e}")
        driver.quit()
        raise


def get_data(driver):
    try:
        driver.get("https://spx.shopee.com.br/#/orderTracking")
        time.sleep(8)


    except Exception as e:
        print(f"Erro ao coletar dados: {e}")
        driver.quit()
        raise

def main():
    try:
        login(driver)
        get_data(driver)
        print("Download finalizado com sucesso.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
