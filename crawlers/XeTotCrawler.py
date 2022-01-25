from base import BaseClass
from common.text_normalizer import normalized
from common.check_file_empty import is_file_empty
from common.normalize_price import replace_all
from common.headers import HEADERS
from crawlers.crawler import Crawler
from schema.validate import ValidateUsedCars
from pprint import pprint
from time import sleep
import json
import requests
from bs4 import BeautifulSoup

class XeTotUsedCarExtractor(BaseClass):
    def __init__(self,url):
        super().__init__()
        self.url = url.split('\n')[0]
        self.source = 'https://xetot.com'
        self.log.info('Crawling %s' %self.url)
        req = requests.get(self.url, headers=HEADERS).text
        self.soup = BeautifulSoup(req, 'lxml')

    def get_name(self):
        try:
            name_selector = '#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > div.product-gab > h2'
            name_container = self.soup.select(name_selector)[0].text
            name = [text for text in name_container.split('\n') if text][0]
        except BaseException:
            name = 'None'

        return name

    def get_model(self):
        try:
            model_selector = '#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(3) > div.info-show'
            model_container = self.soup.select(model_selector)[0].text
            model = [text for text in model_container.split('\n') if text][0]
        except BaseException:
            model = 'None'
        return model

    def get_transmission(self):
        try:
            selector = '#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(5) > div.info-show'
            container = self.soup.select(selector)[0].text
            tranmission = [text for text in container.split('\n') if text][0]
            replacer = {
                'Tự động': 'automatic',
                'Số sàn': 'manual',
                'Khác': 'None'
            }
            tranmission = replace_all(replacer, tranmission)
        except BaseException:
            tranmission = 'None'
        return tranmission

    def get_brand(self):
        try:
            brand_selector = '#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(1) > div.info-show'
            brand_container = self.soup.select(brand_selector)[0].text
            brand = [text for text in brand_container.split('\n') if text][0]
        except BaseException:
            brand = 'None'
        return brand

    def get_price(self):
        try:
            price_selector = '#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > div.product-gab > div > span'
            price_container = self.soup.select(price_selector)[0].text
            price = int(price_container.split(' ')[0].replace('.',''))
        except BaseException:
            price = 'None'
        return price

    def get_year(self):
        try:
            year_selector = '#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(4) > div.info-show'
            year_container = self.soup.select(year_selector)[0].text
            year = int([text for text in year_container.split('\n') if text][0])
        except BaseException:
            year = 'None'
        return year

    def get_km_driven(self):
        try:
            km_driven_container = '#so-km-da-di'
            km_driven = int(self.soup.select(km_driven_container)[0]['value'])
        except BaseException:
            km_driven = 'None'
        return km_driven

    def get_fuels(self):
        try:
            fuels_selector = '#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(6) > div.info-show'
            fuels_container = self.soup.select(fuels_selector)[0].text
            fuels = [text for text in fuels_container.split('\n') if text][0]
            replacer = {
                'Xăng': 'gasoline',
                'Dầu': 'diesel',
                'Diesel': 'diesel',
                'Hybrid': 'hybrid',
                'Điện': 'electric',
                'Khác': 'NONE'
            }
            fuels = replace_all(replacer, fuels)
        except BaseException:
            fuels = 'None'
        return fuels

    def get_origin(self):
        try:
            origin_selector = '#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(6) > div.info-show'
            origin_container = self.soup.select(origin_selector)[0].text
            origin = [text for text in origin_container.split('\n') if text][0]
            if origin.lower == 'việt nam':
                origin =  'domestic'
            else:
                origin =  'imported'
        except BaseException:
            origin = 'None'

        return origin

    def get_type(self):
        try:
            selector = '#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(8) > div.info-show'
            container = self.soup.select(selector)[0].text
            type = [text for text in container.split('\n') if text][0]
            replacer = {
                'Sedan': 'sedan',
                'SUV / Cross over': 'suv',
                'Hatchback': 'hatchback',
                'Pick-up (bán tải)': 'pickup',
                'Minivan (MPV)': 'van',
                'Van': 'van',
                'Coupe (2 cửa)': 'coupe',
                'Mui trần': 'NONE',
                'Kiểu dáng khác': 'NONE'
            }
            type = replace_all(replacer, type)
        except BaseException:
            type = 'None'
        return type

    def get_seats(self):
        try:
            selector = '#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(9) > div.info-show'
            container = self.soup.select(selector)[0].text
            seats = int([text for text in container.split('\n') if text][0])
        except BaseException:
            seats = 'None'
        return seats

    def get_external_color(self):
        try:
            selector = '#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(10) > div.info-show'
            container = self.soup.select(selector)[0].text
            color = [text for text in container.split('\n') if text][0]
        except BaseException:
            color = 'None'
        return color

    def extract(self):
        car = {
            'name': self.get_name(),
            'brand': self.get_brand(),
            'model': self.get_model(),
            'type': self.get_type(),
            "source": self.source,
            "source_url": self.url,
            'origin': self.get_origin(),
            'km_driven': self.get_km_driven(),
            'external_color': self.get_external_color(),
            'seats': self.get_seats(),
            'fuels': self.get_fuels(),
            'transmission': self.get_transmission(),
            'price': self.get_price(),
            'year': self.get_year()
            }
        return car

class XeTotCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.url = 'https://xetot.com/toan-quoc/mua-ban-oto?TinhTrangXe=xe-cu'
        self.source = 'https://xetot.com/'
        self.log.info('Crawling %s' %self.url)
        self.links = []
        req = requests.get(self.url, headers=HEADERS).text
        self.soup = BeautifulSoup(req, 'lxml')

    def get_link(self, link):
        req = requests.get(link, headers=HEADERS).text
        soup = BeautifulSoup(req, 'lxml')
        selector = '#partial-tin-dang-list > div.main-left > div.list-archive-item.search-page.w-100.float-left.mt-4 > ul'
        table = soup.select(selector)[0]
        h3_tag = table.find_all('h3')
        for h3 in h3_tag:
            link = self.source + h3.find('a')['href']
            self.links.append(link)

    def get_car_link(self):
        path = 'data/xetot_cars_link.txt'
        self.log.info('Opening file at path: %s' %path)
        if is_file_empty(path):
            self.log.info('File empty')
            with open(path, 'w', encoding='utf-8') as file:
                for i in range(1,14):
                    link = self.url + '&page=' +str(i)
                    self.log.info('getting link from %s' %link)
                    self.get_link(link)
                file.write('\n'.join(self.links))
                return self.links

        with open(path, 'r', encoding='utf-8') as file:
            self.log.info('Successfully opened file, returning cars_link')
            self.links = file.readlines()
            return self.links

    def crawl(self):
        used_car_path = 'data/chotot_used_car.json'
        self.log.info('Trying to open brands file at %s' %used_car_path)
        if is_file_empty(used_car_path):
            self.log.info(f'File at {used_car_path}, is empty, crawling...')
            with open(used_car_path, 'w', encoding='utf-8') as file:
                validator = ValidateUsedCars()
                self.log.info('Successfully initiate validator')
                cars_links = self.get_car_link()
                for link in cars_links:
                    extractor = XeTotUsedCarExtractor(link)
                    car = extractor.extract()
                    if validator.validate(car):
                        self.crawled_items.append(car)
                    else:
                        self.log.info("CAR FAILED")
                        self.failed_item.append(car)

                json.dump(self.crawled_items, file, indent=4, ensure_ascii=False)
                failed_item_path = 'data/chotot_failed_item.json'
                with open(failed_item_path, 'w', encoding='utf-8') as failed_file:
                    json.dump(self.failed_item, failed_file, indent=4, ensure_ascii=False)
                return self.crawled_items

        self.log.info('Successfully opened file, returning cars json from file')
        with open(used_car_path, 'r', encoding='utf-8') as file:
            cars = json.load(file)
            return cars


def main():
#     url = 'https://xetot.com/ho-chi-minh/ban-xe/ford-ranger-2015-so-tu-dong-1-cau-may-dau/6445'
#     extractor = XeTotUsedCarExtractor(url)
#     pprint(extractor.extract())
    crawler = XeTotCrawler()
    print(crawler.crawl())


if __name__ == '__main__':
    main()
