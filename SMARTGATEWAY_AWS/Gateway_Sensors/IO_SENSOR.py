import json
import re

import serial

class IO_SENSOR:
    def get_data(self):
        temp_msg = "ID:1:TS:23143:TF:60.79:RH:44.00"
        #ser = serial.Serial("COM19", 115200)
        #temp_msg = ser.readline().decode()
        msg = temp_msg.strip()
        temp5 = re.sub(r'\r\n', '', msg)
        return temp5


    def decode_data(self,temp_data):
        temp1 = temp_data
        temp2 = temp1.split(":")
        # print(temp2)
        data_temp = dict(zip(temp2[0::2], temp2[1::2]))
        return data_temp

    def get_io_sensor_data(self):
        while 1:
            data = self.get_data()
            final_data = self.decode_data(data)
            if len(final_data) > 3:
                return json.dumps(final_data)
