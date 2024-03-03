from bs4 import BeautifulSoup as bs
from time import sleep
from random import random
import undetected_chromedriver as uc


class GoogleSearch:
    def __init__(self):
        self.browser = uc.Chrome()
    
    def search(self, query, n_pages=1, time_sleep=0, random_sleep=False, a=10, b=10):
        results = []
        for page in range(n_pages):
            url = f"https://www.google.com/search?q={'+'.join(query.split(' '))}"+f"&start={10*(page-1)}" 
            self.browser.get(url)
        
            soup = bs(self.browser.page_source, 'html.parser')
            for result in soup.find_all('div', class_="yuRUbf"):
                results.append(result.a.get("href"))
            
            if random_sleep:
                sleep(a+b*random())
            else:
                sleep(time_sleep)
        
        return results
    
    def end(self):
        self.browser.close()
        self.browser.quit()