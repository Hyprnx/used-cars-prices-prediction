from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re


class OtoCrawl:
    def __init__(self, base_url):
        self.base_url = base_url

    #  Input 1 page cua 1 hang xe
    def crawl_href(self, url):
        df = pd.DataFrame(columns=['href'])

        html_text = requests.get(url).text
        soup = bs(html_text, 'html.parser')
        box_list_car = soup.find('div', class_='box-list-car')
        item_cars = box_list_car.find_all('div', class_=re.compile(r'item-car'))

        for item in item_cars:
            href = item.find('a')['href']
            link = '{}{}'.format(self.base_url, href)
            # print(link)
            df = df.append({'href': link}, ignore_index=True)

        return df

    def add_to_csv(self, i, df):
        if i == 1:
            df.to_csv('oto_comvn_href.csv', index=False)
        else:
            df.to_csv('oto_comvn_href.csv', mode='a', index=False, header=False)


base_url = 'https://oto.com.vn'
toyota_url = 'https://oto.com.vn/mua-ban-xe-toyota-cu-da-qua-su-dung'

oto = OtoCrawl(base_url)

for i in range(1, 102):
    url = '{}/p{}'.format(toyota_url, i)
    df = oto.crawl_href(url)
    oto.add_to_csv(i, df)