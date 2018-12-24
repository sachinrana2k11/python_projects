from playhouse.shortcuts import model_to_dict
from database import models as md
from configuration.config import confi
import sys,json,uuid,time
import peewee as pw
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from logs.logmanager import log
import os

class database():
    def __init__(self):
        try:
            self.records_list = []
            self.LOG = log()
            self.config = confi()
            self.localdb = pw.SqliteDatabase(self.config.DATABASE_PATH)
            md.proxy.initialize(self.localdb)
            md.devicedata.create_table(True)
            self.data = md.devicedata()
            self.myMQTTClient = AWSIoTMQTTClient(self.config.DEVICE_ID)
            print("INITIALIZING DEVICE ON AWS SERVER")
            self.myMQTTClient.configureEndpoint(self.config.AWS_ARN, self.config.AWS_PORT)
            print("CONNECTED WITH AWS ENDPOINT WITH VALID PORT ")
        except:
                e = sys.exc_info()[0]
                self.LOG.ERROR("FAILLED TO INIT AWS IOT" + str(os.path.basename(__file__)) + str(e))  # error logs
                print("EXCEPTION IN INIT AWS IOT CHECK INTERNET CONNECTIVITY - " + str(e))
                pass


    def Save_In_DataBase(self,payload,date,time):
        try:
            self.data.timestamp = time
            self.data.datestamp = date
            self.data.payload = payload
            self.data.id = uuid.uuid4()
            self.data.deviceid = self.config.DEVICE_ID
            self.data.orgid = self.config.ORG_ID
            self.data.save(force_insert=True)
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO SAVE DATA IN DATABASE ,DATABASE ERROR" + str(os.path.basename(__file__)) + str(e))  # error logs
            print("EXCEPTION IN SAVE DATA IN DATABSE CHECK DATABASE MODELS- " + str(e))
            pass

    def load_credential(self):
        try:
            self.certRootPath = self.config.CERT_PATH
            self.myMQTTClient.configureCredentials("{}root-ca.pem".format(self.certRootPath), "{}cloud.pem.key".format(self.certRootPath),"{}cloud.pem.crt".format(self.certRootPath))
            print("APPLYING CERTIFICATE")
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO LOAD AWS CERTFICATE.." + str(os.path.basename(__file__)) + str(e))  # error logs
            print("EXCEPTION IN LOADING CERTIFICATE IN AWS IOT" + str(e))
            pass

    def connect_server(self):
        try:
            self.myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
            self.myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
            self.myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
            self.myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
            self.myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
            print("CONNECTING MQQT AWS SERVER")
            self.myMQTTClient.connect()
            print("CONNECTED TO MQQT IOT AWS")
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO CONNECT TO THE SERVER" + str(os.path.basename(__file__)) + str(e))  # error logs
            print("EXCEPTION IN CONNECTING AWS SERVER - " + str(e))
            pass

    def update_synced(self, msg_id):
        try:
            query = md.devicedata.update(synced=1).where((md.devicedata.id == msg_id))
            query.execute()
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("FAILLED TO UPDATE SYNCED DATA TO 0---1" + str(os.path.basename(__file__)) + str(e))  # error logs
            print("EXCEPTION IN UPDATING SYNCED DATA- " + str(e))
            pass

    def send_AWS(self,topic_path):
        try:
            records = self.check_data_base()
            if records < 25:
                for data in md.devicedata().select().order_by(md.devicedata.datestamp.desc() and md.devicedata.timestamp.asc()).where(md.devicedata.synced == 0).limit(5):
                    try:
                        self.myMQTTClient.publish(topic_path, json.dumps(model_to_dict(data)), self.config.QOS)
                        print("PUBLISHING  DATA TO AWS-:" + str(model_to_dict(data)))
                        msg_id = data.id
                        print(msg_id)
                        self.update_synced(msg_id)
                    except:
                        e = sys.exc_info()[0]
                        self.LOG.ERROR("FAILLED TO SEND DATA TO THE SERVER" + str(os.path.basename(__file__)) + str(e))  # error logs
                        print("EXCEPTION IN SENDING DATA TO AWS SERVER - " + str(e))
                        continue
            if records >25 and records <50:
                for data in md.devicedata().select().order_by(md.devicedata.datestamp.desc() and md.devicedata.timestamp.asc()).where(md.devicedata.synced == 0).limit(15):
                    try:
                        self.myMQTTClient.publish(topic_path, json.dumps(model_to_dict(data)), self.config.QOS)
                        print("PUBLISHING  DATA TO AWS-:" + str(model_to_dict(data)))
                        msg_id = data.id
                        print(msg_id)
                        self.update_synced(msg_id)
                    except:
                        e = sys.exc_info()[0]
                        self.LOG.ERROR("FAILLED TO SEND DATA TO THE SERVER" + str(os.path.basename(__file__)) + str(e))  # error logs
                        print("EXCEPTION IN SENDING DATA TO AWS SERVER - " + str(e))
                        continue
            if records >50 and records <75:
                for data in md.devicedata().select().order_by(md.devicedata.datestamp.desc() and md.devicedata.timestamp.asc()).where(md.devicedata.synced == 0).limit(25):
                    try:
                        self.myMQTTClient.publish(topic_path, json.dumps(model_to_dict(data)), self.config.QOS)
                        print("PUBLISHING  DATA TO AWS-:" + str(model_to_dict(data)))
                        msg_id = data.id
                        print(msg_id)
                        self.update_synced(msg_id)
                    except:
                        e = sys.exc_info()[0]
                        self.LOG.ERROR("FAILLED TO SEND DATA TO THE SERVER" + str(os.path.basename(__file__)) + str(e))  # error logs
                        print("EXCEPTION IN SENDING DATA TO AWS SERVER - " + str(e))
                        continue
            if records >75:
                for data in md.devicedata().select().order_by(md.devicedata.datestamp.desc() and md.devicedata.timestamp.asc()).where(md.devicedata.synced == 0).limit(50):
                    try:
                        self.myMQTTClient.publish(topic_path, json.dumps(model_to_dict(data)), self.config.QOS)
                        print("PUBLISHING  DATA TO AWS-:" + str(model_to_dict(data)))
                        msg_id = data.id
                        print(msg_id)
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
        for data in md.devicedata().select().order_by(md.devicedata.datestamp.desc() and md.devicedata.timestamp.asc()).where(md.devicedata.synced == 0):
            self.records_list.append(data)
        return len(self.records_list)

