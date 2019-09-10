#!/usr/bin/env python3

##########################################################################
# filename:     geoip.py
# description:  module to access geoIP information using the free API from
# 		ip-api.com.  
# todo list:    

##########################################################################

def get_geoip():
    from urllib import request
    import json

    ip = "8.8.8.8" # TODO validate

    resp = request.urlopen("http://www.ip-api.com/json/" + ip)

    # resp.read() returns bytes object
    # json.loads() returns a dict
    data = json.loads(resp.read())

    return data

