import requests

requests.adapters.DEFAULT_RETRIES = 5
from lxml import html
from bs4 import BeautifulSoup
from pymongo import MongoClient


def get_status_code(url):
    try:
        r = requests.get(url, timeout=20, auth=('user', 'pass'))
        r_s = r.status_code
    except:
        r_s = 'ConnectionError'
    # website responds correct
    if r_s == 200:
        brand_list, p = get_brand_list(url, r)
    # website responds error
    else:
        brand_list = ""
    return r_s, brand_list, p


def get_brand_list(url):
    main_page = requests.get(url, timeout=20, auth=('user', 'pass'))
    try:
        tree = html.fromstring(main_page.text)
        brand_list = tree.xpath('//*[@id="center"]/div[1]/a/@href')
        for i in range(len(brand_list)):
            brand_list[i] = 'https://www.auto-data.net' + brand_list[i]
    except:
        brand_list = "page_code_error"
    return brand_list


def get_model_list(url):
    main_page = requests.get(url, timeout=20, auth=('user', 'pass'))
    try:
        tree = html.fromstring(main_page.text)
        model_list = tree.xpath('//*[@id="center"]/div[1]/a/@href')
        for i in range(len(model_list)):
            model_list[i] = 'https://www.auto-data.net' + model_list[i]
    except:
        model_list = "page_code_error"
    return model_list


def get_modification_list(url):
    main_page = requests.get(url, timeout=20, auth=('user', 'pass'))
    try:
        tree = html.fromstring(main_page.text)
        modi_list = tree.xpath('//*[@id="center"]/table[@class]/tr[@class]/td[1]/a/@href')
        for i in range(len(modi_list)):
            modi_list[i] = 'https://www.auto-data.net' + modi_list[i]
    except:
        modi_list = "page_code_error"
    return modi_list


def get_parameter_list(url):
    r = requests.get(url, timeout=20, auth=('user', 'pass'))
    bs = BeautifulSoup(r.content, "lxml")
    table_body = bs.find('table')
    rows = table_body.find_all('tr')
    para_list = []
    for row in rows:
        cols = row.find_all('td')
        cols = [x.text.strip() for x in cols]
        para_list.append(cols)
    return para_list




def main():
    client = MongoClient()
    db = client.car_database
    car = db.car

    url = 'https://www.auto-data.net/en/allbrands'
    brand_list = get_brand_list(url)
    for i in range(len(brand_list)):
        model_list = get_model_list(brand_list[i])
        for j in range(len(model_list)):
            modi_list = get_modification_list(model_list[j])
            for k in range(len(modi_list)):
                para_list = get_parameter_list(modi_list[k])
                para_dict = {}
                for h in para_list:
                    para_dict.update({h[0].replace('.', ''): h[1]})
                car_id = car.insert_one(para_dict).inserted_id
                print(i, '-', j, '-', '-', k)


if __name__ == "__main__":
    main()