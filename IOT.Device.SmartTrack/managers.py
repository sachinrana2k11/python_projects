import sys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
from iothub_client_args import get_iothub_opt, OptionError
from iothub_client import IoTHubClientRetryPolicy, GetRetryPolicyReturnValue
from helpers import ConfigHelper
from models import *
import uuid      
from playhouse.shortcuts import model_to_dict, dict_to_model
import time
from hardware import * 
from multiprocessing import Process, Manager   
from multiprocessing.managers import BaseManager
from events import Events
import glob
import shutil
# hardware events class used for all hardware
class hardwareevents(Events):
    __event__ = ('hardware_started','hardware_stopped','hardware_enabled','hardware_disabled','hardware_exception')

class cloudevents(Events):
    __event__ = ('cloud_connected','cloud_disconnected','cloud_syncstarted','cloud_syncstopped','cloud_messagesent','cloud_messagereceived','cloud_exception','cloud_command')




class cloudmanager(object):
    """ Cloud Manager to send and recieve data to cloud """
    client = None
    send_callbacks = 0
    isconnected = False
    init_protocol = {'HTTP': IoTHubTransportProvider.HTTP,
                     'MQTT': IoTHubTransportProvider.MQTT,
                     'MQTT_WS': IoTHubTransportProvider.MQTT_WS,
                     'AMQP': IoTHubTransportProvider.AMQP
                   }

    def __init__(self,log):


        #Init variables
        self.isrunning = False
        self.logger = log
        self.events = cloudevents()
        self.device_method_return_value = DeviceMethodReturnValue()
        
        

    def initializecloudmanager(self):        
        
        #Init connction
       
     try:   
        self.logger.info("try to initialize cloud manager")
        cloudmanager.client = IoTHubClient(ConfigHelper.cloudmanager.connection_string, self.init_protocol[ConfigHelper.cloudmanager.protocol])
        cloudmanager.client.set_option("messageTimeout", ConfigHelper.cloudmanager.message_timeout)

        # Load  http settings
        if ConfigHelper.cloudmanager.protocol == 'HTTP':
                
                cloudmanager.client.set_option("timeout", ConfigHelper.cloudmanager.http_timeout)
                cloudmanager.client.set_option("timeout", ConfigHelper.cloudmanager.http_timeout)
                self.logger.info("HTTP setting loaded")
        
        # Load mqtt settings

        if ConfigHelper.cloudmanager.protocol == 'MQTT':
               cloudmanager.client.set_device_method_callback(self.device_method_callback,ConfigHelper.cloudmanager.method_context)
               self.logger.info("MQTT setting loaded ")

        # Set Callback method to recieve message        
        cloudmanager.client.set_message_callback(self.receive_message_callback, ConfigHelper.cloudmanager.receive_context)
        #self.logger.info("method set for recieve message ")

        retryPolicy = IoTHubClientRetryPolicy.RETRY_INTERVAL
        retryInterval = ConfigHelper.cloudmanager.retry_interval
        cloudmanager.client.set_retry_policy(retryPolicy, retryInterval)

     except:
          e = sys.exc_info()[0]
          #Raise exception event
          self.events.cloud_exception(e)
          self.logger.error("Exception in initializecloudmanager() method "+str(e))


    # Function to receive message from cloud two parameters are returned
    def receive_message_callback(self,message, counter):

        try:
        # raise message received event
           #self.logger.info("try to receive cloud message")
           self.events.cloud_messagereceived(message)
           
        # return Accepted
           return IoTHubMessageDispositionResult.ACCEPTED
           #self.logger.info("message recived")
        except:
          e = sys.exc_info()[0]
          #Raise exception event
          self.events.cloud_exception(e)
          self.logger.error("Exception in receive_message_callback() method "+str(e))


    # Function called by cloud on successful reciveing of a message sent earlier
    # this will be used to update the synced status of a message in database
    def send_confirmation_callback(self,message, result, user_context):
      
     try:   
        #print ( "Confirmation  received for messageid : [%s] with result = %s" % (message.message_id, result) )
        
        # Check if application running in debugmode
        #self.logger.info("try to send confirmation callback")
        if (int(ConfigHelper.debugmode) == 1):
            
            # change the status of the message synced and dont delete
           # self.logger.info("debug mode set to = 1")
            query = devicedata.update(synced = 1).where((devicedata.id == message.message_id))
            self.logger.info("query feed up")
            
        else:
            # Delete the message from the database
            #self.logger.info("debug mode not set to = 1")
            query = devicedata.delete().where((devicedata.id == message.message_id))
        
        # Execute query
        query.execute()
        #self.logger.info("query executed...")
    
    # Function to be called when cloud send method call message
     except:
          e = sys.exc_info()[0]
          #Raise exception event
          self.events.cloud_exception(e)
          self.logger.error("Exception in send_confirmation_callback() Method:"+str(e))

    def device_method_callback(self,method_name,payload,user_context):

     try:  
        # Raise cloud_command event to be used by hardware manager
        #self.logger.info("Raising cloud_command event to be used by hardware manager")
        self.events.cloud_command(method_name,payload)

        # Wait for specified time before sending back the return value assigned in the event
       # self.logger.info("waiting for cloud manager..")
        time.sleep(ConfigHelper.cloudmanager.command_callback_wait)
        
        return self.device_method_return_value
        self.logger.info("getting value and return")
     except:
          e = sys.exc_info()[0]
          #Raise exception event
          self.events.cloud_exception(e)
          self.logger.info("Exception in device_method_callback() Method:"+str(e))
    # Function called by cloud on successfull uploading of a file
    # user_context parameter will return the filename uploaded
    # result will be OK or Error
    def file_upload_conf_callback(self, result, user_context):
            
          filename = ConfigHelper.cameraconfig.image_file_path + "sync_" + user_context
      
          # Delete the file 
          os.remove(filename)
          self.logger.info("Deleted" +  filename + " after uploading to server")
          print(' File ' + filename + ' deleted after sync')
    # function to start data sync process
    def startdatasync(self):
        try:
       
            # Set the status of isrunning to True
            self.logger.info("Try to start data sync")
            self.isrunning = True
            
            #raise event sycnstarted
            self.events.cloud_syncstarted()

            # Loop while self.isrunning is true
            while self.isrunning:
           
                  # get the records from database to sync

                  for data in devicedata().select().order_by(devicedata.datestamp.desc() and devicedata.timestamp.asc()).where(devicedata.synced == 0).limit(int(ConfigHelper.datasync.batch_size)):
                  
                        message = IoTHubMessage(json.dumps(model_to_dict(data)))
                        print(data)
                        #self.logger.info("object feed up with jason object..")
                        message.message_id = data.id
                        message.correlation_id = data.id

                        # optional: assign properties
                        prop_map = message.properties()
                        #prop_text = "PropMsg_%d" % message_counter
                        prop_map.add("MESSAGE_TYPE", data.messagetype)

                        
                        cloudmanager.client.send_event_async(message, self.send_confirmation_callback, 0)
                        #raise event message sent
                        self.logger.info("raise event message sent")
                        self.events.cloud_messagesent(data.messagetype,message)
                  
                  if(ConfigHelper.cameraconfig.feed_enabled):
                          # If Camera Feed is Enabled  
                          # pick only files which has name starting with number
                          directory =  ConfigHelper.cameraconfig.image_file_path+"[^0-9]*.jpg"    #[^0-9]*.jpg
                          # get the list of images to sync 
                          for file in list(glob.glob(directory)):
                            filename = os.path.basename(file)
                            filehandle = open(file,"rb")
                            source = filehandle.read()
                            # upload file
                            self.client.upload_blob_async(filename, source, len(source),self.file_upload_conf_callback, filename)
                            self.logger.info("Uploading async file :" + filename)
                            # Rename the file 
                            filehandle.close() 
                            newfilename = ConfigHelper.cameraconfig.image_file_path + "sync_" +  filename
                            self.logger.info("Renaming file :" + filename + " to " + newfilename)
                            os.rename(file,newfilename)
                            break
                
                # Wait for next batch to be processed
                  self.logger.info("wait for next data/image batch to sync")
                  time.sleep(int(ConfigHelper.datasync.sync_interval))    

        except IoTHubError as iothub_error:
            print ( "Unexpected error %s from IoTHub" % iothub_error )
            self.logger.error("Exception with IoTHubError as iothub_error")
            return
        except KeyboardInterrupt:
            print ( "IoTHubClient sample stopped" )
            self.logger.error("Exception with KeyboardInterrupt")

              
    # function to stop data sync process
    def stopdatasync(self):
        try:
           #self.logger.info("try to stop data sync")
           self.isrunning = False
           # raise event sycn stopped
           #self.logger.info("raise event sycn stopped")
           self.events.cloud_syncstopped()
           self.logger.info("cloud sync stopped ")
        except:
          e = sys.exc_info()[0]
          #Raise exception event
          self.events.cloud_exception(e)
          self.logger.error("Exception in stopdatasync() Method:"+str(e))
    # Function to sync feed images with server
    
    
                  


