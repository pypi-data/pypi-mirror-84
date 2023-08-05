import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib.parse import parse_qs, urlparse

class ImageDown:
    KEYWORD = ''
    LIMIT = 5

    def __init__(self, keyword, limit = 5):
        chromedriver_autoinstaller.install()
        self.KEYWORD = keyword
        self.LIMIT = limit
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")      

        self.DRIVER = webdriver.Chrome(options=chrome_options)
        self.DRIVER.get(f'https://www.google.com/search?q={keyword}&tbm=isch')

    def get_urls(self, baslangic = 1):
        urls = []
        for i in range(baslangic, (self.LIMIT + 1)):
            if i == (self.LIMIT + 1):
                break

            try:
                Div = self.DRIVER.find_element(
                        By.XPATH, f'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[{i}]/a[1]'
                    )
                
                Click = ActionChains(self.DRIVER)
                Click.context_click(Div).perform()
                url = parse_qs(urlparse(Div.get_attribute('href')).query)['imgurl'][0]
                urls.append(url)
            except NoSuchElementException:
                break
        return urls
