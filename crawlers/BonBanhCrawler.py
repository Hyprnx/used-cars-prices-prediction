from crawlers.crawler import Crawler
from bs4 import BeautifulSoup
from base import BaseClass
from common.text_normalizer import normalized
import requests
import os
from pprint import pprint
import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep


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

    def crawl(self):
        name_selector = '#car_detail > div.title > h1'
        name = normalized(self.soup.select(name_selector)[0].text)
        container_selector = '#mail_parent > div.txt_input > span'
        container = self.soup.select(container_selector)
        origin = container[0].text
        km_driven = container[3].text.split(" ")[0]
        external_color = container[4].text
        internal_color = container[5].text
        seats = container[6].text.split(' ')[0]
        fuels_and_engine_capacity_container = container[7].text.split("\t")
        fuels = fuels_and_engine_capacity_container[0]
        engine_capacity = fuels_and_engine_capacity_container[1].split(' ')[0]
        transmission = container[9].text
        wheel_drive = container[10].text.split(' ')[0]
        car = {
            'name' : name,
            'origin' : origin,
            'km_driven' : km_driven,
            'external_color': external_color,
            'internal_color': internal_color,
            'seats' : seats,
            'fuels' : fuels,
            'engine_capacity' : engine_capacity,
            'transmission': transmission,
            'wheel_drive': wheel_drive
        }

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
            with open(file_path, 'w') as file:
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
        with open(file_path, 'r') as file:
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
            with open(file_path, 'w') as file:
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
        with open(file_path, 'r') as file:
            cars_links = file.readlines()
            return cars_links


    def soup(self):
        return self.soup().prettify()



def main():
    cr = BonBanhCrawler()
    cr._get_cars_link()


if __name__ == '__main__':
    main()