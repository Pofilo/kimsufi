#!/usr/bin/env python
# encoding: UTF-8

import json
import time
import http1
import requests


API_URL = "https://ws.ovh.com/dedicated/r2/ws.dispatcher/getAvailability2"
REFERENCE = '160sk2'
ZONES = set(["gra", "rbx", "sbg", "par"])


def main():
    print "Calling kimsufi API..."
    try:
        response = http1.get(API_URL)
        if response.status == 200:
            struct = json.loads(response.body)
            for item in struct['answer']['availability']:
                zones = [z['zone'] for z in item['zones'] if z['availability'] not in ('unavailable', 'unknown')]
                if set(zones).intersection(ZONES) and item['reference'] == REFERENCE:
                    print "Found available server, sending sms..."
                    r = requests.get("PUT YOUR FREE URL HERE")
        else:
            print "Error calling API: %s %s" % (response.status, response.message)
    except Exception as e:
        print "Error calling API: %s" % str(e)

if __name__ == '__main__':
    main()
