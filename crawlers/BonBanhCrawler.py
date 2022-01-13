from crawlers.crawler import Crawler
from bs4 import BeautifulSoup
from base import BaseClass
from common.text_normalizer import normalized
import json
import requests
import os
from pprint import pprint
import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from schema.validate import ValidateUsedCars


def is_file_empty(file_path):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty

    return os.path.isfile(file_path) and os.path.getsize(file_path) == 0


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) "
                  "Gecko/20100101 Firefox/46.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0"
}


class BonBanhUsedCarCrawler(BaseClass):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.log.info('Crawling %s' %self.url)
        req = requests.get(self.url, headers=HEADERS).text
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
            price = price[0]* price[1] + price[2]* price[3]
        except IndexError:
            price = price[0] * price[1]
        name_container = normalized(container[0])
        name = name_container[3:]
        return name, price

    def _extract_origin(self, origin_container):
        replacer = {
            'Nhập khẩu': 'imported',
            'Lắp ráp trong nước' : 'domestic'
        }
        origin = self._replace_all(origin_container,replacer)
        return origin

    def _extract_transmission(self, transmission_container):
        replacer = {
            'Số tự động': 'automatic',
            'Số tay' : 'manual'
        }
        origin = self._replace_all(transmission_container,replacer)
        return origin

    def _normalize_km_driven(self, km_driven):
        return int(km_driven.replace(',',""))

    def _normalize_fuels(self, fuels):
        replacer = {
            'Xăng' : 'gasoline',
            'Diesel' : 'diesel',
            'Hybrid' : 'hybrid',
            'Điện': 'electric'
        }
        fuels = self._replace_all(fuels, replacer)

        return fuels

    def extract(self):
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
        wheel_drive = container[10].text.split(' ')[0]
        name, price = self._extract_name_and_price(name_container)
        car = {
            'name' : name,
            'source_url': self.url,
            'origin' : origin,
            'km_driven' : km_driven,
            'external_color': external_color,
            'internal_color': internal_color,
            'seats' : seats,
            'fuels' : fuels,
            'engine_capacity' : engine_capacity,
            'transmission': transmission,
            'wheel_drive': wheel_drive,
            'price': price
        }
        sleep(0.05)
        return car


class BonBanhCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.path = 'C:\\Users\\toduc\\Downloads\\chromedriver_win32\\chromedriver.exe' # change path when use on your machine
        options = Options()
        options.headless = True
        self.log.info('Initializing Selenium')
        self.driver = Chrome(executable_path=self.path, options=options)
        self.url = 'https://bonbanh.com/'
        self.source = 'https://bonbanh.com/'
        self.log.info('Connecting to %s' %self.source)
        self.driver.get(self.url)
        req = self.driver.page_source
        self.soup = BeautifulSoup(req, 'lxml')


    def _get_brand(self):
        file_path = 'data/brands_link.txt'
        self.log.info('Trying to open brands file at %s' %file_path)
        if is_file_empty(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                self.log.info('File is empty, crawling brands...')
                selector = '#primary-nav'
                brands = []
                transparent_brands_container = self.soup.select(selector)[0].find_all('li', attrs={'class':"menuparent", 'style':"z-index:999;"})
                hidden_brands_container = self.soup.select(selector)[0].find_all('li', attrs={'class':"menuparent add_menu"})
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
        file_path = 'data/cars_links.txt'
        self.log.info('Trying to open brands file at %s' %file_path)
        if is_file_empty(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                self.log.info('File is empty, crawling brands...')
                used_car_links = []
                links = self._get_brand()
                for link in links:
                    if self._check_black_list(link):
                        self.log.info('skipping link in blacklist %s' %link)
                        continue
                    self.log.info("Getting used car's links from %s" %link)
                    self.driver.get(link)
                    req = self.driver.page_source
                    soup = BeautifulSoup(req, 'html.parser')
                    try:
                        last_page_selector = '#s-list-car > div > div.pagging > div.navpage > div'
                        last_page_container = soup.select(last_page_selector)[0]
                        last_page_container = last_page_container.find_all('span')
                        link = link.split('\n')[0]
                        last_page = int(last_page_container[-1]['url'][len(link + '/page,'):])
                        pages = [link + '/page,' + str(i) for i in range(1,last_page + 1)]
                    except KeyError:
                        pages = [link]
                    for link in pages:
                        self.log.info("Getting used car's links from %s" %link)
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
        json_file_path = 'data/bonbanh_used_cars.json'
        self.log.info('Trying to open brands file at %s' %json_file_path)
        if is_file_empty(json_file_path):
            self.log.info(f'File at {json_file_path}, is empty, crawling...')
            with open(json_file_path, 'w', encoding='utf-8') as file:
                cars = []
                for i in range(10):
                    url = cars_links[i].split('\n')[0]
                    car = BonBanhUsedCarCrawler(url).extract()
                    # pprint(car)
                    validate_result = validator.validate(car)
                    if validate_result:
                        cars.append(car)

                json.dump(cars, file, indent=4, ensure_ascii=False)
                return cars

        self.log.info('Successfully opened file, returning cars json from file')
        with open(json_file_path, 'r', encoding='utf-8') as file:
            cars = file.readlines()
            return cars

    def soup(self):
        return self.soup().prettify()


def main():
    cr = BonBanhCrawler()
    car = cr.crawl()
    # print(car)
    # print(ValidateUsedCars().validate(car))


if __name__ == '__main__':
    main()