import random
import ibmiotf.device,time,json
import minimalmodbus
from data_handler import data_handler
DateString = "%Y-%m-%d"
TimeString = "%H:%M:%S"
DATA = data_handler()
form = {}
def send_ACK(msg):
    print(msg)
    if client.publishEvent("status", "json", json.dumps(msg), 2):
        print("ACK sended to cloud")
    else:
        print("Can't send ACK")

def get_registers(Registers):
    temp = Registers.split(",")
    return temp

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)

    if(cmd.data["MSG_FOR"] == "COMMUNICATION"):
        DATA.update_COMMUNICATION_CONFIG(cmd.data)
        send_ACK(cmd.data)

    if (cmd.data["MSG_FOR"] == "NODE"):
        DATA.update_NODE_CONFIG(cmd.data)
        send_ACK(cmd.data)

    if (cmd.data["MSG_FOR"] == "CLOUD"):
        DATA.update_CLOUD_CONFIG(cmd.data)
        send_ACK(cmd.data)

    if (cmd.data["MSG_FOR"] == "PING"):
        send_ACK("ALIVE")

param = DATA.get_CLOUD_CONFIG()
client = ibmiotf.device.Client(param)
client.connect()
client.commandCallback = myCommandCallback
while 1:
    # com_temp = DATA.get_COMMUNICATION_CONFIG()
    # node_temp = DATA.get_NODE_CONFIG()
    # Registers = str(node_temp["REGISTERS"])
    # register_data  = get_registers(Registers)
    # #print(register_data)
    # # if(com_temp["COMMUNI_TYPE"]=="TCP"):
    # #     print("")
    # # if (com_temp["COMMUNI_TYPE"] == "SERIAL"):
    # #     rs485 = minimalmodbus.Instrument(com_temp["DEVICE_PORT"], node_temp["SLAVE_ID"])
    # #     rs485.serial.baudrate = com_temp["BAUD_RATE"]  # can be 9600, or another rate
    # #     rs485.serial.bytesize = 8
    # #     rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
    # #     rs485.serial.stopbits = 1
    # #     rs485.serial.timeout = 1
    # #     rs485.debug = False
    # #     rs485.mode = minimalmodbus.MODE_RTU
    # #     print(rs485)
    # # else:
    # #     print("Not found any valid configuration")
    # #print(com_temp)
    # time.sleep(1)
    # for x in range(0,len(register_data)):
    #     temp_data = register_data[x].split(":")
    #     #print(temp_data)
    #     R_name = temp_data[0]
    #     R_value = int(temp_data[1])
    #     #print(R_name,R_value)
    #     R_name_val = random.randint(0,50)#rs485.read_float(R_value,functioncode=4, numberOfRegisters=2)
    #     form[R_name] = R_name_val # making dict as per data
    #
    # print(form)
    # msg_send = client.publishEvent("status", "json", json.dumps(form), 2)
    # print("data sending -:" + str(form) + " " + str(msg_send))
    time.sleep(1);



