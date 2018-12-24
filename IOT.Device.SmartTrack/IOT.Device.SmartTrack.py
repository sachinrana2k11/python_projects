from helpers import ConfigHelper
from hardware import gpshardware,rfidhardware ,shuthardware,panichardware,camerahardware,LCD,accelerohardware
import models as md
import peewee as pw
from multiprocessing import Process, Manager
from managers import *
import uuid
import json
import time
from playhouse.shortcuts import model_to_dict, dict_to_model
from events import Events
from managers import hardwareevents,cloudevents
from time import sleep





class deviceManager(BaseManager):
    pass
    
    
# Read the Config File
c = ConfigHelper('/home/pi/mycode/IOT.Device.SmartTrack/config/SmartTrack.INI')
log = LoggingHelper(ConfigHelper.logconfig.disabled, ConfigHelper.logconfig.logtoconsole)



# Initialize the Database Specified as per the config file
localdb = pw.SqliteDatabase(ConfigHelper.dbfile)
log.info("setiing up Database file ")

md.proxy.initialize(localdb) 
log.info("Database initialize")

md.devicedata.create_table(True)
log.info("Creating table")

cm = cloudmanager(log)
log.info("cloud manager class object created")


hardmamanger = hardwaremanager(log)
log.info("hardware manager class object created")
lcd = LCD()
#self.events=hardwareevents()
#self.events=cloudevents()

#----------------- Event Handlers --------------------------
def hardware_started(name):

    log.info(name + " : hardware started and listening for data :" + str(datetime.datetime.now()))
   # print(name + " : hardware started and listening for data :" + str(datetime.datetime.now()))
    

def hardware_stopped(name):

    #print(name + " : hardware stopped at :" + str(datetime.datetime.now()))
    log.info(name + " : hardware stopped at :" + str(datetime.datetime.now()))

def hardware_enabled(name):

    #print(name + " : hardware got enabled at :" + str(datetime.datetime.now()))
    log.info(name + " : hardware got enabled at :" + str(datetime.datetime.now()))

def hardware_disabled(name):

   # print(name + " : hardware got disabled at :" + str(datetime.datetime.now()))
    log.info(name + " : hardware got disabled at :" + str(datetime.datetime.now()))

def hardware_exception(e):

   # print("Esception raised at  " + str(datetime.datetime.now()) + " : " + str(e))
    log.error("Esception raised at  " + str(datetime.datetime.now()) + " : " + str(e))


def cloud_messagesent(type,message):

   # print(type + ' - message sent at '  + str(datetime.datetime.now()) )
    log.info(type + ' - message sent at '  + str(datetime.datetime.now()) )

def cloud_messagereceived(message):

    try:
        message_buffer = message.get_bytearray()
        size = len(message_buffer)
       # print ( "    Data: <<<%s>>> & Size=%d" % (message_buffer[:size].decode('utf-8'), size) )
        log.info("    Data: <<<%s>>> & Size=%d" % (message_buffer[:size].decode('utf-8'), size))
        map_properties = message.properties()
        key_value_pair = map_properties.get_internals()
       # print ( "    Properties: %s" % key_value_pair )
        log.info ( "    Properties: %s" % key_value_pair )
    except:
        e = sys.exc_info()[0]
       # print(e)
        log.error("exception in cloud_messagereceived() Method:"+e)
        return

def cloud_command(action,payload):
   
 try:
    #print(action + ' received for " ' + device)   
    #cm.device_method_return_value.response = "{ \"Response\": \"This is the response from the dummy\" }"
    
     cm.device_method_return_value =  hardmamanger.processcomand(action,payload,hardwares)
     log.info("cloud_command processed ")
 except:
     e = sys.exc_info()[0]
     #print(e)
     log.error("Exception in cloud_command method:"+str(e))
     return

#-----------------------------------------------------------


# Test Methods

def StartCloudManager():
    
    #lcd.lcd_clear()
    #lcd.data_print("Cloud Manager",0,0)
    #lcd.data_print("Starting",0,1)
    #sleep(1)
    cm.events.cloud_messagesent += cloud_messagesent
    cm.events.cloud_messagereceived += cloud_messagereceived
    cm.events.cloud_command += cloud_command
    cm.initializecloudmanager()
    lcd.lcd_clear()
    #lcd.data_print("Cloud Manager",0,0)
    #lcd.data_print("Started",0,1)
    sleep(1)
    lcd.lcd_clear()
    #lcd.data_print("Cloud Manager",0,0)
    #lcd.data_print("Started sync",0,1)
    sleep(1)
    cm.startdatasync()
        
        
def StartHardwareManager(hardwares):
    lcd.lcd_clear()
    lcd.data_print("Device Starting",0,0)
    lcd.data_print("Wait",6,1)
    sleep(2)
    lcd.lcd_clear()
    lcd.data_print("RFID Starting   ",0,0)
    lcd.data_print("wait....",4,1)
    sleep(2)
    hardmamanger.events.hardware_started += hardware_started
    hardmamanger.events.hardware_stopped += hardware_stopped
    hardmamanger.events.hardware_disabled += hardware_disabled
    hardmamanger.events.hardware_exception += hardware_exception
    hardmamanger.startmanager(hardwares)
          
        
def StartLiveFeedManager():

   
    lm.initializelivefeeddmanager()
    lm.startlivefeedsync()

if __name__ == '__main__':
    # Register classes for hardware
    #deviceManager.register('dummy',dummyhardware)
    #deviceManager.register('gps',gpshardware)
    deviceManager.register('rfid',rfidhardware)
    deviceManager.register('shut',shuthardware)
    #deviceManager.register('panic',panichardware)
    #deviceManager.register('camera',camerahardware)
    #deviceManager.register('accelerometer',accelerohardware)
    
    manager = deviceManager()
    manager.start()
    
    hardwares = {}
    #hardwares['dummy'] = manager.dummy()
    #hardwares['gps'] = manager.gps()
    hardwares['rfid'] = manager.rfid()
    hardwares['shut'] = manager.shut()
    #hardwares['panic'] = manager.panic()
    #hardwares['camera'] = manager.camera()
    #hardwares['accelerometer'] = manager.accelerometer()
    
    StartHardwareManager(hardwares)
    
    #Stopdummydevice(hardwares)
    StartCloudManager()

    
   

    
    
        

   

