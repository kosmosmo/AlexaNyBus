import urllib.request
from bs4 import BeautifulSoup
import collections

class Scraper():
    def __init__(self):
        self.infos = collections.defaultdict(list)
        self.stop = {
            "Q27":"https://bustime.mta.info/m/index?q=501369",
            "Q76":"https://bustime.mta.info/m/index?q=502760",
            "Q26":"https://bustime.mta.info/m/index?q=501555"

        }
        self.dest = {"flushing":["Q26","Q27"]}
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
                strong = strong.text.replace('\xa0', ' ')
                key =self.clean(strong).split(' ')[0]
                break
            for li in a.find_all('li'):
                value = self.clean(li.text)
                self.infos[key].append(value)
        return self.infos

    def destination(self,str):