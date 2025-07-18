import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from urllib.parse import urljoin, urlparse
header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',  # Do Not Track
            'Referer': 'https://www.google.com/',
        }
# Initialize SQLite database
conn = sqlite3.connect('gov_websites.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS websites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE
    )
''')
conn.commit()

visited = set()

def cleanup_url( url):
        """
        Removes 'http://', 'https://', and 'www.' from the beginning of the URL.
        """
        if url.startswith('http://'):
            url = url[len('http://'):]
        elif url.startswith('https://'):
            url = url[len('https://'):]
        if url.startswith('www.'):
            url = url[len('www.'):]
        return url

def is_gov_bd_link(url):
    """Check if the URL belongs to the .gov.bd domain."""
    return re.match(r'^https?://(?:www\.)?.+\.gov\.bd', url)

def save_to_db(url):
    """Save the URL to the database."""
    try:
        cursor.execute('INSERT OR IGNORE INTO websites (url) VALUES (?)', (url,))
        conn.commit()
    except Exception as e:
        print(f"Error saving {url} to database: {e}")

def scrape_links(url):
    """Recursively scrape .gov.bd links from the given URL."""
    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url,verify=False, timeout=5)
        if response.status_code != 200:
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(url, a_tag['href'])
            parsed_link = urlparse(link)
            # Normalize the URL
            normalized_link = f"{parsed_link.scheme}://{parsed_link.netloc}"
            #normalized_link = cleanup_url(normalized_link)
            if is_gov_bd_link(normalized_link) and normalized_link not in visited:
                save_to_db(cleanup_url(normalized_link))
                scrape_links(normalized_link)
    except Exception as e:
        print(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    root_url = "https://bangladesh.gov.bd/index.php"  # Replace with the root .gov.bd website
    scrape_links(root_url)
    print("Scraping completed. Saved websites:")
    for row in cursor.execute('SELECT url FROM websites'):
        print(row[0])

conn.close()