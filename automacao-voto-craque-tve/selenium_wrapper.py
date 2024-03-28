from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from msedge.selenium_tools import Edge

from logger import Logger

class SeleniumWrapper:

    def __init__(self, logger, driver) -> None:

        self._logger = logger
        self._driver : webdriver.Chrome | Edge = driver
    
    def get_page(self, url : str):
        self._driver.get(url)


    def interact_with_default_selenium_click(self, element_xpath : str, timeout : int = 5) -> bool:
        try:
            element = WebDriverWait(self._driver, timeout).until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
            element.click()
            return True
        except TimeoutException as error:
            self._logger.log(Logger.MEDIUM_LEVEL, f"Error when interacting with the element via click: {error}")
            return False

    def interact_with_action_chains(self, element_xpath: str) -> bool:
        try:
            element = self._driver.find_element_by_xpath(element_xpath)
            action = ActionChains(self._driver)
            action.move_to_element(element).perform()
            return True
        except StaleElementReferenceException as e:
            self._logger.log(Logger.MEDIUM_LEVEL, f"Error when interacting with the element via ActionChains: {e}")
            # Tentar encontrar o elemento novamente
            element = self._driver.find_element_by_xpath(element_xpath)
            action = ActionChains(self._driver)
            action.move_to_element(element).perform()
            return True
        except Exception as e:
            self._logger.log(Logger.MEDIUM_LEVEL, f"Error when interacting with the element via ActionChains: {e}")
            return False

    def is_popup_displayed(self, popup_xpath):
        try:
            popup_element = self._driver.find_element_by_xpath(popup_xpath)
            confirmation_element = popup_element.find_element_by_xpath('.//div[contains(text(), "Confirmação de Voto")]')
            return True
        except NoSuchElementException:
            return False
