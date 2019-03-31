import urllib.request
from bs4 import BeautifulSoup
import collections
import unidecode

class Scraper():
    def __init__(self):
        self.infos = collections.defaultdict(list)

    def get_soup(self, url, header):
        return BeautifulSoup(urllib.request.urlopen(url), 'html.parser')

    def clean(self,str):
        return str.replace("<strong>", '').replace("</strong>",'').replace("</li>","").replace("<li>","")

    def scraper(self,url):
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = self.get_soup(url, header)
        for a in soup.find_all("div", {"class": "directionAtStop"}):
            key = None
            for strong in a.find_all('strong'):
                key = unidecode.unidecode(self.clean(strong.text)).split(' ')[0]
                break
            for li in a.find_all('li'):
                value = unidecode.unidecode(self.clean(li.text))
                self.infos[key].append(value)
        return self.infos

a = Scraper()
print (a.scraper("https://bustime.mta.info/m/index;jsessionid=3A3F4616CB3ABC38C9966CB25698DA09?q=501680"))