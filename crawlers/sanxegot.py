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


prefix = 'https://www.sanxehot.vn/'
index = [i for i in range(1, 786)]
url = 'https://www.sanxehot.vn/mua-ban-xe/loai-xe-cu-pg'
links_list = [url + str(i) for i in index]
car_link = []

num = 0
for link in links_list:
    request_url = link

    req = requests.get(request_url, headers=HEADERS).text
    soup = BeautifulSoup(req, 'lxml')

    lis = soup.findAll('li', attrs={'class': 'cars'})

    for i in lis:
        num += 1
        div_container = i.find('div', attrs={'class': 'col m8'})
        a = div_container.find('a')
        car_link.append(prefix + a['href'])

        extractor = ExtractSanXeTotUsedCar(car_link[-1])
        print(num, extractor.get_name())

print(car_link)


def main():
    f = open("sanxehot_link.txt", "w+")
    f.write('\n'.join(car_link))


if __name__ == '__main__':
    main()
