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
import requests
import argparse

import utils
from logger import log, ERROR, WARN, INFO, DEBUG

def main():
	log(INFO, '--------------------')

	# Parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--conf', '-c', dest='configPath')
	args = parser.parse_args()

	# Open conf and load parameters
	config, configPath = utils.openAndLoadConfig(args)
	apiUrl = config.get(utils.sectionDefaultName, utils.apiUrlName)
	idServer = config.get(utils.sectionDefaultName, utils.idServerName)
	zonesDesired = set()
	for zone in set(config.items(utils.sectionZonesName)):
		zonesDesired.add(zone[1])

	log(INFO, 'Calling kimsufi API...')
	try:
		response = http1.get(apiUrl)
		if response.status == 200:
			struct = json.loads(response.body)
			for item in struct['answer']['availability']:
				zones = [z['zone'] for z in item['zones'] if z['availability'] not in ('unavailable', 'unknown')]
				if set(zones).intersection(zonesDesired) and item['reference'] == idServer:
					log(INFO, 'Found available server, sending sms...')
					r = requests.get("PUT YOUR FREE URL HERE")
		else:
			log(ERROR, 'Calling API: "{}" "{}"'.format(response.status, response.message))
	except Exception as e:
		log(ERROR, 'Calling API: {}'.format(str(e)))

if __name__ == '__main__':
	main()
