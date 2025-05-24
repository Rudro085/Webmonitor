from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
import sqlite3

def browser_check(url, timeout=50):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment to run headless

    chromedriver_path = os.path.join( 'chromedriver', 'chromedriver.exe') #os.path.dirname(__file__), '..',
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:

        driver.set_page_load_timeout(timeout)
        driver.get(url)
        title = driver.title
        body = driver.find_element("tag name", "body").text
        if title and body:
            #print(f"[OK] {url} - Title: {title}")
            return True
        else:
            #print(f"[EMPTY] {url} - Website loaded but appears empty.")
            return False
    except (WebDriverException, TimeoutException) as e:
        #print(f"[FAIL] {url} - Selenium failed to open the site: {e}")
        return False
