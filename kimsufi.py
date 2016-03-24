#!/usr/bin/env python
# encoding: UTF-8

import json
import time
import http1
import mail1


API_URL = "https://ws.ovh.com/dedicated/r2/ws.dispatcher/getAvailability2"
REFERENCE = '160sk1'
ZONES = set(["gra", "rbx", "sbg", "par"])


def main():
    while (True):
        print "Calling kimsufi API..."
        try:
            response = http1.get(API_URL)
            if response.status == 200:
                struct = json.loads(response.body)
                for item in struct['answer']['availability']:
                    zones = [z['zone'] for z in item['zones'] if z['availability'] not in ('unavailable', 'unknown')]
                    if set(zones).intersection(ZONES) and item['reference'] == REFERENCE:
                        print "Found available server, sending email..."
                        mail1.send(subject='Kimsufi Available!',
                                   text='Run Forest, run!',
                                   recipients='michel.casabianca@gmail.com',
                                   sender='michel.casabianca@gmail.com',
                                   smtp_host='smtp.orange.fr')
            else:
                print "Error calling API: %s %s" % (response.status,
                                                    response.message)
        except Exception as e:
            print "Error calling API: %s" % str(e)
        time.sleep(30)


if __name__ == '__main__':
    main()
