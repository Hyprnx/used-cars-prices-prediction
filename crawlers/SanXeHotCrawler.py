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


class ExtractSanXeTotLink(BaseClass):
    def __init__(self):
        super().__init__()
        self.prefix = 'https://www.sanxehot.vn'
        self.index = [i for i in range(1, 786)]
        self.url_list = ['https://www.sanxehot.vn/mua-ban-xe/loai-xe-cu-pg' + str(i) for i in self.index]

    def extract_link(self):
        dictionary = {}
        for link in self.url_list:
            self.log.info('Extracting %s' % link)
            req = requests.get(link, headers=HEADERS).text
            soup = BeautifulSoup(req, 'lxml')
            # lis = soup.findAll('li', attrs={'class': 'cars'})
            table_selector = 'body > main > div.section > div > div > div.col.m7.s12 > div > div > section.car > ul'
            lis = soup.select(table_selector)[0].find_all('li')
            li_len = len(lis)
            for i in range(1, li_len + 1):
                link_selector = f'body > main > div.section > div > div > div.col.m7.s12 > div > div > section.car > ul > li:nth-child({i}) > div:nth-child(1) > div.col.m8 > h2 > a'
                link = self.prefix + soup.select(link_selector)[0]['href']

                type_selector = f'body > main > div.section > div > div > div.col.m7.s12 > div > div > section.car > ul > li:nth-child({i}) > div:nth-child(2) > div.col.m8.s12 > table > tbody > tr:nth-child(2) > td'
                type_ = soup.select(type_selector)[0].text

                dictionary[link] = {'url': link,
                                    'type': type_}

        with open(path + "/sanxehot_links.json", "w+", encoding='utf-8') as f:
            f.write(json.dumps(dictionary, indent=4, ensure_ascii=False))


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

        self.car_df.to_csv(path + '/sanxehot_detail.csv')


def main():
    SanXeHotCrawler().crawl()


if __name__ == '__main__':
    main()
