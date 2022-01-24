import requests
from bs4 import BeautifulSoup
from base import BaseClass
from crawlers.crawler import Crawler
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import websockets
import warnings
import pandas as pd
from pprint import pprint
from common.check_file_empty import is_file_empty
from common.text_normalizer import normalized
from common.normalize_price import normalize_price, replace_all
from common.headers import HEADERS
from schema.validate import ValidateUsedCars
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep


class WS:

    def __init__(self):
        warnings.warn('EXPERIMENTAL ONLY', UserWarning)
        self.socket = 'wss://choxeotofun.net/sockjs/543/elmscmew/websocket'
        self.close = None  # default value at start

    def stream(self):
        self.ws = websockets.WebSocketApp(
            self.socket,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )

        print('run forever')
        self.ws.run_forever()

    def on_open(self, ws):
        print('on_open:', ws)

        data = {'op': 'subscribe', 'channel': 'ticker', 'market': 'ETH-PERP'}

        self.ws.send(json.dumps(data))

    def on_close(self, ws):
        print('on_close:', ws)

    def on_message(self, ws, message):
        print('on_message:', ws, message)

        data = json.loads(message)

        if data['type'] == 'update':
            self.close = data['data']['last']

    def get_data_out(self):
        return self.close

    def on_error(self, ws, error):
        print('on_error:', ws, error)


class GetMissingData(BaseClass):
    def __init__(self):
        super().__init__()
        url = 'https://raw.githubusercontent.com/Hyprnx/used-cars-prices-prediction/main/data/bonbanh_used_cars.json'
        self.data = requests.get(url, headers=HEADERS).json()

    def get_data(self):
        return self.data


