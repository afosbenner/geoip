#!/usr/bin/env python3

##########################################################################
# filename:     geoip.py
# description:  module to access geoIP information using the free API from
# 		ip-api.com.  
# todo list:	fix timing to avoid getting kicked off 

##########################################################################

# fields supported by API, see www.ip-api/com/docs/api:json
fields = [ "status",
           "message", # only included when status is fail
           "continent",
           "continentCode",
           "country",
           "countryCode",
           "region",
           "regionName",
           "city",
           "district",
           "zip",
           "lat",
           "lon",
           "timezone",
           "currency",
           "isp",
           "org",
           "as",
           "asname",
           "reverse",
           "mobile",
           "proxy",
           "query" ]

def lookup(addr, f = None):
    from urllib import request
    import json

    url = "http://www.ip-api.com/json/" + addr
    if isinstance(f, str):
        url += "?fields=" + f
    elif isinstance(f, list):
        url += "?fields=" + ",".join(f)
        
    try:
        resp = request.urlopen(url)
    except:
        print("Error occurred while accessing API")
        return None 

    # resp.read() returns bytes object, json.loads() returns a dict
    data = json.loads(resp.read())

    print(resp.getheader("X-Rl")) #driver

    return data

def multi_lookup(addr_list, f = None):
    import time
    import math

    def reset_time():
        return math.floor(time.time())

    data = []
    ti = reset_time()

    for i in range(len(addr_list)):
        te = math.ceil(time.time()) - ti
        print("i =", i, "te =", te) #driver
        if te <= 60 and i > 0 and i%150 == 0:
            print("sleeping", 60 - te, "sec") #driver
            time.sleep(60 - te)
            ti = reset_time()
        data.append(lookup(addr_list[i], f))


    return data

