from crawlers.crawler import Crawler
from bs4 import BeautifulSoup
from base import BaseClass
from common.check_file_empty import is_file_empty
from common.check_os import get_selenium_chrome_webdriver_path
from common.text_normalizer import normalized
from common.normalize_price import replace_all
import pandas as pd
from common.headers import HEADERS
import json
import requests

import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from pprint import pprint
from schema.validate import ValidateUsedCars


class DanhGiaXeExtractor(BaseClass):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def normalize_name(self, name):
        for i in range(len(name)):
            if name[i].isdigit():
                return name[:i]
        return name

    def extract_engine_capacity(self, engine_capacity):
        engine_capacity = engine_capacity.replace('L', '')
        return engine_capacity

    def extract(self):
        res = pd.read_html(self.url)[1]
        replacer = {
            'Dáng xe ': '',
            'Số chỗ ngồi ': '',
            'Số cửa sổ': '',
            'Kiểu động cơ': '',
            'Dung tích động cơ ': '',
            'Công suất cực đại ': '',
            'mã lực': '',
            'Momen xoắn cực đại ': '',
            ' Nm': '',
            'Hộp số': '',
            'Kiểu dẫn động': '',
        }
        for i in range(res.shape[1]):
            name = self.normalize_name(replace_all(replacer, res[i][0]))
            _type = replace_all(replacer, res[i][1]).lower()
            seats = int(replace_all(replacer, res[i][2]))
            engine_capacity = self.extract_engine_capacity(replace_all(replacer, res[i][5]))
            wheel_drive = replace_all(replacer, res[i][9]).replace(' ', '')
            yield name, {'name': name,
                         'type': _type,
                         'seats': seats,
                         'engine_capacity': engine_capacity,
                         'wheel_drive': wheel_drive}


class DanhGiaXeCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.log.info('Initializing Selenium')
        self.chrome_driver_path = get_selenium_chrome_webdriver_path()
        options = Options()
        options.headless = True
        self.driver = Chrome(executable_path=self.chrome_driver_path, options=options)
        self.source = 'https://www.danhgiaxe.com/'
        review_domain = self.source + 'danh-gia-pg'
        self.source_list = [review_domain + str(i) for i in range(1, 67)]
        self.review_list = []
        self.cars = {}

    def get_review_links(self):
        review_link_path = 'cars_information/danhgiaxe/review_link.txt'
        self.log.info('Opening file %s' % review_link_path)
        if is_file_empty(review_link_path):
            self.log.info('File empty, crawling review links')
            with open(review_link_path, 'w', encoding='utf-8') as file:
                for source in self.source_list:
                    self.log.info('Crawling %s' % source)
                    self.driver.get(source)
                    soup = BeautifulSoup(self.driver.page_source, 'lxml')
                    container_selector = 'body > main > div > div > div.col.m9.l7 > div > div > div.list-review > ul'
                    container = soup.select(container_selector)[0]
                    li_list = container.find_all('li')
                    for li in li_list:
                        a = li.find('a')['href']
                        link = self.source + a
                        self.review_list.append(link)
                        self.log.info('Crawled %s' % link)
                file.write('\n'.join(self.review_list))
                return self.review_list

        with open(review_link_path, 'r', encoding='utf-8') as file:
            self.log.info('File exist, returning review links')
            self.review_list = file.readlines()
            return self.review_list

    # def crawl(self):
    #     links = self.get_review_links()
    #     for link in links:
    #         extractor = DanhGiaXeExtractor(link).extract()
    #         for res in extractor:
    #             self.cars[res[0]] = res[1]
    #
    #     print(self.cars)


def main():
    # crwl = DanhGiaXeCrawler()
    # print(crwl.crawl())
    # extractor = DanhGiaXeExtractor(
    #     'https://www.danhgiaxe.com//danh-gia/danh-gia-xe-kia-morning-2022-kho-tim-lai-hao-quang-da-mat-30598')
    # extractor.extract()
    pass


if __name__ == '__main__':
    main()
