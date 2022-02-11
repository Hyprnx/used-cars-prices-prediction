import scrapy
import os
import json
import subprocess
import time
import pandas as pd


class BonBanhScrapy(scrapy.Spider):
    name = 'bonbanhcrawler'
    PREFIX = 'https://bonbanh.com/'
    def start_requests(self):
        urls = ['https://bonbanh.com/']
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        container = response.xpath('//*[@id="primary-nav"]')
        links = container.xpath('.//a')
        for link in links:
            path = self.PREFIX + link.xpath('@href').extract()[0]
            yield {'href': path}

def main():
    subprocess.run('scrapy crawl bonbanhcrawler -o cars_links.json')

if __name__ == '__main__':
    main()