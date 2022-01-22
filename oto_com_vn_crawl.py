from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from oto_comvn_class import OtoCrawl
import re


def _replace_all(text):
    list = ['Năm sản xuất', 'Kiểu dáng', 'Tình trạng', 'Xuất xứ', 'Số km đã đi', 'Tỉnh thành', 'Hộp số', 'Nhiên liệu']
    for i in list:
        text = text.replace(i, '')
    return text


df = pd.DataFrame(columns=["name", "source_url", "origin", "km_driven",
                           "external_color", "seats", "engine_capacity",
                           "fuels", "transmission", "wheel_drive",
                           "price", "year"])


base_url = 'https://oto.com.vn'
toyota_url = 'https://oto.com.vn/mua-ban-xe-toyota'

href_df = pd.read_csv('oto_comvn_href.csv')

car = {}

for href in href_df['href']:

    html_text = requests.get(href)
    # soup = bs(html_text, 'html.parser')
    content = html_text.content
    soup = bs(content.decode('utf-8', 'ignore'), 'html.parser')

    box_detail = soup.find('div', class_='box-detail-listing', id='box-detail')

    price = box_detail.find('input', id='price')['value']
    car['price'] = price
    car['source_url'] = href
    seats = box_detail.find('input', id='numberOfSeat')['value']
    car['seats'] = seats
    # year = box_detail.find('input', id='year')['value']
    # typeOfCar = box_detail.find('input', id='classificationName')['value']

    group_title_detail = soup.find('div', class_='group-title-detail')
    name = group_title_detail.find('h1').string
    car['name'] = name
    car['source_url'] = href

    box_info_detail = soup.find('div', class_='box-info-detail')
    li = box_info_detail.find_all('li')
    info = []

    for l in li:
        txt = _replace_all(l.text.strip())
        info.append(txt)

    keys = ['year', 'typeOfCar', 'condition', 'origin', 'km_driven',
            'city', 'transmission', 'fuels']

    for i in range(8):
        car[keys[i]] = info[i]

    print(car)














