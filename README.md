# geoip
Python module to obtain geographic IP information.  Uses a free API, so no direct access to a database or account creation is necessary.

Note: This module uses the API from www.ip-api.com.  Please see http://www.ip-api.com/docs/legal for their Terms of Service.

## Usage
    import geoip

    # Instantiate Lookup object
    L = geoip.Lookup()

    # Perform lookup with default fields
    a = "8.8.8.8"
    d1 = L.lookup(a)

    # Perform lookup with all fields
    d2 = L.lookup(a, L.fields)
