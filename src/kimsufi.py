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
import telegram
import signal

import utils
from logger import log, ERROR, WARN, INFO, DEBUG

running = True

def signalHandler(signal, frame):
	global running
	running = False
	log(DEBUG, 'Ending signal handled, ending the script...')

def main():
	log(INFO, '--------------------')

	signal.signal(signal.SIGINT, signalHandler)
	signal.signal(signal.SIGTERM, signalHandler)

	# Parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--conf', '-c', dest='configPath')
	args = parser.parse_args()

	# Open conf and load parameters
	config, configPath = utils.openAndLoadConfig(args)
	apiUrl = config.get(utils.sectionDefaultName, utils.apiUrlName)
	idServer = config.get(utils.sectionDefaultName, utils.idServerName)
	pollingInterval = config.get(utils.sectionDefaultName, utils.pollingIntervalName)
	zonesDesired = set()
	for zone in set(config.items(utils.sectionZonesName)):
		zonesDesired.add(zone[1])

	lastStatus = False
	log(INFO, 'Calling kimsufi API on "{}"'.format(apiUrl))
	while running:
		serverFound = False
		try:
			response = http1.get(apiUrl)
			if response.status == 200:
				struct = json.loads(response.body)
				for item in struct['answer']['availability']:
					zones = [z['zone'] for z in item['zones'] if z['availability'] not in ('unavailable', 'unknown')]
					if set(zones).intersection(zonesDesired) and item['reference'] == idServer:
						serverFound = True
						if not lastStatus:
							log(INFO, 'Found available server, sending notifications...')
							if utils.isConfigSection(config, utils.sectionHTTPRequestName):
								log(DEBUG, 'Sending HTTP request')
								request = config.get(utils.sectionHTTPRequestName, utils.HTTPRequest)
								notifResponse = http1.get(request)
								if notifResponse.status is not 200:
									log(ERROR, 'Error calling HTTP request: "{}"'.format(request))
							if utils.isConfigSection(config, utils.sectionEmailName):
								log(WARN, 'Email is not implemented yet')
								# TODO
							if utils.isConfigSection(config, utils.sectionTelegramName):
								log(DEBUG, 'Sending Telegram message')
								token = config.get(utils.sectionTelegramName, utils.telegramTokenName)
								chatID = config.get(utils.sectionTelegramName, utils.telegramChatIDName)
								bot = telegram.Bot(token)
								bot.sendMessage(chatID, 'Hurry up, your kimsufi server is available!!')
							lastStatus = True
						else:
							log(DEBUG, 'Notification already sent, passing...')
					if not serverFound:
						log(DEBUG, 'No server available')
						if lastStatus:
							log(DEBUG, 'Server not available anymore')
							# TODO: send notifications ?
							lastStatus = False
			else:
				log(ERROR, 'Calling API: "{}" "{}"'.format(response.status, response.message))
					# If signal occurs during process, there is no need to sleep
			if running:
				time.sleep(float(pollingInterval))
		except Exception as e:
			log(ERROR, 'Calling API: {}'.format(str(e)))
	
	log(INFO, 'kimsufi script ended.')

if __name__ == '__main__':
	main()
