from typing import Optional

from selenium.common.exceptions import InvalidArgumentException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


def make_driver(headless: Optional[bool] = False):
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--blink-settings=imagesEnabled=false') 
    # 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_experimental_option('prefs', {'download.default_directory': self.results_dir})
    if headless:
        chrome_options.add_argument("headless")
        print('Executando drive no modo headless')
    
    try:
        driver = webdriver.Chrome(options=chrome_options) # type: ignore
        return driver
    except (InvalidArgumentException, TimeoutException, WebDriverException) as e:
        print(f"Error creating WebDriver: {e}")
        return None