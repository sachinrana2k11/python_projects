from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['SACHIN_TEST_DB']
DeviceData = db['DEVICEDATA']
Config = db['CONFIG_DB']
mydict = { "name": "John", "address": "Highway 37" }
x = DeviceData.insert_one(mydict)
y = Config.insert_one(mydict)
print(x.acknowledged,x.inserted_id)
print(y.acknowledged,y.inserted_id)




















# import json
# import time
# import requests
# form={
#   "username": "admin",
#   "password": "12345",
#   "data": "value3"
# }
# while 1:
#     temp =requests.post('https://4r3mpyewwj.execute-api.us-east-1.amazonaws.com/test',data=json.dumps(form))
#     #temp = requests.get('https://4r3mpyewwj.execute-api.us-east-1.amazonaws.com')
#     print(temp.text)
#     time.sleep(5)
