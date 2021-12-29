import logging
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.ERROR)

class Crawler(object):
    """
    Abstract class of crawler, all crawlers must implement crawl() and convert() method
    """
    # REMEMBER TO SET LOGGER TO EACH WORK YOU DO!
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)
        self.log.info('Initializing %s' % self.__class__.__name__)
        self.crawled_items = []
        self.cnt_crawled_items = 0


    def validate_crawled(self, item):
        raise NotImplementedError

    def save_crawled_items(self):
        raise NotImplementedError

    def save(self, item):
        """
        Implement crawl and save items
        """
        raise NotImplementedError

    def crawl(self):
        """
            Implement crawl and save items
        """
        raise NotImplementedError

    def finish(self):
        # self.crawl()
        raise NotImplementedError

def main():
    cr = Crawler()
    print(cr.cnt_crawled_items)

if __name__ == '__main__':
    main()