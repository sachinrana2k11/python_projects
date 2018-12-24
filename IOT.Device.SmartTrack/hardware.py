from models import devicedata, basepayload,gpspayload,rfidpayload,shutpayload,panicpayload,camerapayload,acceleropayload
import json
import time
from helpers import ConfigHelper
import datetime
from helpers import *
import uuid,time
from events import Events
import serial
from managers import hardwareevents
from Adafruit_CharLCD import Adafruit_CharLCD
import picamera
import RPi.GPIO as GPIO
import os
from adxl345 import ADXL345

# hardware base class
class hardwarebase(object):
    """this is a base class for all different hardware helpers"""
    
   # log = LoggingHelper(ConfigHelper.logconfig.disabled, ConfigHelper.logconfig.logtoconsole)
    def __init__(self,name):
        
     try:   
        
        # Init objects & Default
        #--------------------------------------
        self.payload = basepayload()
        self.data = devicedata()
        self.started = False
        self.DateString = '%Y-%m-%d'
        self.TimeString = '%H:%M:%S'
        self.lcd = LCD()
        
		
       # self.logger = logger

        
        #--------------------------------------


        # Init configs
        #--------------------------------------
        
       
        # set the name
        self.name = name
        # Get the hardware id
        self.hardwareid = ConfigHelper.config[self.name]['HARDWARE_ID']
        # check if hardware is enabled or not
        self.enabled = ConfigHelper.hardwares[name]
        
        #--------------------------------------

     except:
          e = sys.exc_info()[0]
          print(e)
          #self.events.hardware_exception(e)
          return
         
     
    def inithardware(self):
        pass

    def start(self):
        
        # Set the started to True
        self.started = True
        
    def stop(self):
        """Stop the hardware"""
        print(self.name + ' stop called')
        self.started = False
    
       
    def getdata(self):
        pass

    def isstarted(self):
        """ Return the status of the hardware """
        return self.started

    def savedata(self):
        try:
           """ Saved the data to local storage """
           self.data.deviceid = ConfigHelper.deviceid
           self.data.id = uuid.uuid4()
           self.data.save(force_insert=True)
        except:
            e = sys.exc_info()[0]
            print(e)
            return
     
    def isenabled(self):
        
        return self.enabled;

    def enable(self):
        """ Enable hardware """
        self.enabled = True
        # Save the value in config file
        ConfigHelper.enabledevice(self.name)
   

    def disable(self):
        """ Disable hardware """
        self.enabled = False
        # Save the value
        ConfigHelper.disabledevice(self.name)
   
        
  
class gpshardware(hardwarebase):
   
    
    def __init__(self):
        hardwarebase.__init__(self,'GPS')
        #self.cam = camera()
        self.payload = gpspayload()
        self.serial1 = None
        #self.lcd.data_print("GPS Initialize..",0,0)
        #time.sleep(2)
        
        

    def start(self):
     try:
        print("Starting GPS Hardware ..")
        #self.lcd.data_print("GPS Started..",0,0)
        time.sleep(4)
        """ Read lat,long,speed from config """
        
        self.serial1 = serial.Serial(ConfigHelper.gpsconfig.Com_Port, ConfigHelper.gpsconfig.Baud_Rate, timeout=1)
        #self.cam.cmaera_start()
        super().start()
        self.getdata()
        
        self.started = True
     except:
         e = sys.exc_info()[0]
         print("1123"+str(e))
         return

    def stop(self):
        
        self.serial1 = None
        self.started = False
        print("Stopping GPS Hardware ..")

    def getdata(self):

       try:
          while self.isstarted():
                    a = str(self.serial1.readline())
                    data=a.split(",")
                    if data[0] == "b'$GPRMC":#for old gps
                    #if data[0] == "b'$GNRMC":#for new m8n gps
                          if data[2]=="A":
                              a=data[3]#raw lat
                              b=data[5]#raw lon
                              c=data[7]#raw speed
                              lati=float(a)/100
                              longi=float(b)/100
                              speed=float(data[7])*1.852
                              lati_int=int(lati)
                              longi_int=int(longi)
                              raw_lat=float(lati-lati_int)/60.0
                              raw_lon=float(longi-longi_int)/60.0
                              latitude=(lati_int+(raw_lat*100))
                              longitude=(longi_int+(raw_lon*100))
                              self.payload.latitude=str(format(latitude,'.6f'))
                              self.payload.longitude =str(format(longitude, '.6f'))
                              self.payload.speed =str(format(speed,'.1f'))
                              print(self.payload.latitude,self.payload.longitude,self.payload.speed+"-Km/h")
                              self.lcd.data_print("Speed-"+self.payload.speed+"-Km/h",0,0)
                              self.data.deviceid = ConfigHelper.deviceid
                              self.data.organizationid = ConfigHelper.orgid
                              self.data.routeid = ConfigHelper.routeid
                              self.data.hardwareid =ConfigHelper.gpsconfig.hardwareid
                              self.data.hardwaretype = 'GPS'
                              self.data.payload = self.payload.payloadjson()
                              today_date = str(datetime.datetime.now().strftime(self.DateString))
                              time_now = str(datetime.datetime.now().strftime(self.TimeString))
                              self.data.datestamp = today_date
                              self.data.timestamp = time_now
                              self.data.applicationname ='SmartTrack'
                              self.savedata()
                              time.sleep(ConfigHelper.gpsconfig.Refresh_Interval)
                          if data[2]=="V":
                             print("GPS data not Available..")
                             self.lcd.data_print("!!GPS signal..",0,0)
       except:
           e = sys.exc_info()[0]
           print("2"+str(e))
           pass


