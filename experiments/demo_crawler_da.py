from crawlers.BonBanhCrawler import BonBanhCrawler
from crawlers.XeTotCrawler import XeTotCrawler

bonbanh = BonBanhCrawler()
xetot = XeTotCrawler()

all_crawlers = [
    bonbanh,
    xetot
]

for crawler in all_crawlers:
    crawler.crawl()
