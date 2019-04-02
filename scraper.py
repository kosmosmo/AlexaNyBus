import urllib.request
from bs4 import BeautifulSoup
import collections
import heapq

class Scraper():
    def __init__(self):
        self.stop = {
            "Q27":"https://bustime.mta.info/m/index?q=501369",
            "Q76":"https://bustime.mta.info/m/index?q=502760",
            "Q26":"https://bustime.mta.info/m/index?q=501555",
            "Q17":"https://bustime.mta.info/m/index?q=501333",
            "Q12":"https://bustime.mta.info/m/index?q=500881",
            "Q13":"https://bustime.mta.info/m/index?q=501084"
        }
        self.out = {
            "Q27": 7,
            "Q76": 2,
            "Q26": 3,
            "Q17": 1,
            "Q12": 1,
            "Q13": 1
        }
        self.dest = {
            "flushing":["Q26","Q27"],
            "city":["Q26","Q27","Q76"],
            "test":["Q17","Q12","Q13"]
        }

    def get_soup(self, url, header):
        return BeautifulSoup(urllib.request.urlopen(url), 'html.parser')

    def clean(self,str):
        return str.replace("<strong>", '').replace("</strong>",'').replace("</li>","").replace("<li>","")

    def scraper(self,bus):
        infos = collections.defaultdict(list)
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        url = self.stop[bus]
        soup = self.get_soup(url, header)
        for a in soup.find_all("div", {"class": "directionAtStop"}):
            key = None
            for strong in a.find_all('strong'):
                strong = strong.text.replace('\xa0', ' ')
                key =self.clean(strong).split(' ')[0]
                break
            for li in a.find_all('li'):
                value = self.clean(li.text)
                infos[key].append(value)
        return infos[bus]

    def cal(self,infos,busno):
        res=[]
        for item in infos:
            if "minute" in item:
                info = item.split(",")[0]
                out = int(item.split("minute")[0]) - self.out[busno]
                if out >= 0:
                    res.append([out,busno,info])
        return res

    def destination(self,des):
        heap = []
        for item in self.dest[des]:
            infos = self.scraper(item)
            for jtem in self.cal(infos,item):
                heapq.heappush(heap,jtem)
        return heap