class rfidhardware(hardwarebase):
   
    
    def __init__(self):
        hardwarebase.__init__(self,'RFID')
        self.payload = rfidpayload()
        self.serial0 = None
        #self.lcd.data_print("RFID Initialize..",0,0)
        #time.sleep(2)
        

    def start(self):
        print("Starting RFID Hardware ..")
        self.lcd.data_print("RFID Started..",0,0)
        time.sleep(2)
        """ Read values from config """
        self.serial0 = serial.Serial(ConfigHelper.rfidconfig.Com_Port, ConfigHelper.rfidconfig.Baud_Rate, timeout=ConfigHelper.rfidconfig.Refresh_Interval)
        super().start()
        self.getdata()
        self.started = True
    def stop(self):
        
        self.serial0 = None
        self.started = False
        print("Stopping RFID Hardware ..")

    def getdata(self):

       
        while self.isstarted():
            time_now1 = str(datetime.datetime.now().strftime(self.TimeString))
            print(time_now1)
            self.lcd.lcd_clear()
            self.lcd.data_print("WELCOME",4,0)
            self.lcd.data_print(time_now1,4,1)    
            a = str(self.serial0.readline())
            if len(a)>10 and len(a)<16:
                data_raw = a.split("'")
                b = data_raw[1]
                print(b)
                self.payload.ID = str(b)

                print('RFID data recieved ' + self.payload.ID)
                #self.lcd.data_print("ID-"+self.payload.id,0,1) 
                
                self.data.deviceid = ConfigHelper.deviceid
                self.data.hardwareid = ConfigHelper.rfidconfig.hardwareid
                self.data.hardwaretype = 'RFID'
                self.data.payload = self.payload.payloadjson()
                self.data.organizationid = ConfigHelper.orgid
                self.data.routeid = ""
                today_date = str(datetime.datetime.now().strftime(self.DateString))

                time_now = str(datetime.datetime.now().strftime(self.TimeString))
                self.data.datestamp = today_date
                self.data.timestamp = time_now
                self.data.applicationname ='SmartID'
                self.savedata()
                self.lcd.data_print("Attendance Mark",0,0)
                self.lcd.data_print("successfully",2,1)
                time.sleep(0.5)
                self.lcd.data_print("                ",0,0)
                self.lcd.data_print("WELCOME",4,0)
            else:
                pass

class accelerohardware(hardwarebase):

   
    def __init__(self):
        hardwarebase.__init__(self,'ACCELEROMETER')
        self.payload = acceleropayload()
        self.serial0 = None
        #self.lcd.data_print("RFID Initialize..",0,1)

        time.sleep(1)
        self.adxl345 = ADXL345()

    def start(self):
        print("Starting Accelero-meter Hardware ..")
        #self.lcd.data_print("RFID  Started..",0,1)
        time.sleep(1)
        """ Read values from config """
        super().start()
        self.getdata()
        self.started = True
    def stop(self):
        self.started = False
        print("Stopping Accelero-meter Hardware ..")

    def getdata(self):
        while self.isstarted():
               axes = self.adxl345.getAxes(True)
               b = float('%.2f' % axes['x'])
               if b < - 1.2:
                  self.payload.value = str(b)
                  print(b)
                  print('accelerometer data recieved ' + self.payload.value)
                  self.data.deviceid = ConfigHelper.deviceid
                  self.data.hardwareid = ConfigHelper.acceleroconfig.hardwareid
                  self.data.hardwaretype = 'ACCELEROMETER'
                  self.data.payload = self.payload.payloadjson()
                  self.data.organizationid = ConfigHelper.orgid
                  self.data.routeid = ConfigHelper.routeid
                  today_date = str(datetime.datetime.now().strftime(self.DateString))
                  time_now = str(datetime.datetime.now().strftime(self.TimeString))
                  self.data.datestamp = today_date
                  self.data.timestamp = time_now
                  self.data.applicationname ='SmartTrack'
                  self.savedata()
               if b> 1.2:
                  self.payload.value = str(b)
                  print(b)
                  print('accelerometer data recieved ' + self.payload.value)
                  self.data.deviceid = ConfigHelper.deviceid
                  self.data.hardwareid = ConfigHelper.acceleroconfig.hardwareid
                  self.data.hardwaretype = 'ACCELEROMETER'
                  self.data.payload = self.payload.payloadjson()
                  self.data.organizationid = ConfigHelper.orgid
                  self.data.routeid = ConfigHelper.routeid
                  today_date = str(datetime.datetime.now().strftime(self.DateString))
                  time_now = str(datetime.datetime.now().strftime(self.TimeString))
                  self.data.datestamp = today_date
                  self.data.timestamp = time_now
                  self.data.applicationname ='SmartTrack'
                  self.savedata()

