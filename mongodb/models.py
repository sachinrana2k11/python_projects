from peewee import *
proxy = Proxy()

class DEVICE_DATA(Model):
    id =  TextField(primary_key=True)
    DEVICE_ID = TextField()
    PAYLOAD = TextField()
    DATE_STAMP = TextField()
    TIME_STAMP = TextField()
    ORG_ID = TextField()
    APPLICATION_NAME = TextField()
    SYNCED = IntegerField(default=0)
    class Meta:
        database = proxy

class COMMUNICATION_CONFIG(Model):
    id = TextField(primary_key=True)
    DEVICE_PORT = TextField()
    BAUD_RATE = TextField()
    DEVICE_IP = TextField()
    DEVICE_IP_PORT =TextField()
    DATE_STAMP = TextField()
    TIME_STAMP = TextField()
    COMMUNI_TYPE = TextField()
    DEVICE_TYPE = TextField()
    #MSG_FOR = TextField()
    class Meta:
        database = proxy

class NODE_CONFIG(Model):
    id = TextField(primary_key=True)
    SLAVE_ID = TextField()
    SLAVE_NAME = TextField()
    REGISTERS = TextField()
    DATE_STAMP = TextField()
    TIME_STAMP = TextField()
    TYPE = TextField()
    #MSG_FOR =TextField()
    class Meta:
        database = proxy

class CLOUD_CONFIG(Model):
    id = TextField(primary_key=True)
    ORG = TextField()
    TYPE = TextField()
    DEVICE_ID = TextField()
    AUTH_METHOD = TextField()
    AUTH_TOKKEN = TextField()
    CLEAR_SESSION = TextField()
    DATE_STAMP = TextField()
    TIME_STAMP = TextField()
    #MSG_FOR = TextField()
    class Meta:
        database = proxy
