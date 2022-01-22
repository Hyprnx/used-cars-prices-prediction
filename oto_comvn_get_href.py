from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re


base_url = 'https://oto.com.vn'
toyota_url = 'https://oto.com.vn/mua-ban-xe-toyota'

df = pd.DataFrame(columns=['href'])


for i in range(1, 102):

    try:

        html_text = requests.get('{}/p{}'.format(toyota_url, i)).text
        soup = bs(html_text, 'html.parser')
        box_list_car = soup.find('div', class_='box-list-car')
        item_cars = box_list_car.find_all('div', class_=re.compile(r'item-car'))

        for item in item_cars:
            href = item.find('a')['href']
            link = '{}{}'.format(base_url, href)
            # print(link)
            df = df.append({'href': link}, ignore_index=True)

        print(df)

        if i == 1:
            df.to_csv('oto_comvn_href.csv', index=False)
        else:
            df.to_csv('oto_comvn_href.csv', mode='a', index=False, header=False)

    except:
        print('Error!!!!')


