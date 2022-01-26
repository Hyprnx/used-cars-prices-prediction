from crawlers.crawler import Crawler
from bs4 import BeautifulSoup
from base import BaseClass
from common.text_normalizer import normalized
from common.normalize_price import replace_all
import json
import requests
from common.check_file_empty import is_file_empty
from pprint import pprint
import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from schema.validate import ValidateUsedCars
from common.headers import HEADERS





class GiaXeHoiCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.source = [f'https://giaxehoi.vn/api/car/'+ str(i) +'/variant' for i in range(1,252)]
        self.cars = {}

    def _normalize_origin(self, origin_code):
        if not origin_code:
            return None
        if origin_code == 2:
            return 'domestic'
        else:
            return 'imported'

    def normalize_wheeldrive(self, wheeldrive):
        if not wheeldrive:
            return None
        replacer = {
            '1': 'FWD',
            '2': 'RWD',
            '3': '4WD',
            '4': 'AWD',
            '5': 'AWD'
        }
        wheeldrive = replace_all(replacer, wheeldrive)
        return wheeldrive

    def normalize_type(self, body_type):
        if not body_type:
            return None
        replacer = {
            '1': 'hatchback',
            '2': 'sedan',
            '3': 'cuv',
            '4': 'mpv',
            '5': 'suv',
            '6': 'pickup',
            '7': 'coupe',
            '8': "convertible",
            '9': "others",
            '10': 'others',
            '20': 'others'
        }
        body_type = replace_all(replacer, body_type)
        return body_type

    def normalize_engine_cap(self, engine_cap):
        if not engine_cap:
            return None
        engine_cap = replace_all({',': "", '.': ''}, engine_cap)
        return int(engine_cap)

    def normalize_transmission(self, transmission):
        if not transmission:
            return None
        replacer = {
            '1': 'manual',
            '2': 'automatic',
            '3': 'automatic',
            '4': 'automatic',
            '5': 'others'
        }
        transmission = replace_all(replacer, transmission)
        return transmission

    def normalize_fuels(self, fuels):
        if not fuels:
            return None
        replacer = {
            '1': 'gasoline',
            '2': 'diesel',
            '3': 'hybrid',
            '4': 'electric',
            '5': 'others'
        }
        fuels = replace_all(replacer, fuels)
        return fuels

    def normalize_year(self, year):
        return int(year) if year else None

    def extract(self, url):
        res = requests.get(url, headers=HEADERS).json()
        for i in range(len(res) - 1):
            reference_url = 'https://giaxehoi.vn/js/selector.js?ver=1.8.9'
            metadata = res[i]
            name = res[i]['full_name']
            self.log.info('Getting infomation from %s' %name)
            model = res[i]['car']
            brand = res[i]['car_brand']
            info = res[i]['info']
            year = self.normalize_year(res[i]['launched_year'])
            origin = self._normalize_origin(res[i]['origin'])
            type_ = self.normalize_type(str(res[i]['body_type']))
            transmission = self.normalize_transmission(info['specs_engine']['transmission'])
            seats = info['specs_dimension']['seats']
            doors = info['specs_dimension']['doors']
            wheel_drive = self.normalize_wheeldrive(info['specs_chassis']['drivetrain'])
            engine_capacity = self.normalize_engine_cap(info['specs_engine']['capacity'])
            self.cars[name] = {'name': name,
                                 'origin': origin,
                                 'type': type_,
                                 'seats': seats,
                                 'doors': doors,
                                 'source': url,
                                 'transmission': transmission,
                                 'wheel_drive': wheel_drive,
                                 'year': year,
                                 'model': model,
                                 'brand': brand,
                                 'engine_capacity': engine_capacity,
                                 'metadata_reference': reference_url,
                                 'metadata': metadata}


    def crawl(self):
        path = 'cars_infomation/giaxehoi_com/car_data.json'
        if is_file_empty(path):
            with open(path, mode='w', encoding='utf-8') as file:
                for link in self.source:
                    res = self.extract(link)
                json.dump(self.cars, file, indent=4, ensure_ascii=False)
                return self.cars

        with open(path, 'r', encoding='utf-8') as file:
            self.cars = json.load(file)
            return self.cars

def main():
    crwlr = GiaXeHoiCrawler()
    res = crwlr.crawl()
    print(len(res))

if __name__ == '__main__':
    main()

