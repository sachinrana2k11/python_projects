#start from here sachin rana
import requests
result = requests.get(url="http://192.168.0.114/temp").content
print(result)

