#  Copyright 2022. Nguyen Thanh Tuan, To Duc Anh, Tran Minh Khoa, Duong Thu Phuong, Nguyen Anh Tu, Kieu Son Tung, Nguyen Son Tung
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

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