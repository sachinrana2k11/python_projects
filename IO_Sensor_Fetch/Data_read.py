import sys

from serial import Serial
from termcolor import colored


class IO_data:
    def __init__(self,Port,Baud_Rate):
        self.port = Port
        self.baud = Baud_Rate
        self.ser = Serial(
            port=self.port,  # Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
            baudrate=self.baud,
            timeout=1
        )

    def read_data(self):
        try:
            temp_data = self.ser.readline()
            uart_data = temp_data.decode()
            return uart_data
        except:
            e = sys.exc_info()[0]
            print(colored("\tTask-1,cannot fetch data from UART ERROR" + str(e), "red"))
            pass

