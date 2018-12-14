from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time,json
def decode_incomming_data(self,params, packet):
        print("received payload is -: ", packet.payload)
        return packet.payload

myMQTTClient = AWSIoTMQTTClient("qwertyuiop123")
print("Initializing device on aws server")
myMQTTClient.configureEndpoint("a3muy1lrol528l-ats.iot.us-east-1.amazonaws.com", 8883)
print("connected with aws endpoint with valid port ")
certRootPath = 'aws_iot_certificates/'
myMQTTClient.configureCredentials("{}root-ca.pem".format(certRootPath), "{}cloud.pem.key".format(certRootPath),"{}cloud.pem.crt".format(certRootPath))
print("Applying certificate")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
print("Connecting MQQT AWS")
myMQTTClient.connect()
print("Connecting done  MQQT AWS")
myMQTTClient.subscribe("home/SDM120", 1,decode_incomming_data)
print("Init subscribing data thread from AWS")
while 1:
        print("waiting for data")
        time.sleep(5)