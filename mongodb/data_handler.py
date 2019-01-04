from playhouse.shortcuts import model_to_dict
import models as md
import peewee as pw
import uuid
from datetime import datetime

class data_handler:
    def __init__(self):
        self.localdb = pw.SqliteDatabase('Data.db')
        md.proxy.initialize(self.localdb)
        md.DEVICE_DATA.create_table(True)
        md.COMMUNICATION_CONFIG.create_table(True)
        md.NODE_CONFIG.create_table(True)
        md.CLOUD_CONFIG.create_table(True)
        self.device_data = md.DEVICE_DATA()
        self.communication = md.COMMUNICATION_CONFIG()
        self.node = md.NODE_CONFIG()
        self.cloud = md.CLOUD_CONFIG()
        self.DateString = "%Y-%m-%d"
        self.TimeString = "%H:%M:%S"

    def update_COMMUNICATION_CONFIG(self,temp):
        self.communication.id = uuid.uuid4()
        self.communication.DEVICE_PORT = temp["DEVICE_PORT"]
        self.communication.BAUD_RATE =temp["BAUD_RATE"]
        self.communication.DEVICE_IP=temp["DEVICE_IP"]
        self.communication.DEVICE_IP_PORT = temp["DEVICE_IP_PORT"]
        self.communication.DATE_STAMP = str(datetime.now().strftime(self.DateString))
        self.communication.TIME_STAMP = str(datetime.now().strftime(self.TimeString))
        self.communication.COMMUNI_TYPE =temp["COMMUNI_TYPE"]
        self.communication.DEVICE_TYPE = temp["DEVICE_TYPE"]
        self.communication.save(force_insert=True)

    def update_NODE_CONFIG(self,temp):
        self.node.id = uuid.uuid4()
        self.node.SLAVE_ID = temp["SLAVE_ID"]
        self.node.SLAVE_NAME = temp["SLAVE_NAME"]
        self.node.REGISTERS = temp["REGISTERS"]
        self.node.DATE_STAMP = str(datetime.now().strftime(self.DateString))
        self.node.TIME_STAMP = str(datetime.now().strftime(self.TimeString))
        self.node.TYPE = temp["TYPE"]
        self.node.save(force_insert=True)


    def update_CLOUD_CONFIG(self,temp):
        self.cloud.id = uuid.uuid4()
        self.cloud.ORG = temp["ORG"]
        self.cloud.TYPE = temp["TYPE"]
        self.cloud.DEVICE_ID = temp["DEVICE_ID"]
        self.cloud.AUTH_METHOD = temp["AUTH_METHOD"]
        self.cloud.AUTH_TOKKEN = temp["AUTH_TOKKEN"]
        self.cloud.CLEAR_SESSION = temp["CLEAR_SESSION"]
        self.cloud.DATE_STAMP = str(datetime.now().strftime(self.DateString))
        self.cloud.TIME_STAMP = str(datetime.now().strftime(self.TimeString))
        self.cloud.save(force_insert=True)

    def get_COMMUNICATION_CONFIG(self):
        for data in md.COMMUNICATION_CONFIG().select().order_by(md.COMMUNICATION_CONFIG.DATE_STAMP.desc() and md.COMMUNICATION_CONFIG.TIME_STAMP.desc()).limit(1):
            return(model_to_dict(data))


    def get_NODE_CONFIG(self):
        for data in md.NODE_CONFIG().select().order_by(md.NODE_CONFIG.DATE_STAMP.desc() and md.NODE_CONFIG.TIME_STAMP.desc()).limit(1):
            return(model_to_dict(data))



    def get_CLOUD_CONFIG(self):
        for data in md.CLOUD_CONFIG().select().order_by(md.CLOUD_CONFIG.DATE_STAMP.desc() and md.CLOUD_CONFIG.TIME_STAMP.desc()).limit(1):
            temp = model_to_dict(data)
            temp1 = {"org": temp["ORG"],
                         "type": temp["TYPE"],
                         "id": temp["DEVICE_ID"],
                         "auth-method": temp["AUTH_METHOD"],
                         "auth-token": temp["AUTH_TOKKEN"],
                         "clean-session":temp["CLEAR_SESSION"]
  }
            return temp1

