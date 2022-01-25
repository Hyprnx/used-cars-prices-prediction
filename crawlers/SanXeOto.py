from base import BaseClass
from common.check_file_empty import is_file_empty
from common.normalize_price import replace_all
from common.headers import HEADERS
from crawlers.crawler import Crawler
from schema.validate import ValidateUsedCars
import json
import requests
from bs4 import BeautifulSoup


class SanXeOtoExtractor(BaseClass):
    def __init__(self, source_url):
        super().__init__()
        self.source = 'https://sanxeoto.com/'
        self.source_url = source_url.split('\n')[0]
        self.log.info('Crawling %s' %self.source_url)
        req = requests.get(self.source_url, headers=HEADERS).text
        self.soup = BeautifulSoup(req, 'lxml')
        self.css_selector = {
            'name': '#chi-tiet-xe > main > div.main-detail > div > div > div.col-xl.wrap-productDetail > div.info-product > h1',
            'brand': '#chi-tiet-xe > main > div.main-detail > div > ul > li:nth-child(2) > a > span',
            'model': '#chi-tiet-xe > main > div.main-detail > div > ul > li:nth-child(3) > a > span',
            'type': '#chi-tiet-xe > main > div.main-detail > div > ul > li:nth-child(4) > a > span',
            'origin': '#chi-tiet-xe > main > div.main-detail > div > div > div.col-xl.wrap-productDetail > div.content-wrap > div:nth-child(1) > div.content-body > ul.ileft > li:nth-child(2) > i',
            'km_driven': '#chi-tiet-xe > main > div.main-detail > div > div > div.col-xl.wrap-productDetail > div.content-wrap > div:nth-child(1) > div.content-body > ul.iright > li:nth-child(4) > i',
            'external_color': '#chi-tiet-xe > main > div.main-detail > div > div > div.col-xl.wrap-productDetail > div.content-wrap > div:nth-child(1) > div.content-body > ul.iright > li:nth-child(1) > i',
            'seats': '#CarsMaxSeating',
            'fuels_and_engine_capacity': '#chi-tiet-xe > main > div.main-detail > div > div > div.col-xl.wrap-productDetail > div.content-wrap > div:nth-child(1) > div.content-body > ul.ileft > li:nth-child(3) > i',
            'transmission': '#chi-tiet-xe > main > div.main-detail > div > div > div.col-xl.wrap-productDetail > div.content-wrap > div:nth-child(1) > div.content-body > ul.ileft > li:nth-child(4) > i',
            'wheel_drive': '#chi-tiet-xe > main > div.main-detail > div > div > div.col-xl.wrap-productDetail > div.content-wrap > div:nth-child(4) > div > div > div:nth-child(3) > div > p',
            'price': '#chi-tiet-xe > main > div.main-detail > div > div > div.col-xl.wrap-productDetail > div.info-product > div.row > div.col-lg-6.col-12.thongtin > div.priceCar > strong',
            'year'

        }

    def get_name(self):
        selector =
