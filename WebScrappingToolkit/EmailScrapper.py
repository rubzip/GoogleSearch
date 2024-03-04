from bs4 import BeautifulSoup as bs
import requests
import re

def get_main_url(url):
    pattern = r"(?:https\:\/\/)?(?:www\.)?([\w\-]+\.\w+)"
    match = re.search(pattern, url)
    if match is not None:
        return match.group(1)
    else:
        return None

class EmailScrapper:
    def __init__(self, original_url):
        self.original_url = original_url
        self.main_url = get_main_url(original_url)
        self.visited_urls = set()
        self.all_urls = set()
        self.all_emails = set()
        self.max_depth = 20

    def get_all_links(self, soup):
        try:
            for tag in soup.find_all():
                if tag.has_attr("href"):
                    url = tag.get("href")
                    if (get_main_url(url)==self.main_url) and (url not in self.visited_urls):
                        self.all_urls.add(url)
        except Exception as ex:
            print(ex)
    
    def get_all_emails(self, soup):
        pattern = r"([\w\-\.]+\@(?:[\w\-]+\.)+[\w\-]{2,4})"
        content = str(soup.body)
        for email in re.findall(pattern, content):
            self.all_emails.add(email)
    
    def get_content(self, url):
        try:
            request = requests.get(url)
            soup = bs(request.text, features="html.parser")
            return soup
        except Exception as ex:
            print(ex)

    def run(self):
        soup = self.get_content(self.original_url)
        self.get_all_emails(soup)
        self.get_all_links(soup)
        i = 0
        while (len(self.all_urls) > 0) and (i < self.max_depth):
            i += 1
            url = self.all_urls.pop()
            soup = self.get_content(url)
            if soup is not None:
                self.get_all_emails(soup)
                self.get_all_links(soup)            
                self.visited_urls.add(url)