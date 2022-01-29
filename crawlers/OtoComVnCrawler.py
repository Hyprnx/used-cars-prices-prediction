from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from base import BaseClass
from crawlers.crawler import Crawler
from common.normalize_price import replace_all
from common.check_file_empty import is_file_empty
import json


class OtoComVnUsedCarCrawler(BaseClass):
    def __init__(self, url):
        super().__init__()
        self.url = url
        # self.log.info('Crawling %s' % self.url)
        req = requests.get(self.url)
        content = req.content
        self.soup = BeautifulSoup(content.decode('utf-8', 'ignore'), 'html.parser')

    def _replace_all(self, text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    def _price_process(self, price):
        new_price = price.replace('.', '')
        return int(new_price)

    def _extract_origin(self, origin):
        if origin == 'Trong nước':
            origin = 'domestic'
        else:
            origin = 'imported'
        return origin

    def _extract_transmission(self, transmission):
        replacer = {
            'Số tự động': 'automatic',
            'Số tay': 'manual',
            'Số hỗn hợp': 'semi-automatic'
        }
        try:
            transmission = self._replace_all(transmission, replacer)
        except:
            pass
        return transmission

    def _extract_fuels(self, fuels):
        replacer = {
            'Xăng': 'gasoline',
            'Dầu': 'diesel',
            'Diesel': 'diesel',
            'Hybrid': 'hybrid',
            'Điện': 'electric'
        }
        try:
            fuels = self._replace_all(fuels, replacer)
        except:
            pass

        return fuels

    def _normalize_type(self, type):
        type = type.lower()
        replacer = {
            'crossover': 'crossover',
            'suv': 'suv',
            'sedan': 'sedan',
            'convertible/cabriolet': 'convertible',
            'coupe': 'coupe',
            'hatchback': 'hatchback',
            'van/minivan': 'van',
            'bán tải / pickup': 'pickup',
            'pick-up truck': 'pickup',
            'truck': 'pickup',
            'city car': 'hatchback',
            'wagon': 'wagon',
        }
        type = replace_all(replacer, type)

        return type

    def _get_brand(self, name):
        brand = name.split(' ')[0]
        replacer = {
            'rolls': 'rolls_royce',
            'alfa': 'alfa_romeo',
            'aston': 'aston_martin',
            'mercedes': 'mercedes_benz'
        }
        for old, new in replacer.items():
            name = name.replace(old, new)

        return brand

    def _remove_words(self, text):
        list = ['Năm sản xuất', 'Kiểu dáng', 'Tình trạng', 'Xuất xứ', 'Số km đã đi', 'Tỉnh thành', 'Hộp số',
                'Nhiên liệu']
        for i in list:
            text = text.replace(i, '')
        return text

    def extract(self):
        car = {}

        box_detail = self.soup.find('div', class_='box-detail-listing', id='box-detail')

        price = box_detail.find('input', id='price')['value']
        seats = box_detail.find('input', id='numberOfSeat')['value']

        car['price'] = price
        car['source_url'] = self.url
        car['seats'] = seats

        group_title_detail = self.soup.find('div', class_='group-title-detail')
        name = group_title_detail.find('h1').string
        car['brand'] = name.split()[0]
        car['name'] = name.split()[1]

        box_info_detail = self.soup.find('div', class_='box-info-detail')
        li = box_info_detail.find_all('li')
        info = []

        for l in li:
            txt = self._remove_words(l.text.strip())
            info.append(txt)

        if len(txt) == 8:
            keys = ['year', 'type', 'condition', 'origin', 'km_driven',
                    'city', 'transmission', 'fuels']

            for i in range(8):
                car[keys[i]] = info[i]

        else:
            keys = ['year', 'type', 'condition', 'origin', 'km_driven',
                    'city', 'transmission']

            for i in range(7):
                car[keys[i]] = info[i]

            car['fuels'] = 'gasoline'

        car = self._normalize_all(car)

        return car

    def _normalize_all(self, car):
        car['price'] = int(car['price'])
        car['origin'] = self._extract_origin(car['origin'])
        car['transmission'] = self._extract_transmission(car['transmission'])
        car['fuels'] = self._extract_fuels(car['fuels'])
        car['km_driven'] = int(car['km_driven'].split()[0].replace('.', ''))
        car['seats'] = int(car['seats'])
        car['type'] = self._normalize_type(car['type'])
        car['brand'] = self._get_brand(car['brand'])
        # car.pop('city')
        car.pop('condition')

        return car


class OtoComVnCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://oto.com.vn'

    def get_brand_link(self):
        brand_ls = ['toyota', 'hyundai', 'vinfast', 'kia', 'ford', 'mazda', 'honda', 'mercedes-benz', 'mitsubishi', 'suzuki', 'peugeot', 'bmw', 'nissan', 'audi', 'porsche', 'landrover', 'lexus']

        brand_url_ls = ['https://oto.com.vn/mua-ban-xe-{}-cu-da-qua-su-dung'.format(brand) for brand in brand_ls]

        return brand_url_ls

    def crawl_href(self, brand_url):
        car_url_ls = []
        self.log.info('Crawling {}...'.format(brand_url))
        for i in range(1, 102):
            url = '{}/p{}'.format(brand_url, i)

            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'html.parser')
            box_list_car = soup.find('div', class_='box-list-car')
            item_cars = box_list_car.find_all('div', class_=re.compile(r'item-car'))

            for item in item_cars:
                href = item.find('a')['href']
                link = '{}{}'.format(self.base_url, href)
                # print(link)
                car_url_ls.append(link)

        return car_url_ls

    def add_href_txt(self, car_url_ls):
        file_path = 'data/otocomvn/href.txt'

        if is_file_empty(file_path):
            self.log.info('Initializing and Adding href links into text file')
            txt_file = open(file_path, 'w+')
            txt_file.write('\n'.join(car_url_ls))
            txt_file.close()
        else:
            self.log.info('Adding href links into text file')
            txt_file = open(file_path, 'a')
            txt_file.write('\n'.join(car_url_ls))
            txt_file.close()

    def crawl_add_href(self):
        brand_url_ls = self.get_brand_link()
        for brand_url in brand_url_ls:
            car_url_ls = self.crawl_href(brand_url)
            self.add_href_txt(car_url_ls)

    def crawl_add_car(self):
        with open('data/otocomvn/href.txt') as f:
            urls = f.readlines()

        output = []
        failed_cars = []

        for url in urls:
            url = url.split('\n')[0]
            try:
                car = OtoComVnUsedCarCrawler(url).extract()
                print(car)

                output.append(car)

            except:
                # self.log.info('URL NOT OK')
                print(url)
                failed_cars.append(url)

        self.log.info('Adding data into json file...')

        with open('data/otocomvn/otocomvn_used_car.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

        with open('data/otocomvn/otocomvn_failed_used_car.json', 'w', encoding='utf-8') as f:
            json.dump(failed_cars, f, ensure_ascii=False, indent=4)


def main():

    crawl = OtoComVnCrawler()
    crawl.crawl_add_href()
    crawl.crawl_add_car()

if __name__ == '__main__':
    main()
