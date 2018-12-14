import uuid
import requests,random
import json
import demjson
import datetime,time
MeterID = "SDM120"
#url = "https://ohiRuOFiH:8c6861f1-d1dc-4322-8819-c072f5bfe9b1@scalr.api.appbase.io/arnowa/pointvalue/_bulk"
url = "https://search-sachinrana2k18-vglslnc4s2vn26pd7gqq7i45pe.us-east-1.es.amazonaws.com/testapp/testvalue/_bulk"
while 1:
    DATETIME_STAMP = str(datetime.datetime.now())
    # Array of data objects
    dataArray = [
      {
      "id": str(uuid.uuid4()),
      "meter": MeterID,
      "name": "voltage",
      "value": random.randint(200,220),
      "time": DATETIME_STAMP
      },
      {
      "id": str(uuid.uuid4()),
      "meter": MeterID,
      "name": "current",
      "value": random.randint(0,10),
      "time": DATETIME_STAMP
      },
      {
        "id": str(uuid.uuid4()),
        "meter": MeterID,
      "name": "frequency",
      "value": random.randint(50,55),
      "time": DATETIME_STAMP
      },
      {
       "id": str(uuid.uuid4()),
      "meter": MeterID,
      "name": "power",
      "value": random.randint(0,500),
      "time": DATETIME_STAMP
      }
    ]

    payload = ""

    # Creating request body
    for data in dataArray:
      # Pushing the operation and _id for each request
      type = {
        "index": {
          "_id": data['id']
        }
      }
      payload += demjson.encode(type) + "\n" + demjson.encode(data) + "\n"



    headers = {
      #'Authorization': "Basic bWVxUmY4S0pDOjY1Y2MxNjFhLTIyYWQtNDBjNS1hYWFmLTVjMDgyZDVkY2ZkYQ==",
      'Content-Type': "application/x-ndjson"
    }

    # Bulk request including the index method and all data objects
    response = requests.request("POST", url, data=payload, headers=headers)
    print(payload)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    time.sleep(1)