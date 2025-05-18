import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from urllib.parse import urljoin, urlparse

class Database:
    def __init__(self, db_name='gov_websites.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS websites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE
            )
        ''')
        self.conn.commit()

    def save_url(self, url):
        try:
            self.cursor.execute('INSERT OR IGNORE INTO websites (url) VALUES (?)', (url,))
            self.conn.commit()
        except Exception as e:
            print(f"Error saving {url} to database: {e}")

    def close(self):
        self.conn.close()

def is_gov_bd_link(url):
    # Accepts both http and https, with or without www, and any subdomain
    return re.match(r'^https?://(?:[\w\-]+\.)*gov\.bd', url)

visited_urls = set()
saved_domains = set()

def get_main_domain(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def scrape_links(url, db):
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        main_domain = get_main_domain(url)
        if is_gov_bd_link(main_domain) and main_domain not in saved_domains:
            db.save_url(main_domain)
            saved_domains.add(main_domain)
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(url, a_tag['href'])
            # Remove URL fragments and normalize
            link = link.split('#')[0]
            link = link.rstrip('/')
            if is_gov_bd_link(link):
                scrape_links(link, db)
    except Exception as e:
        print(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    root_url = "https://crt.sh/?q=%25.gov.bd/"  # Replace with any known .gov.bd root
    db = Database()
    scrape_links(root_url, db)
    print("Scraping completed. Saved websites:")
    for row in db.cursor.execute('SELECT url FROM websites'):
        print(row[0])
    db.close()