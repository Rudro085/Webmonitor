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
        
    def get_html(self,url):
        try:
            start = time.time()
            response = requests.get(url,verify=False, headers=self.headers, timeout=5)
            response_time = time.time() - start
            response.raise_for_status() 
            self.status_code = response.status_code
            self.response_html = response.text 
            self.response_time = response_time
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None

    def check_body_tag(self):
        if self.response_html == None:
            return 0
        try:
            soup = BeautifulSoup(self.response_html, 'html.parser')
            if soup.body:
                return 1
            else:
                return 0
        except Exception as e:
            print(f"Error parsing : {e}")
            return 0
        

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
        self.ssl = verify_ssl_certificate(url)
        url = 'http://'+url if self.ssl == 1 else 'https://'+url

        self.get_html(url=url)
        self.description = http_status_codes[self.status_code]
        self.page_exists = self.check_body_tag()
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
        if site[1] == None:
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











