import configparser
import os, sys
import logging
import inspect
import time, datetime

class ConfigHelper(object):
	"""helper class to work with config file"""

	dbfile = 'SmartTrack.db'
	debugmode = 0
	deviceid = None
	cloudmanager = None
	datasync = None
	hardwares = None
	logconfig = None
	orgid = None
	routeid = None
	gpsconfig = None
	cameraconfig = None
	rfidconfig = None
	panicconfig = None
	acceleroconfig = None
	appname = None
	config = configparser.ConfigParser()

	def __init__(self, configfile):
			""" initialize the config parser"""
			self.config.read(configfile)

			# Load Device Config
			ConfigHelper.dbfile = self.config['DEVICE']['DB_FILE']
			ConfigHelper.debugmode = self.config['DEVICE']['DEBUG_MODE']
			ConfigHelper.deviceid = self.config['DEVICE']['DEVICE_ID']
			ConfigHelper.restartinterval = self.config['DEVICE']['RESTART_INTERVAL']
			ConfigHelper.orgid	= self.config['DEVICE']['ORG_ID']
			ConfigHelper.appname = self.config['DEVICE']['APP_NAME']
			ConfigHelper.routeid = self.config['DEVICE']['ROUTE_ID']

			# Load Logging Config
			ConfigHelper.logconfig = LoggingConfig()
			ConfigHelper.logconfig.logtoconsole = self.config['LOGCONFIG']['LOG_TO_CONSOLE']
			ConfigHelper.logconfig.disabled = int(self.config['LOGCONFIG']['DISABLED'])

			# Load Cloud Manager
			ConfigHelper.cloudmanager = CloudManagerConfig()
			ConfigHelper.cloudmanager.connection_string = str(self.config['CLOUDMANAGER']['CONNECTION_STRING']).strip('"')
			ConfigHelper.cloudmanager.protocol = self.config['CLOUDMANAGER']['PROTOCOL']
			ConfigHelper.cloudmanager.message_timeout = self.config['CLOUDMANAGER']['MESSAGE_TIMEOUT']
			ConfigHelper.cloudmanager.method_context = self.config['CLOUDMANAGER']['RETRY_INTERVAL']
			ConfigHelper.cloudmanager.receive_context = self.config['CLOUDMANAGER']['RECEIVE_CONTEXT']
			ConfigHelper.cloudmanager.method_context = self.config['CLOUDMANAGER']['METHOD_CONTEXT']
			ConfigHelper.cloudmanager.command_callback_wait = int(self.config['CLOUDMANAGER']['COMMAND_CALLBACK_WAIT'])

			# Http protocol properties
			ConfigHelper.cloudmanager.http_timeout = self.config['CLOUDMANAGER']['HTTP_TIMEOUT']
			ConfigHelper.cloudmanager.http_minimum_polling_time = self.config['CLOUDMANAGER']['HTTP_MINIMUM_POLLING_TIME']

			# Load Data Sync
			ConfigHelper.datasync = DataSyncConfig()
			ConfigHelper.datasync.batch_size = str(self.config['DATASYNC']['BATCH_SIZE'])
			ConfigHelper.datasync.sync_interval = str(self.config['DATASYNC']['SYNC_INTERVAL'])
			# Load Hardware devices
			ConfigHelper.hardwares = self.config['HARDWAREDEVICES']
                        #Load GPS setting
			ConfigHelper.gpsconfig = GpsConfig()
			ConfigHelper.gpsconfig.hardwareid = str(self.config['GPS']['HARDWARE_ID'])
			ConfigHelper.gpsconfig.Refresh_Interval = int(self.config['GPS']['REFRESH_INTERVAL'])
			ConfigHelper.gpsconfig.Restart_Interval = self.config['GPS']['RESTART_INTERVAL']
			ConfigHelper.gpsconfig.Com_Port = self.config['GPS']['COM_PORT']
			ConfigHelper.gpsconfig.Baud_Rate = self.config['GPS']['BAUD_RATE']
                        #load rfid setting
			ConfigHelper.rfidconfig = RfidConfig()
			ConfigHelper.rfidconfig.hardwareid = str(self.config['RFID']['HARDWARE_ID'])
			ConfigHelper.rfidconfig.Refresh_Interval = float(self.config['RFID']['REFRESH_INTERVAL'])
			ConfigHelper.rfidconfig.Restart_Interval = self.config['RFID']['RESTART_INTERVAL']
			ConfigHelper.rfidconfig.Com_Port = self.config['RFID']['COM_PORT']
			ConfigHelper.rfidconfig.Baud_Rate = self.config['RFID']['BAUD_RATE']
                        #load panic button setting
			ConfigHelper.panicconfig = PanicConfig()
			ConfigHelper.panicconfig.hardwareid = str(self.config['PANIC']['HARDWARE_ID'])
			ConfigHelper.panicconfig.Refresh_Interval = float(self.config['PANIC']['REFRESH_INTERVAL'])
			ConfigHelper.panicconfig.Restart_Interval = self.config['PANIC']['RESTART_INTERVAL']
                        #load camera setiing
			ConfigHelper.cameraconfig = CameraConfig()
			ConfigHelper.cameraconfig.hardwareid = str(self.config['CAMERA']['HARDWARE_ID'])
			ConfigHelper.cameraconfig.camera_resulution_r1 = int(self.config['CAMERA']['R1'])
			ConfigHelper.cameraconfig.camera_resulution_r2 = int(self.config['CAMERA']['R2'])
			ConfigHelper.cameraconfig.video_file_path = str(self.config['CAMERA']['VIDEO_PATH'])
			ConfigHelper.cameraconfig.image_file_path = str(self.config['CAMERA']['IMAGE_PATH'])
			ConfigHelper.cameraconfig.image_format = str(self.config['CAMERA']['IMG_FORMATE'])
			ConfigHelper.cameraconfig.video_format = str(self.config['CAMERA']['VDO_FORMATE'])
			ConfigHelper.cameraconfig.video_framerate = int(self.config['CAMERA']['FRAME'])
			ConfigHelper.cameraconfig.image_capture_time = float(self.config['CAMERA']['IMG_CAP_TIME'])
			ConfigHelper.cameraconfig.feed_enabled = self.config.getboolean('CAMERA','FEED_ENABLED')
			#accelerometer config
			ConfigHelper.acceleroconfig = AcceleroConfig()
			ConfigHelper.acceleroconfig.Refresh_Interval = float(self.config['ACCELERO']['REFRESH_INTERVAL'])
			ConfigHelper.acceleroconfig.Restart_Interval = self.config['ACCELERO']['RESTART_INTERVAL']
			ConfigHelper.acceleroconfig.hardwareid = str(self.config['ACCELERO']['HARDWARE_ID'])
			
			 

 
	def getstartinterval(device):
	    if 'RESTART_INTERVAL' in ConfigHelper.config[device.upper()]:
	            return int(ConfigHelper.config[device.upper()]['RESTART_INTERVAL'])
	    else:
	            return int(ConfigHelper.restartinterval)

