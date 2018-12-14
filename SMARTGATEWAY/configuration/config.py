import configparser,os
from logs.logmanager import log
config = configparser.ConfigParser()
config.read('configuration\\config.ini')

class confi:
    def __init__(self):
        self.LOG = log()
        self.AWS_ARN = str(config['AWS']['AWS_ARN'])
        self.AWS_PORT = int(config['AWS']['AWS_PORT'])
        self.AWS_TOPIC = str(config['AWS']['AWS_TOPIC'])
        self.QOS = int(config['AWS']['QOS'])
        self.CERT_PATH = str(config['AWS']['CERT_PATH'])
 # -------------------------database------------------------------------------------
        self.DATABASE_PATH= str(config['DATABASE']['DATABASE_PATH'])
        self.SYNC_TIME = int(config['DATABASE']['SYNC_TIME'])
        self.BATCH_SIZE = int(config['DATABASE']['BATCH_SIZE'])
        self.DEBUG_MODE = int(config['DATABASE']['DEBUG_MODE'])

        #--------------------------MODBUS--------------------------------------------------
        self.PORT = str(config['MODBUS']['PORT'])
        self.BAUD_RATE = int(config['MODBUS']['BAUD_RATE'])
        self.SLAVE_ID = int(config['MODBUS']['SLAVE_ID'])
        self.Function_Code = int(config['MODBUS']['Function_Code'])
        self.No_Registers = int(config['MODBUS']['No_Registers'])
        self.Voltage_REG = int(config['MODBUS']['Voltage_REG'])
        self.Current_REG = int(config['MODBUS']['Current_REG'])
        self.Active_Power_REG = int(config['MODBUS']['Active_Power_REG'])
        self.Apparent_Power_REG = int(config['MODBUS']['Apparent_Power_REG'])
        self.Reactive_Power_REG = int(config['MODBUS']['Reactive_Power_REG'])
        self.Power_Factor_REG = int(config['MODBUS']['Power_Factor_REG'])
        self.Phase_Angle_REG = int(config['MODBUS']['Phase_Angle_REG'])
        self.Frequency_REG = int(config['MODBUS']['Frequency_REG'])
        self.Import_Active_Energy_REG = int(config['MODBUS']['Import_Active_Energy_REG'])
        self.Export_Active_Energy_REG = int(config['MODBUS']['Export_Active_Energy_REG'])
        self.Import_Reactive_Energy_REG = int(config['MODBUS']['Import_Reactive_Energy_REG'])
        self.Export_Reactive_Energy_REG = int(config['MODBUS']['Export_Reactive_Energy_REG'])
        self.Total_Active_Energy_REG = int(config['MODBUS']['Total_Active_Energy_REG'])
        self.Total_Reactive_Energy_REG = int(config['MODBUS']['Total_Reactive_Energy_REG'])
        self.FETCH_TIME = int(config['MODBUS']['FETCH_TIME'])

        #--------------------------Device--------------------------------------------------
        self.DEVICE_ID = str(config['DEVICE']['DEVICE_ID'])
        self.ORG_ID = str(config['DEVICE']['ORG_ID'])
        self.RETRY_TIME = int(config['DEVICE']['RETRY_TIME'])
        self.LOG.DEBUG("Config file loaded : " + str(os.path.basename(__file__)))

