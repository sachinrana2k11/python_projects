from peewee import *

proxy = Proxy()

class devicedata(Model):
    id = TextField(primary_key=True)
    gatewayid = TextField()
    payload = TextField()
    timestamp = TextField()
    orgid = TextField()
    devicetype = TextField()
    synced = IntegerField(default=0)

    class Meta:
        database = proxy
