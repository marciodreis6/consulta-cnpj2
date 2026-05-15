from playwright.sync_api import sync_playwright
import re
import time
import random

def consultar_sintegra(cnpj):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        page = browser.new_page()

        # ABRE O SITE
        page.goto(
            "https://portal.sefaz.ba.gov.br/scripts/cadastro/cadastroBa/consultaBa.asp"
        )

        # ESPERA CARREGAR
        page.wait_for_load_state("networkidle")

        # DIGITA O CNPJ
        page.fill('input[name="cnpj"]', cnpj)

        # DELAY HUMANO
        time.sleep(random.uniform(1, 2))

        # CLICA CONSULTAR
        page.click('input[type="submit"]')

        # ESPERA RESULTADO
        page.wait_for_load_state("networkidle")

        # PEGA HTML
        html = page.content()

        browser.close()

    # TRANSFORMA EM MAIÚSCULO
    html_upper = html.upper()

    # PROCURA A SITUAÇÃO CADASTRAL
    match = re.search(
        r"SITUAÇÃO CADASTRAL VIGENTE:\s*([A-Z]+)",
        html_upper
    )

    if match:

        status = match.group(1)

        if status == "ATIVO":
            return "ATIVO"

        elif status == "INAPTO":
            return "INAPTO"

        elif status == "SUSPENSO":
            return "SUSPENSO"

        elif status == "BAIXADO":
            return "BAIXADO"

        else:
            return status

    return "VERIFICAR"
