from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


class Crawl:

    def __init__(self, base_url):
        self.base_url = base_url

    def _replace_all(self, text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    def _price_process(self, price):
        new_price = price.replace('.', '')[:-2]
        return int(new_price)

    def _extract_origin(self, origin):
        if origin == 'Việt Nam':
            origin = 'domestic'
        else:
            origin = 'imported'
        return origin

    def _extract_transmission(self, transmission):
        replacer = {
            'Tự động': 'automatic',
            'Số sàn': 'manual',
            'Bán tự động' : 'semi-automatic'
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

    def _process_car(self, car):
        if not car['prices'] or not car['km_driven']:
            return None
        else:
            car['prices'] = self._price_process(car['prices'])
            car['origin'] = self._extract_origin(car['origin'])
            car['transmission'] = self._extract_transmission(car['transmission'])
            car['fuel'] = self._extract_fuels(car['fuel'])

        return car

    def crawl_all_pages(self):
        url_list = ['{}?page={}'.format(self.base_url, str(page)) for page in range(700, 1000)] #range of pages
        return url_list

    def crawl_href(self, url):
        html_text = requests.get(url).text
        soup = bs(html_text, 'html.parser')
        button = soup.find_all('div', attrs={'role': 'button','tabindex':0 })

        href_lst = []

        for i in button:
            try:
                href = i.find('a')['href'][16:]
                href_lst.append('{}{}'.format(self.base_url, href))
            except:
                pass

        return href_lst


    def crawl_data(self, href):
        output = pd.DataFrame()
        html_text = requests.get(href).text
        soup = bs(html_text, 'html.parser')

        data_itemprops = {
            'brand' : 'carbrand',
            'model' : 'carmodel',
            'date' : 'mfdate',
            'km_driven' : 'mileage_v2',
            'transmission' : 'gearbox',
            'fuel' : 'fuel',
            'origin' : 'carorigin',
            'type' : 'cartype',
            'seats' : 'carseats',
            'prices' : 'price'

        }

        car = {}
        car['url'] = href
        fields = data_itemprops.keys()

        for field in fields:
            itemprop = data_itemprops.get(field)
            try:
                car[field] = soup.find('span', itemprop=itemprop).string
            except:
                car[field] = None

        car = self._process_car(car)
        output = output.append(car, ignore_index=True)
        return output

    def add_to_csv(self, p, output):
        if p == 1:
            output.to_csv('4banh.csv', index=False)
        else:
            output.to_csv('4banh.csv', mode='a', index=False, header=False)


base_url = 'https://xe.chotot.com/'
url = 'https://xe.chotot.com/mua-ban-oto-cu-sdca1'

scrape = Crawl(base_url=url)

pages_url = scrape.crawl_all_pages()

p = 1

for page in pages_url:
    car_url = scrape.crawl_href(page)

    for href in car_url:
        output = scrape.crawl_data(href=href)
        scrape.add_to_csv(p, output)
        print(p)
        p += 1