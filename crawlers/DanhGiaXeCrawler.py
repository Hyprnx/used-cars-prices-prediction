from crawlers.crawler import Crawler
from bs4 import BeautifulSoup
from base import BaseClass
from common.text_normalizer import normalized
from common.normalize_price import replace_all
import json
import requests
from common.check_file_empty import is_file_empty
from time import sleep
from schema.validate import ValidateUsedCars
from common.headers import HEADERS

class DanhGiaXeCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.source = 'https://www.danhgiaxe.com/'
        self.source_list = [self.source + 'danh-gia-pg' + str(i) for i in range(1, 67)]
        self.review_list = []


    def get_review_links(self):
        for source in self.source_list:
            self.log.info('Crawling %s' % source)
            req = requests.get(self.source, headers=HEADERS).text
            soup = BeautifulSoup(req, 'lxml')
            container_selector = 'body > main > div > div > div.col.m9.l7 > div > div > div.list-review > ul'
            container = soup.select(container_selector)[0]
            li_list = container.find_all('li')
            for li in li_list:
                a = li.find('a')['href']
                self.review_list.append(self.source + a)




