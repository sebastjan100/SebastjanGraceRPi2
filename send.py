import requests
from settings import *

def UZ(url, endpoint, distance, apikey):
    headers = {
        "Authorization" : "Bearer " + apikey
    }
    data = {
    "distance": distance
    }
    response = requests.post(url+endpoint, json=data, headers=headers)  
    print(response.status_code)

def DHT(url, endpoint, data, apikey):
    headers = {
        "Authorization" : "Bearer " + apikey
    }
    data = {
    "temp": data[1],
    "hum": data[0]
    }
    response = requests.post(url+endpoint, json=data, headers=headers)
    print(response.status_code)

def PIR(url, endpoint, cas, apikey):
    headers = {
        "Authorization" : "Bearer " + apikey
    }
    response = requests.post(url+endpoint, headers=headers)
    print(cas)
    print(response.status_code)

def TRAK(url, endpoint, apikey):
    headers = {
        "Authorization" : "Bearer " + apikey
    }
    response = requests.get(url+endpoint, headers=headers)
    print(response.text)# response je objekt, ki ima polja text, json, statuscode itd.
    return response.text