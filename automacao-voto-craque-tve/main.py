from datetime import datetime
from driver_downloader import ChromedriverDownloader
from selenium_wrapper import SeleniumWrapper
from browser import Browser
from logger import Logger
from time import sleep

TARGET_URL = "https://tve.ba.gov.br/craque"

def showOutputMessage(self, message="", notime=False):
  
    if ">>>" in message:
        notime=True

    if notime:
        dtime = ''
    else:
        dtime = f'[{datetime.now().strftime("%H:%M:%S")}]'
    
    message = f'{dtime} {message}'
    if ">>>" in message:
        message = f"\n\n{message}\n\n"
    
def main():
    logger = Logger()
    browser = Browser(ChromedriverDownloader(), logger, "edge")
    driver = browser.create_browser_instance()
    seleniumWrapper = SeleniumWrapper(logger, driver)

    xpath_vote_button = "/html/body/main/div[2]/div/div[9]/div/div/form/button"

    showOutputMessage(">>> Carregando site da votação..")
    seleniumWrapper.get_page(TARGET_URL)
    sleep(6)

    votes_count = 0

    while True:

        showOutputMessage(">>> Iniciando votação...")

        vote_result = vote(seleniumWrapper, xpath_vote_button)
        if vote_result:
            votes_count += 1
            showOutputMessage("Voto realizado com sucesso!")
            showOutputMessage(f"Votos realizados: {votes_count}") 
            showOutputMessage("Aguardando 20s, para continuar..")           
            sleep(20)
            driver.refresh()
            sleep(5)
            continue

        showOutputMessage("Falha ao votar! Aguardando 30s")
        driver.refresh()
        sleep(30)

def vote(seleniumWrapper, xpath_vote_button):
    xpath_confirm_button = "/html/body/div/div/div[6]/button[1]"
    clicked = seleniumWrapper.interact_with_default_selenium_click(xpath_vote_button)
    if clicked:
        clicked = seleniumWrapper.interact_with_default_selenium_click(xpath_confirm_button)
        if clicked:
            return True
    return False

if __name__ == "__main__":
    main()