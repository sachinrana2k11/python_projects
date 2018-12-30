import json
import random

import minimalmodbus,sys,os # minumul modbus library for reading modbus data
from configuration.config import confi
from logs.logmanager import log
class MODBUS1:
    def __init__(self):
        try:
            self.LOG = log() #init logs
            self.config = confi() # init config
            '''self.MOD = minimalmodbus.Instrument(self.config.PORT, self.config.SLAVE_ID) #slave id define
            self.MOD.serial.baudrate = self.config.BAUD_RATE # baud rate define
            self.MOD.serial.bytesize = 8 # byte size define
            self.MOD.serial.parity = minimalmodbus.serial.PARITY_NONE # parity define
            self.MOD.serial.stopbits = 1 #stop bits define
            self.MOD.serial.timeout = 1 # time out define
            self.MOD.debug = False # debug define
            self.MOD.mode = minimalmodbus.MODE_RTU #Mode define'''
            self.LOG.DEBUG("MODBUS Config loaded" + str(os.path.basename(__file__))) #log for debug
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("Failled to load modbus config" + str(os.path.basename(__file__))+ str(e)) #exception for error
            print("Could not init MODBUS class - " + str(e))


    def get_data(self): #define as per register value get data from modbus
        try:
            '''Volts = self.MOD.read_float(self.config.Voltage_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Current = self.MOD.read_float(self.config.Current_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Active_Power = self.MOD.read_float(self.config.Active_Power_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Apparent_Power = self.MOD.read_float(self.config.Apparent_Power_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Reactive_Power = self.MOD.read_float(self.config.Reactive_Power_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers2)
            Power_Factor = self.MOD.read_float(self.config.Power_Factor_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Phase_Angle = self.MOD.read_float(self.config.Phase_Angle_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Frequency = self.MOD.read_float(self.config.Frequency_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Import_Active_Energy = self.MOD.read_float(self.config.Import_Active_Energy_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Export_Active_Energy = self.MOD.read_float(self.config.Export_Active_Energy_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Import_Reactive_Energy = self.MOD.read_float(self.config.Import_Reactive_Energy_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Export_Reactive_Energy = self.MOD.read_float(self.config.Export_Reactive_Energy_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Total_Active_Energy = self.MOD.read_float(self.config.Total_Active_Energy_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
            Total_Reactive_Energy = self.MOD.read_float(self.config.Total_Reactive_Energy_REG, functioncode=self.config.Function_Code, numberOfRegisters=self.config.No_Registers)
'''
            form = {
                "Volts": random.randint(220,250),
                "Current": random.randint(0,10),
                "Active_Power": random.randint(100,500),
                "Apparent_Power": random.randint(100,300),
                "Reactive_Power": random.randint(250,300),
                "Power_Factor": random.randint(0,1),
                "Phase_Angle": random.randint(0,180),
                "Frequency": random.randint(50,60),
                "Import_Active_Energy": random.randint(100,250),
                "Export_Active_Energy": random.randint(100,250),
                "Import_Reactive_Energy": random.randint(100,250),
                "Export_Reactive_Energy": random.randint(100,250),
                "Total_Active_Energy": random.randint(10,250),
                "Total_Reactive_Energy": random.randint(10,250)
            } # make a data packet payload in dict object
            return str(json.dumps(form))
        except:
            e = sys.exc_info()[0]
            self.LOG.ERROR("Failled to fetch data from MODBUS" + str(os.path.basename(__file__)) + str(e)) # error logs
            print("Exception in getting data from modbus - " + str(e))
