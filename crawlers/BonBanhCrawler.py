#  Copyright 2022. Nguyen Thanh Tuan, To Duc Anh, Tran Minh Khoa, Duong Thu Phuong, Nguyen Anh Tu, Kieu Son Tung, Nguyen Son Tung
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from crawlers.crawler import Crawler
from bs4 import BeautifulSoup
from base import BaseClass
from common.text_normalizer import normalized
from common.normalize_price import replace_all
from common.check_os import get_selenium_chrome_webdriver_path
import json
import requests
from common.check_file_empty import is_file_empty
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from schema.validate import ValidateUsedCars
from common.headers import HEADERS


class BonBanhUsedCarCrawler(BaseClass):
    def __init__(self, url, session):
        super().__init__()
        self.url = url
        self.log.info('Crawling %s' % self.url)
        req = session.get(self.url, headers=HEADERS).text
        self.soup = BeautifulSoup(req, 'lxml')

    def _replace_all(self, text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    def _extract_name_and_price(self, name):
        # price in name, so pass in name
        billion = 'Tỷ'
        million = 'Triệu'
        container = name.split('-')
        price = container[-1][1:]
        price = price.replace(billion, '1000000000')
        price = price.replace(million, '1000000')
        price = price.split(' ')
        price = [i for i in price if i]
        price = [int(i) for i in price]
        try:
            price = price[0] * price[1] + price[2] * price[3]
        except IndexError:
            price = price[0] * price[1]
        name_container = normalized(container[0])
        name = name_container[3:]
        return name, price

    def _extract_origin(self, origin_container):
        replacer = {
            'Nhập khẩu': 'imported',
            'nhập khẩu': 'imported',
            'Lắp ráp trong nước': 'domestic'
        }
        origin = self._replace_all(origin_container, replacer)
        return origin

    def _extract_transmission(self, transmission_container):
        replacer = {
            'Số tự động': 'automatic',
            'Số tay': 'manual'
        }
        origin = self._replace_all(transmission_container, replacer)
        return origin

    def _normalize_km_driven(self, km_driven):
        return int(km_driven.replace(',', ""))

    def _normalize_fuels(self, fuels):
        replacer = {
            'Xăng': 'gasoline',
            'Dầu': 'diesel',
            'Diesel': 'diesel',
            'Hybrid': 'hybrid',
            'Điện': 'electric'
        }
        fuels = self._replace_all(fuels, replacer)

        return fuels

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

    def normalize_type(self, type):
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
            'wagon': 'wagon'
        }
        type = replace_all(replacer, type)

        return type

    def _get_model(self):
        selector = '.breadcrum > span:nth-child(4) > a:nth-child(1) > span:nth-child(1) > strong:nth-child(1)'
        return self.soup.select(selector)[0].text

    def extract(self):
        try:
            name_selector = '#car_detail > div.title > h1'
            name_container = self.soup.select(name_selector)[0].text
            container_selector = '#mail_parent > div.txt_input > span'
            container = self.soup.select(container_selector)
            origin = self._extract_origin(container[0].text)
            km_driven = self._normalize_km_driven(container[3].text.split(" ")[0])
            external_color = container[4].text
            internal_color = container[5].text
            seats = int(container[6].text.split(' ')[0])
            fuels_and_engine_capacity_container = container[7].text.split("\t")
            fuels = self._normalize_fuels(fuels_and_engine_capacity_container[0])
            engine_capacity = float(fuels_and_engine_capacity_container[1].split(' ')[0])
            transmission = self._extract_transmission(container[9].text)
            wheel_drive = container[10].text.split(' ')[0].replace('RFD', "RWD")
            name, price = self._extract_name_and_price(name_container)
            year_selector = '#wrapper > div.breadcrum > span:nth-child(6) > b > i'
            year_container = self.soup.select(year_selector)[0].text
            year = int(year_container.split(' ')[-1])
            type = container[2].text
            brand = self._get_brand(name)
            model = self._get_model()
            car = {
                'name': name,
                'model': model,
                'source_url': self.url,
                'origin': origin,
                'km_driven': km_driven,
                'external_color': external_color,
                'internal_color': internal_color,
                'seats': seats,
                'fuels': fuels,
                'engine_capacity': engine_capacity,
                'transmission': transmission,
                'wheel_drive': wheel_drive,
                'price': price,
                'year': year,
                'type': self.normalize_type(type),
                'brand': brand
            }
            sleep(0.4)
            return car
        except BaseException as e:
            self.log.info(e)
            return {'car_failed': None}


class BonBanhCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.path = get_selenium_chrome_webdriver_path()
        options = Options()
        options.headless = True
        self.log.info('Initializing Selenium')
        self.driver = Chrome(executable_path=self.path, options=options)
        self.url = 'https://bonbanh.com/'
        self.source = 'https://bonbanh.com/'
        self.log.info('Connecting to %s' % self.source)
        self.driver.get(self.url)
        self.s = requests.session()
        req = self.driver.page_source
        self.soup = BeautifulSoup(req, 'lxml')

    def _get_brand(self):
        file_path = 'data/bonbanh/bonbanh_brands_link.txt'
        self.log.info('Trying to open brands file at %s' % file_path)
        if is_file_empty(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                self.log.info('File is empty, crawling brands...')
                selector = '#primary-nav'
                brands = []
                transparent_brands_container = self.soup.select(selector)[0].find_all('li',
                                                                                      attrs={'class': "menuparent",
                                                                                             'style': "z-index:999;"})
                hidden_brands_container = self.soup.select(selector)[0].find_all('li',
                                                                                 attrs={'class': "menuparent add_menu"})
                for brand_container in transparent_brands_container:
                    brand = brand_container.find('a')['href']
                    brands.append(self.source + brand)
                for brand_container in hidden_brands_container:
                    brand = brand_container.find('span')['url']
                    brands.append(self.source + brand)
                file.write('\n'.join(brands))
                return brands
        self.log.info('Successfully opened file, getting brands from file')
        with open(file_path, 'r', encoding='utf-8') as file:
            brands = file.readlines()
            return brands

    def _check_black_list(self, link):
        black_list = [
            'https://bonbanh.com/oto/brilliance',
            'https://bonbanh.com/oto/datsun',
            'https://bonbanh.com/oto/gaz',
            'https://bonbanh.com/oto/lada',
            'https://bonbanh.com/oto/maybach',
            'https://bonbanh.com/oto/mercury',
            'https://bonbanh.com/oto/pontiac',
            'https://bonbanh.com/oto/rover'
        ]  # brands that have no cars selling

        validate_link = link.split('\n')[0]
        return validate_link in black_list

    def _get_cars_link(self):
        file_path = 'data/bonbanh/bonbanh_cars_links.txt'
        self.log.info('Trying to open brands file at %s' % file_path)
        if is_file_empty(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                self.log.info('File is empty, crawling brands...')
                used_car_links = []
                links = self._get_brand()
                for link in links:
                    if self._check_black_list(link):
                        self.log.info('skipping link in blacklist %s' % link)
                        continue
                    self.log.info("Getting used car's links from %s" % link)
                    self.driver.get(link)
                    req = self.driver.page_source
                    soup = BeautifulSoup(req, 'html.parser')
                    try:
                        last_page_selector = '#s-list-car > div > div.pagging > div.navpage > div'
                        last_page_container = soup.select(last_page_selector)[0]
                        last_page_container = last_page_container.find_all('span')
                        link = link.split('\n')[0]
                        last_page = int(last_page_container[-1]['url'][len(link + '/page,'):])
                        pages = [link + '/page,' + str(i) for i in range(1, last_page + 1)]
                    except KeyError:
                        pages = [link]
                    for link in pages:
                        self.log.info("Getting used car's links from %s" % link)
                        # append car's links to list
                        req = requests.get(link, headers=HEADERS).text
                        soup = BeautifulSoup(req, 'lxml')
                        table_container_selector = '#s-list-car > div > ul'
                        table = soup.select(table_container_selector)[0]
                        lis_tag = table.find_all('li', attrs={'itemtype': "http://schema.org/Car"})
                        for li_tag in lis_tag:
                            a_tag = li_tag.find('a')['href']
                            print(self.source + a_tag)
                            used_car_links.append(self.source + a_tag)
                        sleep(1)

                file.write('\n'.join(used_car_links))
                return used_car_links

        self.log.info('Successfully opened file, getting cars links from file')
        with open(file_path, 'r', encoding='utf-8') as file:
            cars_links = file.readlines()
            return cars_links

    def crawl(self):
        validator = ValidateUsedCars()
        self.log.info('Successfully initiate validator')
        cars_links = self._get_cars_link()
        json_file_path = 'data/bonbanh/bonbanh_used_cars.json'
        self.log.info('Trying to open brands file at %s' % json_file_path)
        if is_file_empty(json_file_path):
            self.log.info(f'File at {json_file_path}, is empty, crawling...')
            with open(json_file_path, 'w', encoding='utf-8') as file:
                # cars_links = cars_links[:10]    # test with first 10 cars
                i = 0
                for i in range(len(cars_links)):
                    if i % 100 == 0:
                        self.log.info(f'Crawled {i}')
                        successful_item_length = len(self.crawled_items)
                        failed_item_length = len(self.failed_item)
                        perf = successful_item_length / (successful_item_length + failed_item_length + 1) * 100
                        failed_perf = 100 - perf
                        self.log.info(f'Successful: {successful_item_length}, took: {perf} %')
                        self.log.info(f'Failed: {failed_item_length}, took: {failed_perf} %')
                        sleep(5)
                    url = cars_links[i].split('\n')[0]
                    try:
                        car = BonBanhUsedCarCrawler(url, self.s).extract()
                    except TimeoutError:
                        sleep(10)
                        self.log.info('TIME OUT TIME OUT TIME OUT')
                        car = BonBanhUsedCarCrawler(url).extract()
                    validate_result = validator.validate(car)
                    if validate_result[0]:
                        self.crawled_items.append(car)
                    else:
                        self.failed_item.append(car)
                        self.log.info(validate_result)
                    i += 1

                json.dump(self.crawled_items, file, indent=4, ensure_ascii=False)
                failed_item_path = 'data/bonbanh/bonbanh_failed_items.json'
                with open(failed_item_path, 'w', encoding='utf-8') as failed_file:
                    json.dump(self.failed_item, failed_file, indent=4, ensure_ascii=False)
                return self.crawled_items, self.failed_item

        self.log.info('Successfully opened file, returning cars json from file')
        with open(json_file_path, 'r', encoding='utf-8') as file:
            cars = json.load(file)
        with open('data/bonbanh/bonbanh_failed_items.json', 'r', encoding='utf-8') as failfile:
            failed_cars = json.load(failfile)
            return cars, failed_cars

    def soup(self):
        return self.soup().prettify()


def main():
    cr = BonBanhCrawler()
    car = cr.crawl()
    print(len(car[0]))
    print(len(car[1]))


if __name__ == '__main__':
    main()
