import random,datetime
import time

DateString = "%Y-%m-%d"
TimeString = "%H:%M:%S"

class handle:
    def __init__(self):
        print("constructor init")

    def get_data(self):
        form = {
            "datestamp":str(datetime.datetime.now().strftime(DateString)),
            "timestamp":str(datetime.datetime.now().strftime(TimeString)),
            "voltage":random.randint(250,300),
            "current": random.randint(20, 50)
        }
        return form

