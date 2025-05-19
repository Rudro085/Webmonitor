from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import os
import sqlite3

def check_website(url, service, chrome_options):
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        title = driver.title
        body = driver.find_element("tag name", "body").text
        driver.quit()
        if title and body:
            print(f"[OK] {url} - Title: {title}")
            return True
        else:
            print(f"[EMPTY] {url} - Website loaded but appears empty.")
            return False
    except WebDriverException as e:
        print(f"[FAIL] {url} - Selenium failed to open the site: {e}")
        return False

if __name__ == '__main__':
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment to run headless

    chromedriver_path = os.path.join(os.path.dirname(__file__), '..', 'chromedriver', 'chromedriver.exe')
    service = Service(executable_path=chromedriver_path)


    conn = sqlite3.Connection('scrapped.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM sites')
    sites = cur.fetchall()
    for site in sites:
        status = check_website("http://"+site[0],service,chrome_options)
        cur.execute('''UPDATE sites SET 
                    SSL = ?
                    WHERE Domain = ?''', (
                        1 if status else 0,
                        site[0])
                        )
        conn.commit()