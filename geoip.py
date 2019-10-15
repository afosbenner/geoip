"""geoip module

Using the JSON API from www.ip-api.com, retrieve geographic IP
information for a given IP address or hostname. This service does not
require the user to sign-up or provide an API key, as long as the user
does not exceed a maximum number of requests per minute, as specified on
their website. Using the methods provided in the geoip.Lookup class, the
user need not worry about the timing restrictions imposed by the API
service.

Classes provided by module:
Lookup

Example:
import geoip
L = geoip.Lookup()
a = "8.8.8.8"
d1 = L.lookup(a)
d2 = L.lookup(a, L.fields)
"""

import time
from math import ceil
from time import time, sleep
from urllib import request
import json

max_per_min = 45 # specified on website

class Lookup:
    """Lookup class

    Provide methods to lookup geographic IP information and a list of
    fields accepted by the API. 

    Methods of class Lookup:
    lookup()
    multi_lookup()

    Attributes of class Lookup:
    fields[]
    """

    def __init__(self):
        self._ti = 0
        self._te = 0
        self._count = 1
        # fields supported by API, see www.ip-api/com/docs/api:json
        self.fields = [ "status",
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
                        "query" 
                      ]


    def _reset_time(self):
        self._ti = time()

    def _elapsed(self):
        self._te = time() - self._ti

    def _check_timing(self):
        self._elapsed()
        try: # try to use header vals returned
            if self._XRl == 0:
                #print("sleeping", 2 + self._XTtl, "<headers>") # driver
                sleep(2 + self._XTtl) # sleep extra 2 seconds
        except: # if headers can't be used, fall back on timer/counter
            if self._te < 60  and self._count > max_per_min:
                #print("te=", self._te) # driver
                #print("sleeping", 62-ceil(self._te), "<timer>") # driver
                sleep(62 - ceil(self._te)) # sleep extra second
        finally:
            self._elapsed()
        if self._te > 60:
            self._reset_time()
            self._count = 1

    def lookup(self, addr, f=None):
        """lookup() Usage: <Lookup_obj>.lookup(addr, [f])

        Returns a dict containing the geoIP info for given address.

        Parameters:
        addr: a list of strings containing IP addresses or hostnames
        f: Optional. a list of strings containing field names to include
           in lookup.  See fields list for valid fields.  If this is
           omitted, the request will have no fields specified, so the 
           API will return the default fields.
        """

        # TODO check for addr type, maybe add exception
        if isinstance(addr, list):
            return self.multi_lookup(addr, f)
        else:
            url = "http://www.ip-api.com/json/" + addr
            if isinstance(f, str):
                url += "?fields=" + f
            elif isinstance(f, list):
                url += "?fields=" + ",".join(f)

            if self._ti == 0:
                self._reset_time()
            else:
                self._check_timing()
            #print("count =", self._count, "te =", self._te) #driver

            try:
                resp = request.urlopen(url, timeout=5)
            except:
                #print("Error occurred while accessing API") # driver
                return None

            #resp.read() returns bytes object, json.loads() returns a dict
            data = json.loads(resp.read())
            try:
                self._XRl = int(resp.getheader("X-Rl"))
                self._XTtl = int(resp.getheader("X-Ttl"))
            except:
                self._XRl, self._XTtl = None, None
            #print("Rl:", self._XRl, "Ttl:", self._XTtl) # driver

            self._count += 1

            return data

    def multi_lookup(self, addr_list, f=None):
        """multi_lookup() Usage: <Lookup_obj>.multi_lookup(addr_list, [f])

        Returns a list of dicts containing the geoIP info for each address
        in addr_list.

        Parameters:
        addr_list: a list of strings containing IP addresses or hostnames
        f: Optional. a list of strings containing field names to include
           in lookup.  See fields list for valid fields.  If this is
           omitted, the request will have no fields specified, so the 
           API will return the default fields.
        """
        data = []
        for i in range(len(addr_list)):
            #sleep(0.065) #for testing
            data.append(self.lookup(addr_list[i], f))

        return data


