
from peewee import *
from helpers import ConfigHelper
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime
import json
import uuid


# define a Proxy object for peewee ORM
proxy = Proxy()

# default basepayload object
# this will be used for defining payload for various hardware sensors
class basepayload(object):
    """ Base Class for Different Hardware data"""
    def payloadjson(self):
       return json.dumps(self.__dict__)

class cloudcommandpayload(object):
      # Model class for command payload received from cloud
      
      def __init__(self,json_object):
           
        if 'hardware' in json_object:
               self.hardware = json_object['hardware']
               
        if 'hardwareid' in json_object:
               self.hardwareid = json_object['hardwareid']
         
          

      



class devicedata(Model):


    
    payload = TextField()

    messagetype = TextField(default='Application')

    id = TextField(primary_key=True)
    
    organizationid= TextField()

    routeid = TextField()

    deviceid = TextField()

    hardwaretype = TextField()

    datestamp = TextField(default=datetime.datetime.now)

    timestamp = TextField(default=datetime.datetime.now)

    hardwareid = TextField()

    synced = IntegerField(default=0)

    applicationname = TextField()


    class Meta:
        database = proxy

class dummypayload(basepayload):
    """ payload class for dummy hardware """

    def __init__(self):
        self.name = None
        self.value = None
         
 
class gpspayload(basepayload):
    """ payload class for GPS hardware """

    def __init__(self):
        self.latitude =None
        self.longitude=None
        self.speed=None
        
class rfidpayload(basepayload):
    """ payload class for rfid hardware """

    def __init__(self):
        self.ID = None  

class shutpayload(basepayload):
    """ payload class for rfid hardware """

    def __init__(self):
        self.status= None

class panicpayload(basepayload):
    
    def __init__(self):
        self.status = None


class camerapayload(basepayload):
    
    def __init__(self):
        self.status = None
      
class acceleropayload(basepayload):

    def __init__(self):
        self.value = None 
        
        

