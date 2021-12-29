import logging

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.ERROR)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class BaseClass:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)
        self.log.info('Init %s' % self.__class__.__name__)

