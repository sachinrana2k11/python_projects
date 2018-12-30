import demjson
import requests
from playhouse.shortcuts import model_to_dict
from database import models as md
from configuration.config import confi
import sys,json,uuid,time
import peewee as pw
from logs.logmanager import log
import os

class database():
    def __init__(self):
        try:
            self.LOG = log()
            self.config = confi()
            self.localdb = pw.SqliteDatabase(self.config.DATABASE_PATH)
            md.proxy.initialize(self.localdb)
            md.devicedata.create_table(True)
            self.data = md.devicedata()
        except:
                e = sys.exc_info()[0]
                self.LOG.ERROR("FAILLED TO INIT TABLE " + str(os.path.basename(__file__)) + str(e))  # error logs
                print("EXCEPTION IN INITINIT TABLE" + str(e))
                pass


    def Save_In_DataBase(self,data,timestamp,device):
        try:
            self.data.timestamp = timestamp
            self.data.payload = data
            self.data.id = uuid.uuid4()
            self.data.devicetype = device
            self.data.gatewayid = self.config.DEVICE_ID
            self.data.orgid = self.config.ORG_ID
            self.data.save(force_insert=True)
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO SAVE DATA IN DATABASE ,DATABASE ERROR" + str(os.path.basename(__file__)) + str(e))  # error logs
            print("EXCEPTION IN SAVE DATA IN DATABSE CHECK DATABASE MODELS- " + str(e))
            pass

    def update_synced(self, msgid):
        try:
            #print(md.devicedata.id,msgid)
            query = md.devicedata.update(synced=1).where((md.devicedata.id == msgid))
            query.execute()
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO UPDATE SYNCED DATA TO 0---1" + str(os.path.basename(__file__)) + str(e))  # error logs
            print("EXCEPTION IN UPDATING SYNCED DATA- " + str(e))
            pass

    def sync_data(self):
        try:
            #records = self.check_data_base()
            #print(records)
            # if records < 25:
            for data in md.devicedata().select().order_by(md.devicedata.timestamp.asc()).where(md.devicedata.synced == 0).limit(5):
                try:
                    data_raw = model_to_dict(data)
                    data_to_send = self.get_data_value(data_raw)
                    print(data_to_send)
                    ack = self.send_data_elastic(data_to_send)
                    if ack == True:
                        #print("PUBLISHING  DATA TO CLOUD-:" + str(data_to_send))
                        msg_id = data.id
                        self.update_synced(msg_id)
                except:
                    e = sys.exc_info()[0]
                    self.LOG.ERROR("FAILLED TO SEND DATA TO THE SERVER" + str(os.path.basename(__file__)) + str(e))  # error logs
                    print("EXCEPTION IN SENDING DATA TO AWS SERVER - " + str(e))
                    continue

        except:
                e = sys.exc_info()[0]
                self.LOG.ERROR("FAILLED TO SEND DATA TO AWS IOT" + str(os.path.basename(__file__)) + str(e))  # error logs
                print("EXCEPTION IN SENDING  DATA TO AWS - " + str(e))
                pass


    def check_data_base(self):
        record_list= []
        for data in md.devicedata().order_by(md.devicedata.timestamp.asc()).where(md.devicedata.synced == 0):
            record_list.append(data)
        return len(record_list)

    def get_data_value(self,data_raw):
        type = data_raw['devicetype']
        if type == 'MODBUS':
            # Array of data objects
            raw_payload = json.loads(data_raw['payload'])

            dataArray = []
            for i in raw_payload:
                raw_form = {"meter": data_raw['gatewayid'], "name": i, "value": raw_payload[i], "timestamp": data_raw['timestamp']}
                dataArray.append(raw_form)
            payload = ""

            # Creating request body
            for data in dataArray:
                # Pushing the operation and _id for each request
                type = {
                    "index": {
                        # "_id": data['id']
                    }
                }
                payload += demjson.encode(type) + "," + "\n" + demjson.encode(data) + "\n"
            return payload
        elif type == 'IO_SENSOR':
            # Array of data objects
            raw_payload = json.loads(data_raw['payload'])

            dataArray = []
            for i in raw_payload:
                raw_form = {"Sensorid": data_raw['gatewayid'], "name": i, "value": raw_payload[i], "timestamp": data_raw['timestamp']}
                dataArray.append(raw_form)
            payload = ""

            # Creating request body
            for data in dataArray:
                # Pushing the operation and _id for each request
                type = {
                    "index": {
                        # "_id": data['id']
                    }
                }
                payload += demjson.encode(type) + "," + "\n" + demjson.encode(data) + "\n"
            return payload




    def send_data_elastic(self,payload):
        headers = {
            # 'Authorization': "Basic bWVxUmY4S0pDOjY1Y2MxNjFhLTIyYWQtNDBjNS1hYWFmLTVjMDgyZDVkY2ZkYQ==",
            'Content-Type': "application/x-ndjson"
        }

        # Bulk request including the index method and all data objects
        try:
            response = requests.request("POST",self.config.ELASTIC_ADDRESS, data=payload, headers=headers)
            #print(payload)
            parsed = json.loads(response.text)
            #print(json.dumps(parsed, indent=4, sort_keys=True))
            print("data send successfully")
            return True

        except:
            e = sys.exc_info()[0]
            print("try next time " + str(e))
            return False


