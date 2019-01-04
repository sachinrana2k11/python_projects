#start from here sachin rana
import re
import sys
import ibmiotf.device,time,json
import minimalmodbus
import serial
port_modbus = 'COM5'
port_rf = 'COM20'
port_controller = ''
param = {"org": "3n4830",
         "type": "NODE",
         "id": "MODBUS2k18",
         "auth-method": "token",
         "auth-token": "_hcXXOFbYdj+4Q)oZZ",
         "clean-session":"true"
         }
# def write_data_hardware(data):
#     print(data['MSG'])
#     try:
#         ser.write(data['MSG'].encode())
#         print("data send to arduino : " + str(data['MSG']))
#     except:
#         e = sys.exc_info()[0]
#         print("Exception in Writing data to hardware -: " + str(e))
#         pass

def send_ACK(msg):
    print(msg)
    if client.publishEvent("status", "json", json.dumps(msg), 2):
        print("ACK sended to cloud")
    else:
        print("Can't send ACK")

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)
    send_ACK("data recived at gateway side")
    #write_data_hardware(cmd.data)
client = ibmiotf.device.Client(param)
client.connect()
client.commandCallback = myCommandCallback
'''ser = serial.Serial(port_controller,9600,timeout=1)'''
ser1 = serial.Serial(port_rf,9600,timeout=1)
if __name__ == '__main__':
    print("start the programm")
    '''rs485 = minimalmodbus.Instrument(port_modbus, 1)
    rs485.serial.baudrate = 2400 # can be 9600, or another rate
    rs485.serial.bytesize = 8
    rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
    rs485.serial.stopbits = 1
    rs485.serial.timeout = 1
    rs485.debug = False
    rs485.mode = minimalmodbus.MODE_RTU
    print(rs485)'''
    while 1:
        temp_data = ser1.readline().decode()
        msg = temp_data.strip()
        dht_data = re.sub(r'\r\n', '', msg)
        print(dht_data)
        temp1 = dht_data
        temp2 = temp1.split(":")
        # print(temp2)
        data_temp = dict(zip(temp2[0::2], temp2[1::2]))
        print(data_temp)
        # Volts = rs485.read_float(0, functioncode=4, numberOfRegisters=2)
        # Current = rs485.read_float(6, functioncode=4, numberOfRegisters=2)
        # Active_Power = rs485.read_float(12, functioncode=4, numberOfRegisters=2)
        # Frequency = rs485.read_float(70, functioncode=4, numberOfRegisters=2)
        form = {
            "voltage": 220,#round(Volts,0),
            "current": 22,#round(Current,1),
            "power": 56,#round(Active_Power,2),
            "frequency":89 #round(Frequency,0)
        }
        temp = client.publishEvent("status", "json", json.dumps(form), 2)
        print("data sending -:" + str(form) + " " + str(temp))
        time.sleep(1);
