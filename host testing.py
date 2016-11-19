
# coding: utf-8

# In[3]:

__author__ = 'Yuri'
                                                                                                     
   
import sys

try:
    from http.client import HTTPConnection #Python 3
except ImportError:
    from httplib import HTTPConnection #Python 2
        
import base64
import time
import hashlib #md5
from urllib.parse  import quote #URL encode
import timeit


port = 700
url1= '/site/api/v1/catalog/filter/products'
host_list = ('',
             '',
             '',
             '')






TOKEN_SALT = ""
headers = {'Accept':'application/json',                                                           
           'X-Auth':'token'}                                                                                                                                                                               


member_entity_no = 1
    
def generate_token(member_no):
    
    sec = lambda: round(int(time.time()))    # get timestamp in seconds (if *1000 we will get milisec)
    
    timestamp = sec()
    
    #create a token
    token = "timestamp="+quote(str(timestamp), "UTF-8")+"&salt="+quote(TOKEN_SALT, "UTF-8")    
    print("token 1:" +token)
    
    md5_hash = hashlib.md5(bytes(token, "UTF-8")).digest()
    
    #safety base64 it
    base64_md5 = base64.urlsafe_b64encode(md5_hash)
        
    
    #prepare secret key
    secret = "+str(timestamp)+"&token="+str(base64_md5, "UTF-8")
    
    #base64 it
    encoded_data = base64.urlsafe_b64encode(bytes(secret, "UTF-8"))    
    
    return encoded_data.decode("utf-8") 

def test_host(hosts):  
    
    for host in hosts:        
        start_time = timeit.default_timer()
        print('testing %s:%s' % (host, port))
        conn = HTTPConnection(host, port=port, timeout=30)
        headers['X-Auth'] = generate_token(member_entity_no)
        print("HEADERS: %s" % headers.values())
        try:
            request = conn.request('GET', url, None, headers)
            response = conn.getresponse()
            
            #json_obj = json.loads(str(response.read()))            
            #json.dumps(json_obj)
            
            print(str(response.read())) #get body 
            print(response.status, response.reason)
        except ConnectionRefusedError as e:    
            print(e)
            pass
        print("EXECUTION TIME: %s" % (timeit.default_timer() - start_time))
        print("------------------------------------------")
        conn.close()
        #conn.request('HEAD', 'test.do')





