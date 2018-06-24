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

DEFAULT_CONFIG_PATH = '../config/kimsufi.conf'
SECTION_DEFAULT_NAME = 'GENERAL'
API_URL_NAME = 'API_URL'
SECTION_ZONES_NAME = 'ZONES'
ID_SERVER_NAME = 'ID_SERVER'
POLLING_INTERVAL_NAME = 'POLLING_INTERVAL'
SECTION_HTTP_REQUEST_NAME = 'HTTP_REQUEST'
HTTP_REQUEST = 'REQUEST'
SECTION_EMAIL_NAME = 'EMAIL'
SECTION_TELEGRAM_NAME = 'TELEGRAM'
TELEGRAM_TOKEN_NAME = 'TOKEN'
TELEGRAM_CHATID_NAME = 'CHATID'

def open_and_load_config(args):
	if args.config_path:
		config_path = args.config_path
	else:
		config_path = DEFAULT_CONFIG_PATH
	config = configparser.SafeConfigParser()
	
	if os.path.isfile(config_path):
		try:
			config.read(config_path)
		except configparser.ParsingError as e:
			log(ERROR, 'Parsing error: {}'.format(str(e)))
			sys.exit(1)
	else:
		log(ERROR, 'Config file "{}" not found."'.format(configPath))
		sys.exit(1)

	check_config(config)

	return config, config_path

def check_config(config):
	# Check at least a section of notification exists
	if (not is_config_section(config, SECTION_HTTP_REQUEST_NAME) 
		and not is_config_section(config, SECTION_EMAIL_NAME) 
		and not is_config_section(config, SECTION_TELEGRAM_NAME)):
		log(WARN, 'No section of notification found in the config file, just logs will be done.')
	# Check the mandatories keys and sections
	check_config_section(config, SECTION_ZONES_NAME)
	check_config_key(config, SECTION_DEFAULT_NAME, API_URL_NAME)
	check_config_key(config, SECTION_DEFAULT_NAME, ID_SERVER_NAME)

def is_config_section(config, section):
	if config.has_section(section):
		return True
	else:
		return False

def is_config_key(config, section, key):
	if config.has_option(section, key):
		return True
	else:
		return False

def check_config_section(config, section):
	if not is_config_section(config, section):
		log(ERROR, 'No section "{}" in config file'.format(section))
		sys.exit(1)

def check_config_key(config, section, key):
	if not is_config_key(config, section, key):
		log(ERROR, 'No key "{}" in section "{}" in config file'.format(key, section))
		sys.exit(1)
