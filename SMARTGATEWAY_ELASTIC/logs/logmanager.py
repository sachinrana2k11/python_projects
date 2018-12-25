import logging
from datetime import datetime
import os



class log:
    def __init__(self):
        self.DateString = "%Y-%m-%d"
        self.TimeString = "%H-%M-%S"
        self.date = str(datetime.now().strftime(self.DateString))
        self.time = str(datetime.now().strftime(self.TimeString))
        self.dir_name = str("logs/"+self.date)
        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)
        self.temp1 = logging.getLogger('peewee')
        self.temp1.disabled = 1
        self.temp = logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=self.dir_name+'/'+self.time+'.log',
                    filemode='w')
        self.logger = logging


    def DEBUG(self,msg):
        self.logger.debug(msg)

    def ERROR(self,msg):
        self.logger.error(msg)


    def WARNING(self,msg):
        self.logger.warning(msg)

    def INFO(self, msg):
        self.logger.info(msg)

#LOG = log()