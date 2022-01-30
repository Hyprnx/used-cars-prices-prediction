import json
import requests
from bs4 import BeautifulSoup
from base import BaseClass
from schema.validate import ValidateUsedCars

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) "
                  "Gecko/20100101 Firefox/46.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0"
}

path = '/Users/minhkhoa/Documents/used-cars-prices-prediction/data/sanxehot/'


class ExtractSanXeTotUsedCar(BaseClass):
    def __init__(self, url):
        super().__init__()
        self.url = url
        req = requests.get(self.url, headers=HEADERS).text
        self.soup = BeautifulSoup(req, 'lxml')

    def get_name(self):
        name_selector = '#chitietxe > div.title.sxh-noborder > h1 > span:nth-child(2)'
        name = self.soup.select(name_selector)[0]
        return name.text


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

        return dictionary


def main():
    car_link = ExtractSanXeTotLink().extract_link()
    print('\n'.join(car_link))
    with open(path + "sanxehot_links.json", "w+") as f:
        f.write(json.dumps(car_link, indent=4))


if __name__ == '__main__':
    main()
