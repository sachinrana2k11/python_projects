from manager.handler import database
from time import  sleep
from datetime import datetime
from configuration.config import confi
from Gateway_Sensors.MODBUS import MODBUS
from logs.logmanager import log
import multiprocessing
from Gateway_Sensors.IO_SENSOR import IO_SENSOR
import os
LOG = log()
config = confi()
Data_base = database()
MOD = MODBUS()
IO = IO_SENSOR()

def feed_data_database(): #process for fetch data from hardware and feed it to databse
    LOG.DEBUG("FEEDING data to databse started-: "+str(os.path.basename(__file__)))
    while True:
        fetch_datetimestamp = get_datetime()
        data = MOD.get_data()
        Data_base.Save_In_DataBase(data, fetch_datetimestamp[0],fetch_datetimestamp[1],'MODBUS')
        print("Payload save in databse is :- "+ data)
        sleep(config.FETCH_TIME)

def get_data_io_sensor():
    LOG.DEBUG("FEEDING IO_SENSORS data to databse started-: " + str(os.path.basename(__file__)))
    while True:
        DATETIME_STAMP = get_datetime()
        data = IO.get_io_sensor_data()
        Data_base.Save_In_DataBase(data, DATETIME_STAMP[0],DATETIME_STAMP[1],'IO_SENSOR')
        print("Payload save in databse")
        sleep(config.FETCH_TIME)

def sync_data(): #process for sync data from database to aws iot
    Data_base.load_credential()
    Data_base.connect_server()
    while True:
        Data_base.send_AWS(config.AWS_TOPIC)
        sleep(config.SYNC_TIME)

def get_datetime():
    DateString = "%Y-%m-%d"
    TimeString = "%H:%M:%S"
    date = str(datetime.now().strftime(DateString))
    time = str(datetime.now().strftime(TimeString))
    return date,time

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=sync_data) # 1st process
    p2 = multiprocessing.Process(target=feed_data_database) # 2nd process
    p3 = multiprocessing.Process(target=get_data_io_sensor) # 2nd process
    p1.start()
    p2.start()
    p3.start()


