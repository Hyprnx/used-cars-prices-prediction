import logging
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.ERROR)
from base import BaseClass


class Crawler(BaseClass):
    """
    Abstract class of crawler, all crawlers must implement crawl() and convert() method
    """
    # REMEMBER TO SET LOGGER TO EACH WORK YOU DO!
    def __init__(self):
        super().__init__()
        self.crawled_items = []
        self.failed_item = []


    def validate_crawled(self, item):
        # validate using schema in schema folder
        raise NotImplementedError

    def save_crawled_items(self):
        raise NotImplementedError

    def save(self, item):
        """
        Implement crawl and save items to data folder
        """
        raise NotImplementedError

    def crawl(self):
        """
            Implement crawl in subclass
        """
        raise NotImplementedError

    def finish(self):
        # self.crawl()
        raise NotImplementedError