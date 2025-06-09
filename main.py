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
        d1 = 'SoC_SP_Cravinhos'
        d2 = 'SOC_Received'

        page.goto("https://spx.shopee.com.br/#/orderTracking", timeout=60000)


        # Preenche o primeiro campo
        input1 = page.locator('xpath=/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[6]/form/div[8]/div/span/span[1]/div/div/div/span/input')
        input1.click()
        input1.fill("")  # limpa
        input1.fill("SoC_SP_Cravinhos")
        time.sleep(2)
        # Clica no item da lista suspensa
        page.locator("li.ssc-option[title='SoC_SP_Cravinhos']").first.click()

        # Campo 2
        input2 = page.locator('xpath=/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[6]/form/div[21]/div/span/span[1]/div/div/div/span/input')
        input2.click()
        input2.fill("")
        input2.fill(d2)
        time.sleep(2)
        page.locator('xpath=/html/body/span[7]/div/div/div/ul/li[1]/span/b').click()
        time.sleep(2)
        page.locator('xpath=/html/body/div[1]/div/div[2]/div[1]/div[1]/span[2]/span[1]/span').click()

        # Botão pesquisar
        page.locator('xpath=/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[6]/form/div[25]/button[1]').click()
        time.sleep(4)

        # Captura do dado
        first_value = page.inner_text('xpath=/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[10]/div/div[3]/div/span[1]')
        data.append(first_value)

    except Exception as e:
        print(f"Erro ao coletar dados: {e}")
        raise

    return data

def update_google_sheets(first_value):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("hxh.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_url(
        'https://docs.google.com/spreadsheets/d/1R1Ywt_8SuT3X154l1dS30NJEP-JZgoWzH-oq4bOJld0/edit'
    ).worksheet("Reporte HxH")

    sheet.update('B55', [[first_value]])

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            login(page)
            data = get_data(page)
            if data:
                update_google_sheets(data[0])
                print("Dados atualizados com sucesso.")
            else:
                print("Nenhum dado encontrado.")
        except Exception as e:
            print(f"Erro durante o processo: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