class hardwaremanager(object):
    """ Hardware Manager to start all the listed and enabled hardware in config """
    
    def __init__(self,log):

        self.events = hardwareevents()
        self.logger = log
        self.logger.info("logger initialized---")
    # Method to start all hardware's which are enabled in config
    def startmanager(self,hardwares):
        
     try:
        
       #manager = Manager()
       self.processes = {} 
       
       # create manager to share the hardware object with multiple process
       # Initialize all the different hardwares which are enabled in config
      
       for device,enabled in ConfigHelper.hardwares.items():
           
       
            # Check if hardware is enabled
            if enabled == 'True' :
                  self.processes[device] = Process(target = hardwares[device].start)
                  self.processes[device].start()
                  #raise the intihardware event
                  self.events.hardware_started(device)
                  self.logger.info("manager started for enable devices")      
            else:
                pass
     except:
          e = sys.exc_info()[0]
          print(e)
          self.logger.error("Exception in startmanager() Method:"+str(e))
          self.events.hardware_exception(e)


    # Method to start and init a specific hardware based on name
    def starthardware(self,device,hardwares):
        try:
        # If device is enabled and intialized
            self.logger.info("Try to start starthardware() Method ")
            if device in hardwares:
            # Start the device to enable it if not started already
                if hardwares[device].isstarted() == False:
            
                    

                           self.processes[device] = Process(target = hardwares[device].start)
                           self.processes[device].start()
                      
                           # raise the hardware_start event
                           self.events.hardware_start(device)
                           # Keep waiting for this process to finish
                           self.processes[device].join() 
                           self.logger.info("starthardware() Method Started")
                   
        except:
            e = sys.exc_info()[0]
            #Raise exception event
            self.logger.error("Exception in  starthardware() Method:"+str(e))
            self.events.hardware_exception(e)
    
    # Method to stop a specific hardware based on name
    def stophardware(self,device,hardwares):
       
        try:
                # If device is enabled and intialized
                self.logger.info("Try to start stophardware() Method ")
                if device in hardwares:
                    self.logger.info(device+"found in hardware")
                    deviceobj = hardwares[device]
                    # If device is started   
                    if deviceobj.isstarted():
            
                        # Call stop of the object    
                        deviceobj.stop()
                        self.logger.info('device stopped event called')
                        # Raise Stopped Event
                        self.events.hardware_stopped(device)
                        self.logger.info("hardware stopped")
        except:
            e = sys.exc_info()[0]
            #Raise exception event
            self.logger.info("Exception in stophardware() Method :"+str(e))
            self.events.hardware_exception(e)
    
    # Method to stop a specific hardware based on name
    def restarthardware(self,device,hardwares):
        
     try:
        self.logger.info("try to restart device") 
        self.stophardware(device,hardwares) 
        # Give 10 seconds to stop
        self.logger.info("waiting for 10 sec to stop device")
        time.sleep(ConfigHelper.getstartinterval(device))
        self.logger.info("Device stopped")
        # Start Device again
        self.logger.info("try to again start device")
        self.starthardware(device,hardwares)
        self.logger.info("Device Restarted successfully ")
        

    # Method to disable a specific hardware based on name
     except:
        e = sys.exc_info()[0]
        self.logger.error("Exception in restarthardware() Method:"+str(e))
        self.events.hardware_exception(e)

    def disablehardware(self,device,hardwares):
       
        try:
                # If device is enabled and intialized
                self.logger.info("try to disable hardware")
                if device in hardwares:
                    self.logger.info(device+":found in hardwares")
                    deviceobj = hardwares[device]
                    # If device is started   
                    if deviceobj.isstarted():
                        self.logger.info("stopping hardware")
                        deviceobj.stop()
                        # Raise Stopped Event
                        self.events.hardware_stopped(device)
                        self.logger.info("Device stopped")
                        # Now disable the device
                        self.loggerog.info("try to Device disable")
                        deviceobj.disable()
                        # Raise disabled event
                        self.events.hardware_disabled(device)
                        self.logger.info("Device disabled")
        except:
            e = sys.exc_info()[0]
            #Raise exception event
            self.events.hardware_exception(e)
            self.logger.error("Exception in disablehardware() Method:"+str(e))

    # Method to enable a specific hardware based on name
    def enablehardware(self,device,hardwares):
       
        try:
                # If device is disabled
                self.logger.info("try to enable hardware")
                if device in hardwares:
                    self.logger.info(device+":Found in hardwares")
                    deviceobj = hardwares[device]
                    # If device is started   
                    if deviceobj.isenabled() == False:
            
                        deviceobj.enable()
                        # Raise Enable Event
                        self.events.hardware_enabled(device)

                        # Now Start the device
                        self.starthardware(device,hardwares)
                        self.logger.info("Device enabled")
        except:
            e = sys.exc_info()[0]
            #Raise exception event
            self.events.hardware_exception(e)
            self.logger.error("Exception in enablehardware() Method"+str(e))

    # Method to check if hardware is started
    def ishardwarestarted(self,device,hardwares):
     try:    
        self.logger.info("try to run ishardwarestarted() method and checking for hardware started or not ")
        if device in hardwares:
             
            deviceobj = hardwares[device]
            return deviceobj.isstarted()
            self.logger.info("hardware isstarted True")
        else:
            return False
            self.logger.info("hardware isstarted false")
     except:
          e = sys.exc_info()[0]
          #Raise exception event
          self.logger.error("Exception in ishardwarestarted() method"+str(e))
          self.events.hardware_exception(e)
    
    hardware_actions = {   'START'  : starthardware,
                           'STOP'   : stophardware,
                           'ENABLE' : enablehardware,
                           'DISABLE': disablehardware,
                           'RESTART': restarthardware,
                           'ISSTARTED': ishardwarestarted
                       }       
                 
        

    # Method to process command based on payload and action
    def processcomand(self,action,payload,hardwares):
        
        try:
         # Action is present in list of available actions
            self.logger.info("try to process command")
            if action in self.hardware_actions:

                # Execute the action for device specified in payload
                # convert payload to object
                self.logger.info("initialize jason object")
                json_obj = json.loads(payload)
                self.logger.info("creating cloudcommandpayload() class object ")
                cloudpayload = cloudcommandpayload(json_obj)
                
                # call the specific action 
                self.hardware_actions[action](self,cloudpayload.hardware,hardwares)
                self.logger.info("returning the status of DeviceMethodReturnValue() ")
                # Return the Status
                devicereturn = DeviceMethodReturnValue()
                devicereturn.response = '{ "Status": "Success","Message":"Action completed succesfully"}'
                devicereturn.status = 200
                return devicereturn
                self.logger.info("return success")
        except:
       
             e = sys.exc_info()[0]
             self.logger.error("exception in processcomand() Method"+str(e))
             #Raise exception event
             self.events.hardware_exception(e)
             # Return the Status
             devicereturn = DeviceMethodReturnValue()
             devicereturn.response = '{ "Status": "Failure","Message":"Action failed"}'
             devicereturn.status = 0
             return devicereturn
        
# https://github.com/MicrosoftDocs/azure-docs/blob/master/articles/iot-hub/iot-hub-python-getstarted.md
# https://github.com/Azure/azure-iot-sdk-python/tree/master/device/samples

    
   
 

  
        