class shuthardware(hardwarebase):
    def __init__(self):
        hardwarebase.__init__(self,'SHUT')
        print("starting shutdown function ")
        """self.cam = camerahardware()"""
        self.gps = gpshardware()
        self.rfid = rfidhardware()
        self.payload = shutpayload()
        #self.dummy = dummyhardware()
        self.cam = camerahardware()
        GPIO.setmode(GPIO.BCM)
        self.a=0
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.buttonTime = 0
        
    def start(self):
        
        time.sleep(2)
        """self.cam.camera_live_images()"""
        super().start()
        self.getdata()
        """print("hello shut...")"""

    def getdata(self):
        while self.isstarted():
            button_state = GPIO.input(26)
            if button_state == True:
                self.buttonTime = self.buttonTime+1
                print(self.buttonTime)
                time.sleep(1)
            if(self.buttonTime >=3):
                print('Button Pressed...')
                #self.gps.stop()
                self.rfid.stop()
                #self.cam.stop()
                self.lcd.data_print("Shuting down.",0,0)
                os.system('shutdown now -h')
                #self.dummy.stop()
                self.buttonTime=0
                
            elif button_state == False:
                #print("hello")
                self.buttonTime=0
                #time.sleep(1)
                continue
            
            


            
class LCD:
    def __init__(self):
        self.lcd = Adafruit_CharLCD(25,24,23,17,21,22,16,2)


    def data_print(self,msg,a,b):
        #self.lcd.clear()
        self.lcd.set_cursor(a,b)
        self.lcd.message(msg)
    def lcd_clear(self):
        self.lcd.clear()
        


class camerahardware(hardwarebase):

    def __init__(self):
        hardwarebase.__init__(self,'CAMERA')
        self.payload = camerapayload()
        self.dateString = '%d%m%y%H%M%S'
        
        

    def start(self):
        print("starting camera function ")
        camerahardware.camera = picamera.PiCamera(resolution=(ConfigHelper.cameraconfig.camera_resulution_r1,ConfigHelper.cameraconfig.camera_resulution_r2),framerate=ConfigHelper.cameraconfig.video_framerate)
        MyDateTime = datetime.datetime.now().strftime(self.dateString)
        #camerahardware.camera.start_recording(ConfigHelper.cameraconfig.video_file_path+str(MyDateTime)+ConfigHelper.cameraconfig.video_format)
        print("recording starts at-"+MyDateTime)
        super().start()
        self.getdata()
        print("camera image capturing started")

    def stop(self):
        
        MyDateTime = datetime.datetime.now().strftime(self.dateString)
        #camerahardware.camera.stop_recording()
        print("recording stops at-"+MyDateTime)
        camerahardware.camera.close()
        
        

    def getdata(self):
        while self.isstarted():
            filename1 = datetime.datetime.now().strftime("%m%d%Y_%H%M%S")
            camerahardware.camera.capture(ConfigHelper.cameraconfig.image_file_path+filename1+ConfigHelper.cameraconfig.image_format, use_video_port=True)
            print("file captures - "+filename1)
            time.sleep(ConfigHelper.cameraconfig.image_capture_time)


class panichardware(hardwarebase):
    def __init__(self):
        hardwarebase.__init__(self,'PANIC')
        print("starting panic button function ")
        self.payload = panicpayload()
        #self.cam = camera()
        #self.gps = gpshardware()
        #self.rfid = rfidhardware()
        #self.payload = shutpayload()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(12, GPIO.OUT)
        
    def start(self):
        #self.cam.cmaera_start()
        super().start()
        self.getdata()

    def getdata(self):
        while self.isstarted():
            input_state = GPIO.input(4)
            if input_state == True:
             
               #print('Panic Button Pressed...')
               #self.gps.stop()
               #self.rfid.stop()
               #self.cam.camera_stop()
               #os.system('shutdown now -h')
               self.payload.status=str("panic_butoon_pressed")
               self.data.deviceid = ConfigHelper.deviceid
               self.data.hardwareid =ConfigHelper.panicconfig.hardwareid
               self.data.hardwaretype = 'PANIC'
               self.data.payload = self.payload.payloadjson()
               self.data.organizationid = ConfigHelper.orgid
               self.data.routeid = ConfigHelper.routeid
               today_date = str(datetime.datetime.now().strftime(self.DateString))
               time_now = str(datetime.datetime.now().strftime(self.TimeString))
               self.data.datestamp = today_date
               self.data.timestamp = time_now
               self.data.applicationname ='SmartTrack'
               self.savedata()
               for i in range(1,60):
                 print('Panic Button Pressed...')
                 GPIO.output(12, True)
                 time.sleep(0.2)
                 GPIO.output(12,False)
                 time.sleep(0.2)
            else:
               GPIO.output(12, False)
            

			   
