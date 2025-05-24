import sqlite3
import time
import requests
from bs4 import BeautifulSoup, Tag
from modules.http_code import http_status_codes
from modules.ssl_verification import verify_ssl_certificate
from modules.browser_check import browser_check

class Bot:
    def __init__(self):
        self.headers = {
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
        self.status_code = 0
        self.description = 'N/A'
        self.ssl = None
        self.response_time = None
        self.browser_status = None
        self.page_exists = 0
        self.header_text = '-'
        self.dom_score = 0
        self.overall_score = 0
        self.response_html = None
        self.time = None

    def cleanup_url(self, url):
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



    def reset(self):
        self.status_code = 0
        self.description = 'N/A'
        self.ssl = None
        self.response_time = None
        self.page_exists = 0
        self.browser_status = None
        self.header_text = '-'
        self.dom_score = 0
        self.overall_score = 0
        self.response_html = None
        self.time = None
        
    def get_html(self,url):
        http_url = 'http://'+url
        https_urls = 'https://'+url

        try:
            start = time.time()
            https_response = requests.get(https_urls, verify=False, headers=self.headers, timeout=5)
            self.response_time = time.time() - start
            #https_response.raise_for_status()
            self.status_code = https_response.status_code
            self.ssl = True
            self.response_html = https_response.text
        except:
            self.ssl = False
            try:
                start = time.time()
                http_response = requests.get(http_url,verify=False, headers=self.headers, timeout=5)
                self.response_time = time.time() - start
                self.status_code = http_response.status_code
                self.response_html = https_response.text
            except:
                status_code = 0


    def is_valid_html(self):
        """
        Extensive HTML response validator.
        Returns True if the page is a valid webpage (not error/blank), else False.
        """
        html = self.response_html
        if not html or not isinstance(html, str):
            return False

        # Check for HTTP error status codes


        # Check for minimal HTML structure
        soup = BeautifulSoup(html, 'html.parser')
        if not soup.find():  # No tags found
            return False

        # Check for <html> and <body> tags
        if not soup.html or not soup.body or not soup.head:
            return False

        # Check for common error keywords in title or body
        error_keywords = [
            "404", "not found", "error", "forbidden", "unavailable", "bad gateway","nginx",
            "service unavailable", "server not found",
            "internal server error", "502", "503", "504", "problem loading page",
            "site can't be reached", "connection timed out", "maintenance", "server error"
        ]
        title = (soup.title.string or "").lower() if soup.title else ""
        body_text = soup.body.get_text(separator=' ', strip=True).lower() if soup.body else ""

        for keyword in error_keywords:
            if keyword in title or body_text:
                return False

        # Check if the page is not blank (has some visible text)
        visible_text = body_text.strip()
        if len(visible_text) < 30:  # Arbitrary threshold for "blank" pages
            return False

        return True
        

    def get_dom_structure(self):
        if self.response_html == None:
            return 0
        try:
            soup = BeautifulSoup(self.response_html, 'html.parser')
        

            all_tags = soup.find_all()
            self.dom_score = len(all_tags)
            
            print(f"Total tags found: {self.dom_score}")
            

            tag_counts = {}
            for tag in all_tags:
                tag_name = tag.name
                tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1
            
            print("\nTag distribution:")
            for tag, count in sorted(tag_counts.items()):
                print(f"{tag}: {count}")
            
            return self.dom_score
        except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None

            
        
    def get_score(self):
        OK = 1. if self.status_code >= 200 and self.status_code < 400 else 0.
        return  int((OK + self.page_exists + self.dom_score/1500.)*100./3.0)
        
    def run(self,url):

        
        self.reset()
        url = self.cleanup_url(url)
        #self.ssl = verify_ssl_certificate(url)
        #url = 'http://'+url if self.ssl == 1 else 'https://'+url

        self.get_html(url=url)
        self.description = http_status_codes[self.status_code]
        self.page_exists = self.is_valid_html()
        self.browser_status = browser_check(url = url)
        self.get_dom_structure()
        if not self.dom_score == 0 :
            self.page_exists = 1 
        self.overall_score = self.get_score()
        #return [self.status_code,self.description,self.response_time,self.page_exists,self.dom_score,self.overall_score]



if __name__ == '__main__':
    bot = Bot()
    conn = sqlite3.Connection('main.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM sites')
    sites = cur.fetchall()
    for site in sites:
        if site[1] == None or True:
            try:
                bot.run(site[0])
                cur.execute('''UPDATE sites SET 
                            Status_code = ?,
                            Description = ?,
                            SSL = ?,
                            Response_time = ?,
                            Browser_status =?,
                            Page_exists = ?,
                            Tag_count = ?,
                            Score = ? 
                            WHERE Domain = ?''', (
                                bot.status_code,
                                bot.description,
                                bot.ssl,
                                bot.response_time,
                                bot.browser_status,
                                bot.page_exists,
                                bot.dom_score,
                                bot.overall_score,
                                site[0])
                                )
                conn.commit()
            except:
                pass