class LoggingHelper(object):
	
	
	def __init__(self, logdisabled ,  useConsole=True):
		"""
		Simple Logging Helper. Retuens logger reference.

		Paramsmeters:
		fileName: Filename, may include full path, or will open a file in default folder
		logLevel: Pass logging.INFO, logging.DEBUG or other enums for logging level
		useConsole: If Ture, will also dump log to console
		"""
    	##### init logging
		self.log = logging.getLogger()
		self.log.setLevel(logging.INFO)
		logFormatter = logging.Formatter("%(asctime)s | %(threadName)-12.12s | %(levelname)-5.5s | %(message)s")
        #to disable or enable complete logging
		self.log.disabled = logdisabled 

        #### file handler
		filename = '/home/pi/mycode/IOT.Device.SmartTrack/logs/'+datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.log'
		fileOut = logging.FileHandler(filename)
		fileOut.setFormatter(logFormatter)
		self.log.addHandler(fileOut)

		##### console handler
		if useConsole:
			consoleOut = logging.StreamHandler(sys.stdout)
			consoleOut.setFormatter(logFormatter)
			self.log.addHandler(consoleOut)

	def debug(self,message):
		"Automatically log the current function details."
		# Get the previous frame in the stack, otherwise it would
		# be this function!!!
		func = inspect.currentframe().f_back.f_code
		# Dump the message + the name of this function to the log.
		self.log.debug("%s: %s in %s:%i" % (
			message, 
			func.co_name, 
			os.path.basename(func.co_filename), 
			func.co_firstlineno
		))

	def info(self,message):
		"Automatically log the current function details."
		# Get the previous frame in the stack, otherwise it would
		# be this function!!!
		func = inspect.currentframe().f_back.f_code
		# Dump the message + the name of this function to the log.
		self.log.info("%s: %s in %s:%i" % (
			message, 
			func.co_name, 
			os.path.basename(func.co_filename), 
			func.co_firstlineno
		))

	def warning(self,message):
		"Automatically log the current function details."
		# Get the previous frame in the stack, otherwise it would
		# be this function!!!
		func = inspect.currentframe().f_back.f_code
		# Dump the message + the name of this function to the log.
		self.log.warning("%s: %s in %s:%i" % (
			message, 
			func.co_name, 
			os.path.basename(func.co_filename), 
			func.co_firstlineno
		))

	def error(self,message):
		"Automatically log the current function details."
		# Get the previous frame in the stack, otherwise it would
		# be this function!!!
		func = inspect.currentframe().f_back.f_code
		# Dump the message + the name of this function to the log.
		self.log.error("%s: %s in %s:%i" % (
			message, 
			func.co_name, 
			os.path.basename(func.co_filename),  
			func.co_firstlineno
		))



class CloudManagerConfig(object):
    
    connection_string = None
    protocol = None
    http_timeout = None
    http_minimum_polling_time = None
    message_timeout = None
    send_callbacks = None
    iot_deviceid = None
    receive_context = None
    method_context = None
    retry_interval = None
    command_callback_wait = None

class DataSyncConfig(object):
    batch_size = None
    sync_interval = None

class LoggingConfig(object):

	disabled = None
	loglevel = None
	logtoconsole = None

class GpsConfig(object):
    hardwareid=None
    Restart_Interval=None
    Refresh_Interval=None
    Com_Port=None
    Baud_Rate=None

class RfidConfig(object):
    hardwareid=None
    Restart_Interval=None
    Refresh_Interval=None
    Com_Port=None
    Baud_Rate=None
    
class PanicConfig(object):
    hardwareid=None
    Restart_Interval=None
    Refresh_Interval=None

class CameraConfig(object):
    hardwareid=None
    camera_resulution_r1= None
    camera_resulution_r2= None
    video_file_path = None
    image_file_path = None
    image_format = None
    video_format = None
    video_framerate =None
    image_capture_time =None
    feed_enabled = False

class AcceleroConfig(object):
    hardwareid=None
    Restart_Interval=None
    Refresh_Interval=None
   
    
