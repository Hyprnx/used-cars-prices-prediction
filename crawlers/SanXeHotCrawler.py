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
from common.normalize_price import normalize_price
from common.headers import HEADERS

path = 'data/sanxehot'


class SanXeHotCrawler(BaseClass):
    def __init__(self):
        super().__init__()
        self.df = pd.read_json(path + '/sanxehot_links.json').T
        self.car_df = pd.DataFrame(columns=['name', 'brand', 'source_url', 'type', 'origin', 'km_driven',
                                            'external_color', 'seats', 'engine_capacity', 'fuels',
                                            'transmission', 'wheel_drive', 'price', 'year'])

    def crawl(self):
        for i in range(0, len(self.df)):
            url = self.df.iloc[i]['url']
            type = self.df.iloc[i]['type']
            self.log.info('Crawling %s', url)
            req = requests.get(url, headers=HEADERS).text
            soup = BeautifulSoup(req, 'lxml')
            body_page = soup.find('table', class_='info').tbody
            car_feature = body_page.find_all('td')

            gia = car_feature[0].text
            gia = gia.replace(',', '.')
            price = normalize_price(gia)

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

            self.car_df = self.car_df.append(pd.Series({'name': name, 'brand': None, 'source_url': url, 'type': type,
                                                        'origin': origin, 'km_driven': km_driven,
                                                        'external_color': external_color,
                                                        'seats': None, 'engine_capacity': engine_capacity,
                                                        'fuels': fuels,
                                                        'transmission': transmission, 'wheel_drive': None,
                                                        'price': price, 'year': year}), ignore_index=True)

        return self.car_df


def main():
    cars = SanXeHotCrawler().crawl()
    cars.to_csv(path + '/sanxehot_detail.csv')


if __name__ == '__main__':
    main()