from crawlers.crawler import Crawler
from bs4 import BeautifulSoup
import requests
import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) "
                  "Gecko/20100101 Firefox/46.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0"
}

class BonBanhCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.path = 'C:\\Users\\toduc\\Downloads\\chromedriver_win32\\chromedriver.exe' # change path when use on your machine
        options = Options()
        options.headless = True
        self.driver = Chrome(executable_path=self.path, options=options)
        self.url = 'https://bonbanh.com/'
        self.source = 'https://bonbanh.com/'
        self.driver.get(self.url)
        req = self.driver.page_source
        self.soup = BeautifulSoup(req, 'lxml')


    def _get_brand(self):
        selector = '#primary-nav'
        brands = []
        transparent_brands_container = self.soup.select(selector)[0].find_all('li', attrs={'class':"menuparent", 'style':"z-index:999;"})
        hidden_brands_container = self.soup.select(selector)[0].find_all('li', attrs={'class':"menuparent add_menu"})
        for brand_container in transparent_brands_container:
            brand = brand_container.find('a')['href']
            brands.append(self.source + brand)
        for brand_container in hidden_brands_container:
            brand = brand_container.find('span')['url']
            brands.append(self.source + brand)
        return brands

    def soup(self):
        return self.soup().prettify()

def main():
    cr = BonBanhCrawler()
    for i in cr._get_brand():
        print(i)



if __name__ == '__main__':
    main()