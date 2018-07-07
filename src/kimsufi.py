'''
kimsufi.py: kimsufi's main file.

kimsufi: Sends an alert when your kimsufi is available.
Copyright (C) 2016-2018 pofilo <git@pofilo.fr>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

'''


import json
import time
import http1
import argparse
import signal

import utils
import notifications
from logger import Logger, FATAL, ERROR, WARN, INFO, DEBUG

running = True
my_logger = Logger()

def signal_handler(signal, frame):
    global running
    running = False
    my_logger.log(DEBUG, 'Ending signal handled, ending the script...')
    
def main():
    my_logger.log(INFO, '--------------------')

    # Check python3 is used
    utils.check_python_version()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', '-c', dest='config_path')
    args = parser.parse_args()

    # Open conf and load parameters
    config, config_path = utils.open_and_load_config(args)
    my_logger.level_used = config.get(utils.SECTION_DEFAULT_NAME, utils.LOG_LEVEL)
    api_url = config.get(utils.SECTION_DEFAULT_NAME, utils.API_URL_NAME)
    id_server = config.get(utils.SECTION_DEFAULT_NAME, utils.ID_SERVER_NAME)
    polling_interval = config.get(utils.SECTION_DEFAULT_NAME, utils.POLLING_INTERVAL_NAME)
    zones_desired = set()
    for zone in set(config.items(utils.SECTION_ZONES_NAME)):
        zones_desired.add(zone[1])

    last_status = False
    my_logger.log(INFO, 'Calling kimsufi API on "{}"'.format(api_url))
    while running:
        server_found = False
        try:
            response = http1.get(api_url)
            if response.status == 200:
                struct = json.loads(response.body)
                for item in struct['answer']['availability']:
                    zones = [z['zone'] for z in item['zones'] if z['availability'] not in ('unavailable', 'unknown')]
                    if set(zones).intersection(zones_desired) and item['reference'] == id_server:
                        server_found = True
                        if not last_status:
                            my_logger.log(INFO, 'Found available server, sending notifications...')
                            notifications.send_notifications(config)
                            last_status = True
                        else:
                            my_logger.log(DEBUG, 'Notification already sent, passing...')
                    if not server_found:
                        my_logger.log(DEBUG, 'No server available')
                        if last_status:
                            my_logger.log(DEBUG, 'Server not available anymore')
                            # TODO: send notifications ?
                            last_status = False
            else:
                my_logger.log(ERROR, 'Calling API: "{}" "{}"'.format(response.status, response.message))
            # If signal occurs during process, there is no need to sleep
            if running:
                time.sleep(float(polling_interval))
        except Exception as e:
            my_logger.log(ERROR, 'Calling API: {}'.format(str(e)))
    
    my_logger.log(INFO, 'kimsufi script ended.')

if __name__ == '__main__':
    main()
