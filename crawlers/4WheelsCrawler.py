import random
import time
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
import time
import pandas as pd
import csv

chromeOptions = Options()
chromeOptions.headless = True
proxy = Proxy()
proxy.proxyType = ProxyType.MANUAL
proxy.autodetect = False

proxy.httpProxy = proxy.sslProxy = proxy.socksProxy = "171.251.22.154:5001"
chromeOptions.Proxy = proxy
chromeOptions.add_argument("ignore-certificate-errors")


ser = Service(r"/Users/sontung/PycharmProjects/linhtinh/chromedriver-2")
driver = webdriver.Chrome(service=ser, options=chromeOptions)
driver.get("https://xe.chotot.com/mua-ban-oto-cu-sdca1")

CARS = '//*[@id="__next"]/div[3]/div[1]/div[3]/main/div[1]/div[4]/div/div[1]/ul[1]/div[1]/li/a/div[2]/div/div[3]'
CARS2 = '//*[@id="__next"]/div[3]/div[1]/div[3]/main/div[1]/div[4]/div/div[1]/ul[1]/div[2]/li/a/div[2]/div/div[2]/div/p'
CARS3 =  '/html/body/div[1]/div[3]/div[1]/div[3]/main/div[1]/div[4]/div/div[1]/ul[1]/div[2]/li/a/div[2]/div/h3'

list_car = []
# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, CARS3))).click()

def process_car(car):
    if car['transmission'] == 'Tự động' or car['transmission'] == 'Số tự động':
        car['transmission'] = 'Automatic'
    elif car['transmission'] == 'Số sàn':
        car['transmission'] = 'Manual'
    if car['fuel'] == 'Dầu':
        car['fuel'] = 'Diesel'
    elif car['fuel'] == 'Xăng':
        car['fuel'] = 'Gasoline'
    return car


def get_car(driver, path):
    global list_car
    hyper = {
        'car_brand' : '/html/body/div[1]/div[3]/div[1]/div/div[4]/div[5]/div[2]/div/div[2]/span/span[2]',
        'car_model' : '/html/body/div[1]/div[3]/div[1]/div/div[4]/div[5]/div[3]/div/div[2]/span/span[2]',
        'car_date' : '/html/body/div[1]/div[3]/div[1]/div/div[4]/div[5]/div[4]/div/div[2]/span/span[2]',
        'car_km' : '/html/body/div[1]/div[3]/div[1]/div/div[4]/div[5]/div[5]/div/div[2]/span/span[2]',
        'car_transmission' : '/html/body/div[1]/div[3]/div[1]/div/div[4]/div[5]/div[7]/div/div[2]/span/span[2]',
        'car_fuel' : '/html/body/div[1]/div[3]/div[1]/div/div[4]/div[5]/div[8]/div/div[2]/span/span[2]',
        'car_type' : '/html/body/div[1]/div[3]/div[1]/div/div[4]/div[5]/div[10]/div/div[2]/span/span[2]',
        'car_seats' : '/html/body/div[1]/div[3]/div[1]/div/div[4]/div[5]/div[11]/div/div[2]/span/span[2]',
        'car_price' : '/html/body/div[1]/div[3]/div[1]/div/div[4]/div[2]/div[1]/div[1]/span/div/span/span/span[1]',
        'next' : '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div/button[2]'

    }

    ele = driver.find_element(By.XPATH, path)
    driver.execute_script("arguments[0].click();", ele)
    for _ in range(10):
        car = {}
        time.sleep(random.uniform(0,1))
        try:
            car['brand'] = driver.find_element(By.XPATH, hyper['car_brand']).text
            car['model'] = driver.find_element(By.XPATH, hyper['car_model']).text
            car['date'] = driver.find_element(By.XPATH, hyper['car_date']).text
            car['km_driven'] = driver.find_element(By.XPATH, hyper['car_km']).text
            car['transmission'] = driver.find_element(By.XPATH, hyper['car_transmission']).text
            car['fuel'] = driver.find_element(By.XPATH, hyper['car_fuel']).text
            car['type'] = driver.find_element(By.XPATH, hyper['car_type']).text
            car['seats'] = driver.find_element(By.XPATH, hyper['car_seats']).text
            car['price'] = driver.find_element(By.XPATH, hyper['car_price']).text.split()[0]
            car['url'] = driver.current_url
        except:
            pass
        # print(car)
        if len(car.keys()) > 9:
            list_car.append(process_car(car))
        time.sleep(random.uniform(0,1))
        next = driver.find_element(By.XPATH, hyper['next'])
        driver.execute_script("arguments[0].click();", next)
        print('Loop {}: Done'.format(_))
    print('All done')
    driver.quit()

get_car(driver, CARS3)
# print(list_car)
# print('-----')
# print(list_car[0]['brand'])

keys = list_car[0].keys()
with open('4wheels.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(list_car)

# df.to_csv('4wheels.csv', encoding='utf-8')

