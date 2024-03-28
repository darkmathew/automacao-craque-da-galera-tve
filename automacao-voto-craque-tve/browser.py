# -*- coding: UTF-8 -*-
from subprocess import PIPE, Popen
from os import environ, getenv
from time import sleep
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium import webdriver
from logger import Logger
from driver_downloader import ChromedriverDownloader
from useragents import UserAgent

class Browser:

    def __init__(self, chromeDriverDownloader : ChromedriverDownloader, logger : Logger, browser_selected = "chrome"):
        self.__chrome_driver_downloader = chromeDriverDownloader
        self.__logger : Logger = logger
        self.browserSelected = browser_selected
        self.user_agent = UserAgent().get_user_agent()

        self.subprocessConstructor()
        environ['WDM_LOG_LEVEL'] = '0'

    def subprocessConstructor(self):
        _original_constructor = Popen.__init__
        def _patched_constructor (* args, ** kwargs):
            for key in ('stdin','stdout','stderr'):
                if key not in kwargs:
                    kwargs [key] = PIPE
            return _original_constructor (* args, ** kwargs)
        Popen.__init__ = _patched_constructor

    def create_browser_instance(self) -> webdriver.Chrome | Edge | None:        
        browser, options = self.setup_browser_and_options()        
        options = self.setup_default_arguments(options)

        self.setup_headless(options)
        self.setup_proxy(browser, options)

        attempts = 5
        for attempt in range(attempts):
            try:
                driver = None
                if browser == "chrome":
                    version = self.__chrome_driver_downloader.getBrowserVersion()
                    self.__chrome_driver_downloader.version = version
                    self.__chrome_driver_downloader.check_and_download()
                    driver = webdriver.Chrome(
                        executable_path=getenv('LOCALAPPDATA') + f"\\CSGOEmpireBot\\driver\\chromedriver{version}.exe", 
                        options=options
                    )
                elif browser == "edge":
                    driver = Edge(EdgeChromiumDriverManager(
                            cache_valid_range=7, path=self.__chrome_driver_downloader.folder_path).install(),
                            options=options
                        )                                    
                return driver

            except Exception as e:
                self.__logger.log(Logger.MEDIUM_LEVEL, f"Failed to create browser: {e}")
                if attempt + 1 == attempts:
                    self.__logger.log(Logger.HIGH_LEVEL, f"Failed to create browser after {attempts} attempts.")
                    return None
                sleep(10)
                continue
        return None

    def setup_browser_and_options(self):        
        browser = ""
        if "edge" in self.browserSelected:
            browser = "edge"
            options = EdgeOptions()
        else:
            browser = "chrome"
            options = ChromeOptions()
        return browser, options

    def setup_headless(self, options : ChromeOptions | EdgeOptions):
        return None

    def setup_proxy(self, browser, options : ChromeOptions | EdgeOptions):
        if browser == "chrome":
            options.add_argument("--incognito")

        elif browser == "edge":
            options.add_argument("--inprivate")

    def setup_default_arguments(self, options : ChromeOptions | EdgeOptions):
        options.add_argument("--log-level=3")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-infobars')
        options.add_argument("--mute-audio")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--silent")
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-dev-shm-using")
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--lang=en-US")
        options.add_argument(f'user-agent={self.user_agent}')
        options.add_argument(f"--force-device-scale-factor=0.6")
        options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('prefs', {'credentials_enable_service': False, 'profile': {'password_manager_enabled': False}})  
        options.add_argument("--window-size=1270,768")      
        return options