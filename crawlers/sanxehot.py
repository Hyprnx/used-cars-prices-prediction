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


class ExtractSanXeTotLink:
    def __init__(self):
        self.prefix = 'https://www.sanxehot.vn/'
        self.index = [i for i in range(1, 786)]
        self.url_list = ['https://www.sanxehot.vn/mua-ban-xe/loai-xe-cu-pg' + str(i) for i in self.index]
        self.car_link = []
        self.num = 0

    def extract_link(self):
        for link in self.url_list:
            req = requests.get(link, headers=HEADERS).text
            soup = BeautifulSoup(req, 'lxml')
            lis = soup.findAll('li', attrs={'class': 'cars'})

            for i in lis:
                self.num += 1
                div_container = i.find('div', attrs={'class': 'col m8'})
                a = div_container.find('a')
                self.car_link.append(self.prefix + a['href'])
                print(self.num)

        return self.car_link


def main():
    car_link = ExtractSanXeTotLink().extract_link()
    print('\n'.join(car_link))
    with open("sanxehot_link.txt", "w+") as f:
        f.write('\n'.join(car_link))


if __name__ == '__main__':
    main()