class ChoXeOtoFunCarExtractor(BaseClass):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.log.info('Connecting to %s' %self.url)
        driver.get(self.url)
        self.log_entries = [entry for entry in driver.get_log('performance')]
        req = driver.page_source
        self.soup = BeautifulSoup(req, 'lxml')

    def _get_websocket(self):
        for i in self.log_entries:
            message = json.loads(i['message'])
            method = message['message']['method']
            if method == 'Network.webSocketCreated':
                url = message['message']['params']['url']
                return url
        return self.log.info('NO WEBSOCKER FOUND AT %s' %self.url)

    def _get_log(self):
        return self.log_entries



    def get_name(self):
        selector = '#react-target > div > div.site-container > div.main-content > div.car-details__StyledPage-sc-1n76gqm-0.bFDqvC > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12 > div > div.main-container > div.left-column > div.specifications > h2'
        container = self.soup.select(selector)[0]
        container = container.text
        index = container.index('bán xe')
        name = container[(index + 7):-4]
        return normalized(name, delimiter= ' ')

    def get_price(self):
        selector = '#react-target > div > div.site-container > div.main-content > div.car-details__StyledPage-sc-1n76gqm-0.bFDqvC > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12 > div > div.main-container > div.left-column > div.specifications > div.post-info > div.price > span'
        container = self.soup.select(selector)[0].text
        price = normalize_price(container)
        return price

    def avg_km_driven(self, km_driven):
        replacer = {
            '0 km(xe mới)': '0',
            'dưới 1000 km': '500',
            '1000 - 3000 km': '1500',
            '3000 - 6000 km': '4500',
            '6000 - 1 vạn' : '8000',
            '1 vạn - 2 vạn' : '15000',
            '2 vạn - 4 vạn': '30000',
            '4 vạn - 7 vạn': '55000',
            '7 vạn - 10 vạn': '85000',
            '10 vạn - 15 vạn': '125000',
            '15 vạn - 20 vạn': '175000',
            'trên 20 vạn': '0'
        }
        km_driven = replace_all(replacer, km_driven)
        return int(km_driven)

    def normalize_fuels(self,fuels):
        replacer = {
            'Xăng': 'gasoline',
            'Dầu': 'diesel',
            'Điện': 'electric',
        }
        fuels = replace_all(replacer,fuels)
        return fuels

    def normalize_wheel_drive(self, wheel_drive):
        replacer = {
            'Cầu trước (FWD)': 'FWD',
            'Cầu sau (RWD)': 'RWD',
            'Hai cầu (4WD)': '4WD',
            'Hai Cầu': '0'
        }
        wheel_drive = replace_all(replacer, wheel_drive)
        return wheel_drive

    def normalize_transmission(self, transmission):
        replacer = {
            'Số tự động': 'automatic',
            'Số sàn (tay)': 'manual'
        }
        transmission = replace_all(replacer, transmission)
        return transmission

    def get_type(self):
        # sleep(3)
        xpath = '/html/body/div/div/div[1]/div[2]/div[2]/div/div[1]/div/div[1]/div[2]/div[3]/div/div[2]/div[2]/div/div/div/div/div/div[1]/p'
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        # container = self.soup.select(selector)[0].text
        return element.text


    def extract(self):
        try:
            car = {}
            car['price'] = self.get_price()
            car['source'] = 'https://choxeotofun.net/'
            car['source_url'] = self.url
            car['name'] = self.get_name()

            # brand_selector = '#react-target > div > div.site-container > div.main-content > div.car-details__StyledPage-sc-1n76gqm-0.bFDqvC > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12 > div > div.main-container > div.left-column > div.specifications > div.MuiPaper-root.info-table.MuiPaper-elevation1.MuiPaper-rounded > div > div:nth-child(2)'
            # car['brand'] = normalized(self.soup.select(brand_selector)[0].text)
            year_selector = '#react-target > div > div.site-container > div.main-content > div.car-details__StyledPage-sc-1n76gqm-0.bFDqvC > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12 > div > div.main-container > div.left-column > div.specifications > div.MuiPaper-root.info-table.MuiPaper-elevation1.MuiPaper-rounded > div > div:nth-child(6)'
            car['year'] = int(self.soup.select(year_selector)[0].text)
            km_driven_selector = '#react-target > div > div.site-container > div.main-content > div.car-details__StyledPage-sc-1n76gqm-0.bFDqvC > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12 > div > div.main-container > div.left-column > div.specifications > div.MuiPaper-root.info-table.MuiPaper-elevation1.MuiPaper-rounded > div > div:nth-child(8)'
            car['km_driven'] = self.avg_km_driven(self.soup.select(km_driven_selector)[0].text)
            fuel_selector = '#react-target > div > div.site-container > div.main-content > div.car-details__StyledPage-sc-1n76gqm-0.bFDqvC > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12 > div > div.main-container > div.left-column > div.specifications > div.MuiPaper-root.info-table.MuiPaper-elevation1.MuiPaper-rounded > div > div:nth-child(14)'
            car['fuels'] = self.normalize_fuels(self.soup.select(fuel_selector)[0].text)
            engine_capacity_selector = '#react-target > div > div.site-container > div.main-content > div.car-details__StyledPage-sc-1n76gqm-0.bFDqvC > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12 > div > div.main-container > div.left-column > div.specifications > div.MuiPaper-root.info-table.MuiPaper-elevation1.MuiPaper-rounded > div > div:nth-child(16)'
            car['engine_capacity'] = float(self.soup.select(engine_capacity_selector)[0].text)
            wheel_drive_selector = '#react-target > div > div.site-container > div.main-content > div.car-details__StyledPage-sc-1n76gqm-0.bFDqvC > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12 > div > div.main-container > div.left-column > div.specifications > div.MuiPaper-root.info-table.MuiPaper-elevation1.MuiPaper-rounded > div > div:nth-child(18)'
            car['wheel_drive'] = self.normalize_wheel_drive(self.soup.select(wheel_drive_selector)[0].text)
            external_color_selector = '#react-target > div > div.site-container > div.main-content > div.car-details__StyledPage-sc-1n76gqm-0.bFDqvC > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12 > div > div.main-container > div.left-column > div.specifications > div.MuiPaper-root.info-table.MuiPaper-elevation1.MuiPaper-rounded > div > div:nth-child(10)'
            car['external_color'] = self.soup.select(external_color_selector)[0].text
            transmission_selector = '#react-target > div > div.site-container > div.main-content > div.car-details__StyledPage-sc-1n76gqm-0.bFDqvC > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12 > div > div.main-container > div.left-column > div.specifications > div.MuiPaper-root.info-table.MuiPaper-elevation1.MuiPaper-rounded > div > div:nth-child(12)'
            car['transmission'] = self.normalize_transmission(self.soup.select(transmission_selector)[0].text)
            return car
        except BaseException as e:
            self.log.info(e)
            return None




class ChoXeOtoFunCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.key = '?gt=1638524283073'
        self.car_indicator = '/o-to'
        self.BASE_URL = 'https://choxeotofun.net'
        self.POST_FIX = '&p='

        # add page after '&p=' to get access to the page

    def get_page(self):
        pages_path = 'data/ChoXeOtoFun_pages_links.txt'
        self.log.info('Getting cars Link from %s' %pages_path)
        if is_file_empty(pages_path):
            self.log.info('File empty, generating pages...')
            with open('data/ChoXeOtoFun_pages_links.txt', 'w', encoding='utf-8') as file:
                pages = [self.BASE_URL + self.car_indicator + self.key + self.POST_FIX + str(i) for i in range(2822)]
                file.write('\n'.join([i for i in pages]))
                return pages

        self.log.info('Successfully opened file, returning pages links')
        with open('data/ChoXeOtoFun_pages_links.txt', 'r', encoding='utf-8') as file:
            pages = file.readlines()
            return pages

    def extract_cars_link_in_page(self, page):
        url = page.split('\n')[0]
        req = requests.get(url,headers=HEADERS).text
        soup = BeautifulSoup(req, 'lxml')
        cars = []
        for i in range(1,19):
            selector = f'#react-target > div > div.site-container > div.main-content > div.list__StyledPage-skpmhw-0.kmcMaQ > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12 > div > div.main-container > div.left-column > div.styles__StyledListing-sc-5y87aq-1.btHUuc.listing-container > div.grid-container-wrapper > div.MuiGrid-root.list-container.MuiGrid-container.MuiGrid-spacing-xs-2 > div:nth-child({i}) > div > div > div > div.card-media-container > a'
            container = soup.select(selector)[0]
            car = container['href']
            cars.append(self.BASE_URL + car)

        for car in cars:
            yield car

    def get_cars_links(self):
        cars_path = 'data/ChoXeOtoFun_cars_links.txt'
        if is_file_empty(cars_path):
            with open(cars_path, 'w', encoding='utf-8') as cars_links:
                pages = self.get_page()
                cars_lists = []
                for page in pages:
                    link_in_page = self.extract_cars_link_in_page(page)
                    for link in link_in_page:
                        cars_lists.append(link)

        self.log.info('Successfully opened file, returning cars links')
        with open('data/ChoXeOtoFun_pages_links.txt', 'r', encoding='utf-8') as file:
            pages = file.readlines()
            return pages




def main():
    validate = ValidateUsedCars()
    links = ['https://choxeotofun.net/ban-xe/ha-noi-ban-xe-mercedes-benz-c-class-at-2015-KBCLDwhGiXuFtGzNg',
             'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-mercedes-benz-e-classe-at-2011-sJ8Xw4YCX3mt8rP9p',
            'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-kia-cerato-1-6-at-2011-ZyrPfBao3cZarRmP9',
            'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-hyundai-i10-1-2-at-2019-gAsZ52xopCA6q7Qnw',
            'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-hyundai-starex-mt-2012-cWpnSCBcMdXBMT3iQ',
            'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-ford-everest-2-0-at-2019-aEpjM56WDrgpXSMs8',
            'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-honda-civic-2-0-at-2008-RJDFbC5Ti97zznpLz',
            'https://choxeotofun.net/ban-xe/ho-chi-minh-ban-xe-lexus-lx-5-7-at-2020-2q8pt7f3rYPnHLanB',
            'https://choxeotofun.net/ban-xe/tuyen-quang-ban-xe-toyota-vios-1-5-mt-2010-W9wotznRGwPanW3uJ',
            'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-kia-cerato-1600-at-2017-Bfi9ouBR2mRaA3T7D',
            'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-mercedes-benz-glk-class-3000-at-2009-nFvhJiCwBkM3pGYrM',
            'https://choxeotofun.net/ban-xe/ho-chi-minh-ban-xe-hyundai-kona-2-0-at-2019-dxRQPWcGTR3NrnDhv',
            'https://choxeotofun.net/ban-xe/ho-chi-minh-ban-xe-hyundai-kona-2-0-at-2018-2Gob5GYfbSncaGh4k',
            'https://choxeotofun.net/ban-xe/ho-chi-minh-ban-xe-toyota-innova-2-0-mt-2014-5hLbKfG5RYSE66sZH',
            'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-lexus-es-at-2018-qe2CfDYaEEnaxLTsa',
            'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-kia-rio-1-4-at-2016-85D8bwhBd8aLGHhoR',
            'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-hyundai-i10-mt-2015-MkBF7eQXqqJ58G7zX',
            'https://choxeotofun.net/ban-xe/ha-noi-ban-xe-vinfast-lux-sa2-0-2-0-at-2020-i4B3EQn8RdRL2FAbw'
            ]
    for link in links:
        crwlr = ChoXeOtoFunCarExtractor(link)
        res = crwlr.extract()
        pprint(res)

    # check_data = GetMissingData()
    # pprint(check_data.get_data())


if __name__ == '__main__':
    CHROME_DRIVER_PATH = 'C:\\Users\\toduc\\Downloads\\chromedriver_win32\\chromedriver.exe'  # change path when use on your machine
    options = Options()
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    options.headless = True
    driver = Chrome(executable_path=CHROME_DRIVER_PATH, options=options, desired_capabilities=caps)
    main()

