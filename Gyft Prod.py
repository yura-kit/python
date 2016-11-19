
# coding: utf-8

# In[17]:

import sys
import hashlib
import http.client

try:
    from http.client import HTTPConnection #Python 3
except ImportError:
    from httplib import HTTPConnection #Python 2
        
import base64
import time
import hashlib #md5
from urllib.parse  import quote #URL encode
import timeit

#url = 'https://api.gyft.com/mashery/v1/reseller/shop_cards'
#health_check = 'https://api.gyft.com/mashery/v1/health/check' https://apitest.gyft.com/mashery/v1/reseller/shop_cards

#TEST

#PROD
api_key = ''
prod_secret = ''


host = 'api.gyft.com'
port = 443
headers = {'Accept':'application/json, application/*+json', 'x-sig-timestamp':''}              
def generate_token():
    
    sec = lambda: round(int(time.time()))    # get timestamp in seconds (if *1000 we will get milisec)
    
    timestamp = sec()
    print(timestamp)
    token = str(api_key) + str(prod_secret) + str(timestamp)
    
    
    new_token = hashlib.sha256(bytes(token, "UTF-8")).hexdigest()
    
    #print("token :" + new_token)
    #health_check = '/mashery/v1/health/check'
    #health_check = '/mashery/v1/reseller/shop_cards'
    health_check = '/mashery/v1/reseller/shop_cards'

    health_check = health_check + '?api_key=' + api_key + '&sig=' + new_token
    headers['x-sig-timestamp'] = str(timestamp)
    print(health_check)
    print(headers)
    
    c = http.client.HTTPSConnection(host)
    try:
        
        request = c.request('GET', health_check, None, headers)
                
        response = c.getresponse()
            
        print(str(response.read())) #get body 
        print(response.status, response.reason)
    except ConnectionRefusedError as e:    
        print(e)
        pass

    

