import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

class SitemapFinder:
    def __init__(self, base_url):
        self.base_url = base_url if base_url.startswith('http') else 'http://' + base_url
        self.visited_sitemaps = set()
        self.all_urls = set()

    def fetch_sitemap(self, url):
        try:
            print(f"Fetching: {url}")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.content
            else:
                print(f"Failed to fetch sitemap: {response.status_code}")
        except Exception as e:
            print(f"Exception: {e}")
        return None

    def parse_sitemap(self, content):
        try:
            root = ET.fromstring(content)
            namespace = {'ns': root.tag.split('}')[0].strip('{')}

            # If it's a sitemap index (nested sitemaps)
            if root.tag.endswith("sitemapindex"):
                for sitemap in root.findall("ns:sitemap", namespace):
                    loc = sitemap.find("ns:loc", namespace).text
                    if loc not in self.visited_sitemaps:
                        self.visited_sitemaps.add(loc)
                        self.process_sitemap(loc)
            # It's a regular URL sitemap
            elif root.tag.endswith("urlset"):
                for url in root.findall("ns:url", namespace):
                    loc = url.find("ns:loc", namespace).text
                    self.all_urls.add(loc)
        except ET.ParseError:
            print("Failed to parse XML sitemap.")

    def process_sitemap(self, sitemap_url):
        content = self.fetch_sitemap(sitemap_url)
        if content:
            self.parse_sitemap(content)

    def run(self):
        root_sitemap = urljoin(self.base_url, '/sitemap.xml')
        self.process_sitemap(root_sitemap)
        print(f"\n✅ Total URLs Found: {len(self.all_urls)}")
        return list(self.all_urls)

if __name__ == '__main__':
    site = 'https://pbi.gov.bd'
    finder = SitemapFinder(site)
    urls = finder.run()
    for url in urls:
        print(url)
