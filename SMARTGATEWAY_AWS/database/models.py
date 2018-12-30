from peewee import *

proxy = Proxy()

class devicedata(Model):
    id = TextField(primary_key=True)
    deviceid = TextField()
    payload = TextField()
    datestamp = TextField()
    timestamp = TextField()
    devicetype = TextField()
    orgid = TextField()
    synced = IntegerField(default=0)

    class Meta:
        database = proxy
