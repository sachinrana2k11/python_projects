from manager.handler import database
from time import  sleep
import datetime
from configuration.config import confi
from Gateway_Sensors.MODBUS import MODBUS
from Gateway_Sensors.IO_SENSOR import IO_SENSOR
from logs.logmanager import log
import multiprocessing
import os

#---------------------------------Init basic class and define objects----------------------------
LOG = log()
config = confi()
Data_base = database()
#---------------------------------Init basic class and define objects----------------------------


#---------------------------------Init hardware class and define objects----------------------------
MOD = MODBUS() #modbus class object
IO = IO_SENSOR()#IO sensor class object
#---------------------------------Init hardware class and define objects----------------------------



def get_data_modbus(): #process for fetch data from hardware and feed it to databse
    LOG.DEBUG("FEEDING modbus data to databse started-: "+str(os.path.basename(__file__)))
    while True:
        DATETIME_STAMP = get_timestamp()
        data = MOD.get_data()
        Data_base.Save_In_DataBase(data,DATETIME_STAMP,'MODBUS')
        print("Payload save in databse is :- "+ data)
        sleep(config.FETCH_TIME+1)


def get_data_io_sensor():
    LOG.DEBUG("FEEDING IO_SENSORS data to databse started-: " + str(os.path.basename(__file__)))
    while True:
        DATETIME_STAMP = get_timestamp()
        data = IO.get_io_sensor_data()
        Data_base.Save_In_DataBase(data, DATETIME_STAMP, 'IO_SENSOR')
        print("Payload save in databse is :- " + str(data))
        sleep(config.FETCH_TIME)




def sync_data(): #process for sync data from database to aws iot
    while True:
        Data_base.sync_data()
        sleep(config.SYNC_TIME)

def get_timestamp():
    temp_time = str(datetime.datetime.now().utcnow().isoformat())
    return temp_time

if __name__ == '__main__':
    task_list = [get_data_modbus, get_data_io_sensor]
    i = 0
    while (i < len(task_list)):
        fnc1 = str(task_list[i])
        print(fnc1)
        temp1 = str('P')
        temp2 = str(i)
        temp3 = temp1+temp2
        temp3 = multiprocessing.Process(target=task_list[i])
        temp3.start()
        i = i+1
    # p1 = multiprocessing.Process(target=get_data_modbus) # 1st process
    # p2 = multiprocessing.Process(target=get_data_io_sensor) # 2nd process
    # p1.start()
    # p2.start()
    #get_data_modbus()
    #get_data_io_sensor()
    #sync_data()


