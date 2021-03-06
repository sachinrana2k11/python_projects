import multiprocessing
import re
import sys
import time
import requests
import json
import demjson
import datetime
import serial
from termcolor import colored
from Data_read import IO_data
#------------------------------configurations-------------------------------------------
url = "https://ohiRuOFiH:8c6861f1-d1dc-4322-8819-c072f5bfe9b1@scalr.api.appbase.io/arnowa/pointvalues/_bulk"
data_send_time  = 0.5 # sec
data_fetch_time = 0.1 #sec
#-------------------------------UART config---------------------------------------------
Baud_Rate = 115200
PORT = 'COM19'
#------------------------------configurations-------------------------------------------
#io_data = IO_data(PORT,Baud_Rate)

def get_data():
     #temp_msg = "ID:1:TS:23143:TF:60.79:RH:44.00"
     ser = serial.Serial("COM19", 115200)
     temp_msg = ser.readline().decode()
     msg = temp_msg.strip()
     temp5 = re.sub(r'\r\n', '', msg)
     return temp5


def decode_data(temp_data):
    temp1 = temp_data
    temp2 = temp1.split(":")
    #print(temp2)
    data_temp = dict(zip(temp2[0::2],temp2[1::2]))
    return data_temp

def task_getdata(one,q):
    while 1:
        data = get_data()
        final_data = decode_data(data)
        #print(len(final_data))
        if len(final_data) > 3:
            if q.full() == False:
                q.put(final_data)
                print("Task-1, Data inserted in queue is :- "+ str(final_data))
                time.sleep(data_fetch_time)
            elif q.full() == True:
                print("Task-1, Queue is full..wait for data pipe to free")
                time.sleep(data_fetch_time)


def task_senddata(two,q):
    while 1:
        if q.empty() == False:
            DATETIME_STAMP = str(datetime.datetime.now().utcnow().isoformat())
            print("\tTask-2,Data fetched from Queue is :-"+ str(q.get()))
            queue_data = q.get()
            # Array of data objects
            dataArray = [
                  {
                  #"id": str(uuid.uuid4()),
                  #"NodeID": queue_data['ID'],
                  "meter": "IO123",
                  "name": "Temprature",
                  "value": float(queue_data['TF']),
                  "timestamp": DATETIME_STAMP
                  },
                  {
                  #"id": str(uuid.uuid4()),
                  #"NodeID": queue_data['ID'],
                  "meter": "IO123",
                  "name": "Humidity",
                  "value": float(queue_data['RH']),
                  "timestamp": DATETIME_STAMP
                  }
            ]
            payload = ""

            # Creating request body
            for data in dataArray:
              # Pushing the operation and _id for each request
              type = {
                "index": {
                 # "_id": data['id']
                }
              }
              payload += demjson.encode(type) +","+ "\n" + demjson.encode(data) + "\n"

            headers = {
                  #'Authorization': "Basic bWVxUmY4S0pDOjY1Y2MxNjFhLTIyYWQtNDBjNS1hYWFmLTVjMDgyZDVkY2ZkYQ==",
                  'Content-Type': "application/x-ndjson"
                }

            # Bulk request including the index method and all data objects
            try:
                response = requests.request("POST", url, data=payload, headers=headers)
                print(payload)
                parsed = json.loads(response.text)
                print(json.dumps(parsed, indent=4, sort_keys=True))
                print(colored("\tTask-2, Data sends sucessfully-:","green"))
                time.sleep(data_send_time)

            except:
                e = sys.exc_info()[0]
                print(colored("\tTask-2,try next time " + str(e),"red"))
                continue
                time.sleep(data_send_time)
        elif q.empty() == True:
            print(colored("\tTask-2, Queue is empty wait for data to be feed","red"))
            time.sleep(data_send_time+0.5)

if __name__ == '__main__':
    one = 1 #dummy arguments
    two = 2 #dummy arguments
    q = multiprocessing.Queue(100)
    p1 = multiprocessing.Process(target=task_getdata,args=(one,q)) # 1st process
    p2 = multiprocessing.Process(target=task_senddata,args=(two,q)) # 2nd process
    p1.start()
    p2.start()
    p1.join()
    p2.join()