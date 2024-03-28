# -*- coding: UTF-8 -*-
from os import popen, remove, makedirs, rename, getenv
from os.path import exists, isfile
from requests import get
from requests_cache import disabled
from re import search
from io import BytesIO
from zipfile import ZipFile


class ChromedriverDownloader:
    def __init__(self):
        self.folder_path = getenv('LOCALAPPDATA') + "\\CSGOEmpireBot\\driver\\"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        self.version = None

    def getBrowserVersion(self, navegador='chrome'):

        browser = {
            'edge': r'reg query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Edge\BLBeacon" /v version',
            'chrome': r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        }

        pattern = r'\d+'
        command = browser[navegador]
        stdout = popen(command).read()
        version = search(pattern, stdout)

        if not version:
            raise ValueError(
                f'Versão do chrome não pôde ser obtida com o comando {command}')

        version = version.group(0)
        version = int(version)
        self.version = version
        return version

    def check_local(self):
        if exists(self.folder_path) is False:
            makedirs(self.folder_path)

        if exists(f'./{self.folder_path}/chromedriver.zip'):
            remove(f'./{self.folder_path}/chromedriver.zip')

        if isfile(f'{self.folder_path}/chromedriver{self.version}.exe'):
            return True

        else:
            return False

    def download(self, navegador):
        if navegador == 'chrome':
            last_version = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{self.version}"
            last_version = get(last_version, timeout=50)
            last_version = last_version.text
            API_URL = f"https://chromedriver.storage.googleapis.com/{last_version}/chromedriver_win32.zip"

        elif navegador == 'edge':
            last_version = f"https://msedgedriver.azureedge.net/LATEST_STABLE_{self.version}"
            last_version = get(last_version, timeout=50)
            last_version = last_version.text
            API_URL = f"https://msedgedriver.azureedge.net/{self.version}/edgedriver_win32.zip"

        mem_zip_file = BytesIO()

        with disabled():
            file = get(API_URL, headers=self.headers)

            if (file.headers.get('content-type')) == "application/zip":
                mem_zip_file.write(file.content)

        with ZipFile(mem_zip_file, 'r') as zipObj:
            zipObj.extractall(self.folder_path)

        rename(self.folder_path + 'chromedriver.exe',
                  self.folder_path + 'chromedriver' + str(self.version) + '.exe')


    def check_and_download(self, browser='chrome'):
        user_version = self.getBrowserVersion(browser)
        if user_version != self.version or not self.check_local():
            self.download(browser)
