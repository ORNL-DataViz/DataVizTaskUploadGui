import requests  
import json

url = "http://127.0.0.1:8000/practice"
data = {'category':'bear_paws', 'num_of_photos':50}
r=requests.post(url, data=data)
got_response = r.text
print(got_response)

url = "http://127.0.0.1:8000/practice"
data = {'category':'baby yoda', 'num_of_photos':1 }
f = open('/Users/62m/Desktop/Baby-Yoda-2.jpg', 'rb')
files = {
        'photo': f,
        'Content-Type': 'image/jpeg'
    }
r=requests.post(url, data=data, files=files)
got_response = r.text
print(got_response)
print(r.status_code)
