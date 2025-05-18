import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from urllib.parse import urljoin, urlparse

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
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(url, a_tag['href'])
            parsed_link = urlparse(link)
            # Normalize the URL
            normalized_link = f"{parsed_link.scheme}://{parsed_link.netloc}"
            if is_gov_bd_link(normalized_link) and normalized_link not in visited:
                save_to_db(normalized_link)
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