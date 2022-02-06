import pandas as pd
from crawlers.crawler import Crawler
from bs4 import BeautifulSoup
from base import BaseClass
from common.text_normalizer import normalized
import json
import requests
import os
from pprint import pprint
from schema.validate import ValidateUsedCars

path = '/Users/minhkhoa/Documents/used-cars-prices-prediction/data/sanxehot/'
df = pd.read_json(path + 'sanxehot_links.json').T

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) "
                  "Gecko/20100101 Firefox/46.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0"
}


class SanXeHotCrawler:
    def __init__(self):
        self.df = pd.read_json(path + 'sanxehot_links.json').T

    def crawl(self):
        car_list = {}

        num = 0
        for i in range(401, 801):
            url = df.iloc[i]['url']
            type = df.iloc[i]['type']
            req = requests.get(url, headers=HEADERS).text
            soup = BeautifulSoup(req, 'lxml')
            body_page = soup.find('table', class_='info').tbody
            car_feature = body_page.find_all('td')

            gia = car_feature[0].text
            gia = gia.replace(',', '')
            if 'triệu' in gia:
                price = gia.replace(' triệu', '000000')
            elif 'tỷ' in gia:
                price = gia.replace(' tỷ', '000000')

            name = car_feature[2].text
            year = car_feature[4].text

            km_driven = car_feature[6].text.split()[0]
            km_driven = km_driven.replace('.', '')

            dong_co = car_feature[8].text.split()
            if len(dong_co) == 2:
                fuels = dong_co[0]
                engine_capacity = dong_co[1].split('L')[0]
            else:
                fuels = dong_co[0]
                engine_capacity = None

            transmission = car_feature[10].text
            origin = car_feature[12].text
            external_color = car_feature[14].text

            car_list[num] = {'name': name, 'brand': None, 'source_url': url, 'type': type,
                             'origin': origin, 'km_driven': km_driven,
                             'external_color': external_color,
                             'seats': None, 'engine_capacity': engine_capacity, 'fuels': fuels,
                             'transmission': transmission, 'wheel_drive': None,
                             'price': price, 'year': year}
            num += 1
            print(num)

        return car_list


cars = SanXeHotCrawler().crawl()
with open(path + "cars_detail800.json", "w+") as f:
    f.write(json.dumps(cars, indent=4))
