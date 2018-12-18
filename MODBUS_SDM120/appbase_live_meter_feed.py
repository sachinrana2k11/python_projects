import sys

import minimalmodbus
import time
import uuid
import requests,random
import json
import demjson
import datetime
MeterID = "SDM120"
url = "https://ohiRuOFiH:8c6861f1-d1dc-4322-8819-c072f5bfe9b1@scalr.api.appbase.io/arnowa/pointvalues/_bulk"
'''rs485 = minimalmodbus.Instrument('COM11', 1)
rs485.serial.baudrate = 2400 # can be 9600, or another rate
rs485.serial.bytesize = 8
rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
rs485.serial.stopbits = 1
rs485.serial.timeout = 1
rs485.debug = False
rs485.mode = minimalmodbus.MODE_RTU
print(rs485)'''
while 1:
    Volts = random.randint(100,220)#rs485.read_float(0, functioncode=4, numberOfRegisters=2)
    Current = random.randint(1,10)#rs485.read_float(6, functioncode=4, numberOfRegisters=2)
    Active_Power = random.randint(100,1000)#rs485.read_float(12, functioncode=4, numberOfRegisters=2)
    Apparent_Power = random.randint(100,500)#rs485.read_float(18, functioncode=4, numberOfRegisters=2)
    Reactive_Power = random.randint(100,500)#rs485.read_float(24, functioncode=4, numberOfRegisters=2)
    Power_Factor = random.randint(0,1)# rs485.read_float(30, functioncode=4, numberOfRegisters=2)
    Phase_Angle = random.randint(0,180)#rs485.read_float(36, functioncode=4, numberOfRegisters=2)
    Frequency = random.randint(50,60)#rs485.read_float(70, functioncode=4, numberOfRegisters=2)
    Import_Active_Energy = random.randint(500,1000)#rs485.read_float(72, functioncode=4, numberOfRegisters=2)
    Export_Active_Energy = random.randint(500,2000)#rs485.read_float(74, functioncode=4, numberOfRegisters=2)
    Import_Reactive_Energy = random.randint(200,500)#rs485.read_float(76, functioncode=4, numberOfRegisters=2)
    Export_Reactive_Energy = random.randint(100,400)#rs485.read_float(78, functioncode=4, numberOfRegisters=2)
    Total_Active_Energy = random.randint(5000,8000)#rs485.read_float(342, functioncode=4, numberOfRegisters=2)
    Total_Reactive_Energy = random.randint(3000,5000)#rs485.read_float(344, functioncode=4, numberOfRegisters=2)
    DATETIME_STAMP = str(datetime.datetime.now().utcnow().isoformat())

    # Array of data objects
    dataArray = [
          {
          #"id": str(uuid.uuid4()),
          "meter": MeterID,
          "name": "Volts",
          "value": Volts,
          "timestamp": DATETIME_STAMP
          },
          {
          #"id": str(uuid.uuid4()),
          "meter": MeterID,
          "name": "Current",
          "value": Current,
          "timestamp": DATETIME_STAMP
          },
          {
            #"id": str(uuid.uuid4()),
            "meter": MeterID,
             "name": "Active_Power",
             "value": Active_Power,
             "timestamp": DATETIME_STAMP
          },
        {
          # "id": str(uuid.uuid4()),
          "meter": MeterID,
          "name": "Apparent_Power",
          "value": Apparent_Power,
          "timestamp": DATETIME_STAMP
        },
        {
           # "id": str(uuid.uuid4()),
            "meter": MeterID,
            "name": "Reactive_Power",
            "value": Reactive_Power,
            "timestamp": DATETIME_STAMP
        },
        {
            #"id": str(uuid.uuid4()),
            "meter": MeterID,
            "name": "Power_Factor",
            "value": Power_Factor,
            "timestamp": DATETIME_STAMP
        },
        {
            #"id": str(uuid.uuid4()),
            "meter": MeterID,
            "name": "Phase_Angle",
            "value": Phase_Angle,
            "timestamp": DATETIME_STAMP
        },
        {
            #"id": str(uuid.uuid4()),
            "meter": MeterID,
            "name": "Frequency",
            "value": Frequency,
            "timestamp": DATETIME_STAMP
        },
        {
            #"id": str(uuid.uuid4()),
            "meter": MeterID,
            "name": "Total_Active_Energy",
            "value": Total_Active_Energy,
            "timestamp": DATETIME_STAMP
        },

        {
            #"id": str(uuid.uuid4()),
            "meter": MeterID,
            "name": "Total_Reactive_Energy",
            "value": Total_Reactive_Energy,
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

    except:
        e = sys.exc_info()[0]
        print("try next time " + str(e))
        continue
    time.sleep(1)