import sqlite3
import time
import requests
from bs4 import BeautifulSoup, Tag
from modules.http_code import http_status_codes

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
        self.response_time = None
        self.page_exists = 0
        self.header_text = '-'
        self.dom_score = 0
        self.overall_score = 0




    def reset(self):
        self.status_code = 0
        self.description = 'N/A'
        self.response_time = None
        self.page_exists = 0
        self.header_text = '-'
        self.dom_score = 0
        self.overall_score = 0
        


    def check_body_tag(self,url):
        try:
            response = requests.get(url,headers=self.headers ,verify=False, timeout=5)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.body:
                return 1
            else:
                return 0
        except Exception as e:
            print(f"Error accessing {url}: {e}")
            return 0
        
        
    def check_uptime(self,url):
        try:
            start = time.time()
            response = requests.get(url,verify=False, headers=self.headers, timeout=5)
            #print(self.validate_html_and_score( response.text))
            response_time = time.time() - start
            return response.status_code, response_time
        except Exception as e:
            return 0, None
    

    def get_html(self,url):
            try:
                response = requests.get(url,headers=self.headers ,verify=False,timeout=5.)
                response.raise_for_status()  
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL: {e}")
                return None
            
    def traverse_dom(self, element, indent=0):

        if isinstance(element, Tag):
            self.dom_score += 1
            print(f"Found tag: {element.name}, DOM score: {self.dom_score}")

            for child in element.children:
                if isinstance(child, Tag):
                    self.traverse_dom(child, indent + 2)

    def get_dom_structure(self, url):

        html_content = self.get_html(url)
        if not html_content:
            print("No HTML content fetched.")
            return 0

        soup = BeautifulSoup(html_content, 'html.parser')
        

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

            
        
    def get_score(self):
        OK = 1. if self.status_code >= 200 and self.status_code < 400 else 0.
        return  int((OK + self.page_exists + self.dom_score/1500.)*100./3.0)
        
    def run(self,url):
        url = 'http://'+ url
        self.reset()
        self.status_code,self.response_time = self.check_uptime(url)
        self.description = http_status_codes[self.status_code]
        self.page_exists = self.check_body_tag(url)
        self.get_dom_structure(url)
        if not self.dom_score == 0 :
            self.page_exists = 1 
        self.overall_score = self.get_score()
        return [self.status_code,self.description,self.response_time,self.page_exists,self.dom_score,self.overall_score]



if __name__ == '__main__':
    bot = Bot()
    conn = sqlite3.Connection('main.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM sites')
    sites = cur.fetchall()
    for site in sites:
        result = bot.run(site[0])
        cur.execute('UPDATE sites SET Status_code = ?,Description = ?,Response_time = ?,Page_exists = ?,Tag_count = ?, Score = ? WHERE Domain = ?', (result[0],result[1],result[2],result[3],result[4],result[5],site[0]))
        conn.commit()











