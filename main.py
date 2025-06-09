from playwright.sync_api import sync_playwright
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import datetime
import os
import pytz

timezone = pytz.timezone('America/Sao_Paulo')

# Diretório de download para GitHub Actions
download_dir = "/tmp"

# Cria o diretório, se não existir
os.makedirs(download_dir, exist_ok=True)

def login(page):
    page.goto("https://spx.shopee.com.br/")
    page.wait_for_selector('xpath=//*[@placeholder="Ops ID"]', timeout=15000)
    page.fill('xpath=//*[@placeholder="Ops ID"]', 'Ops34139')
    page.fill('xpath=//*[@placeholder="Senha"]', '@Shopee1234')
    page.click('xpath=/html/body/div[1]/div/div[2]/div/div/div[1]/div[3]/form/div/div/button')

    page.wait_for_timeout(15000)
    try:
        page.click('css=.ssc-dialog-close', timeout=5000)
    except:
        print("Nenhum pop-up foi encontrado.")
        page.keyboard.press("Escape")

def get_data(page):
    data = []
    try:
        # Primeiro link
        page.goto("https://spx.shopee.com.br/#/dashboard/facility-soc/historical-data")
        page.wait_for_selector('xpath=//*[@id="mgmt-dashboard-content"]/div/div/div[2]/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/canvas', timeout=45000)
        first_value = page.inner_text('xpath=/html/body/div[1]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[3]/div[2]/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div/div/div/table/tbody/tr[2]/td[25]')
        data.append(first_value)
     

    except Exception as e:
        print(f"Erro ao coletar dados: {e}")
        raise
    return data

def update_google_sheets(data):
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("hxh.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1R1Ywt_8SuT3X154l1dS30NJEP-JZgoWzH-oq4bOJld0/edit?gid=0#gid=0').worksheet("Python")

    # Copiar o valor da célula AH5 para B61
    value_to_copy = report_sheet.acell('AE5').value
    report_sheet.update('B55', [[value_to_copy]])  # Atualiza B61 com o valor da célula AH5


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            login(page)
            data = get_data(page)
            update_google_sheets(data)
            print("Dados atualizados com sucesso.")

        except Exception as e:
            print(f"Erro durante o processo: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
