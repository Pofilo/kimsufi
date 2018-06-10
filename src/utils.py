'''
utils.py: kimsufi's utilities.

kimsufi: Sends an alert when your kimsufi is available.
Copyright (C) 2018 pofilo <git@pofilo.fr>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

'''

import configparser
import os.path
import sys

from logger import log, ERROR, WARN, INFO, DEBUG

defaultConfigPath = '../config/kimsufi.conf'
sectionDefault = 'DEFAULT'
apiUrlName = 'API_URL'
idServerName = 'ID_SERVER'
sectionSMSName = 'SMS'
sectionEmailName = 'EMAIL'
sectionTelegramName = 'TELEGRAM'

def openAndLoadConfig(args):
	if args.configPath:
		configPath = args.configPath
	else:
		configPath = defaultConfigPath
	config = configparser.SafeConfigParser()
	
	if os.path.isfile(configPath):
		try:
			config.read(configPath)
		except configparser.ParsingError as e:
			log(ERROR, 'Parsing error: {}'.format(str(e)))
			sys.exit(1)
	else:
		log(ERROR, 'Config file "{}" not found."'.format(configPath))
		sys.exit(1)

	checkConfig(config)

	return config, configPath

def checkConfig(config):
	# Check at least a section of notification exists
	if (not isConfigSection(config, sectionSMSName) 
		and not isConfigSection(config, sectionEmailName) 
		and not isConfigSection(config, sectionTelegramName)):
		log(ERROR, 'No section of notification found in the config file')
		sys.exit(1)
	# Check the mandatories fields
	checkConfigKey(config, sectionDefault, apiUrlName)
	checkConfigKey(config, sectionDefault, idServerName)

def isConfigSection(config, section):
	if config.has_section(section):
		return True
	else:
		return False

def isConfigKey(config, section, key):
	if config.has_option(section, key):
		return True
	else:
		return False

def checkConfigKey(config, section, key):
	if not isConfigKey(config, section, key):
		log(ERROR, 'No key "{}" in section "{}" in config file'.format(key, section))
		sys.exit(1)
