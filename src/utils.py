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

from sys import version_info
from logger import Logger, FATAL, ERROR, WARN, INFO, DEBUG

DEFAULT_CONFIG_PATH = '../config/kimsufi.conf'
SECTION_DEFAULT_NAME = 'GENERAL'
API_URL_NAME = 'API_URL'
SECTION_ZONES_NAME = 'ZONES'
ID_SERVER_NAME = 'ID_SERVER'
POLLING_INTERVAL_NAME = 'POLLING_INTERVAL'
LOG_LEVEL_NAME = 'LOG_LEVEL'
SECTION_HTTP_REQUEST_NAME = 'HTTP_REQUEST'
HTTP_REQUEST_FOUND_NAME = 'REQUEST_FOUND'
HTTP_REQUEST_NOT_FOUND_NAME = 'REQUEST_NOT_FOUND'
SECTION_EMAIL_NAME = 'EMAIL'
EMAIL_SMTP_SERVER_NAME = 'SMTP_SERVER'
EMAIL_SMTP_PORT_NAME = 'SMTP_PORT'
EMAIL_SMTP_FROM_NAME = 'SMTP_FROM'
EMAIL_SMTP_PASSWORD_NAME = 'SMTP_PASSWORD'
EMAIL_SMTP_TO_NAME = 'SMTP_TO'
SECTION_TELEGRAM_NAME = 'TELEGRAM'
TELEGRAM_TOKEN_NAME = 'TOKEN'
TELEGRAM_CHATID_NAME = 'CHATID'

my_logger = Logger()

def open_and_load_config(args):
    if args.config_path:
        config_path = args.config_path
    else:
        config_path = DEFAULT_CONFIG_PATH
    config = configparser.ConfigParser()

    if os.path.isfile(config_path):
        try:
            config.read(config_path)
        except configparser.ParsingError as e:
            my_logger.log(FATAL, 'Parsing error: {}'.format(str(e)))
    else:
        my_logger.log(FATAL, 'Config file "{}" not found."'.format(configPath))

    check_config(config)

    return config, config_path

def check_config(config):
    # Check at least a section of notification exists
    if (not is_config_section(config, SECTION_HTTP_REQUEST_NAME)
            and not is_config_section(config, SECTION_EMAIL_NAME)
            and not is_config_section(config, SECTION_TELEGRAM_NAME)):
        my_logger.log(WARN, 'No section of notification found in the config file, just logs will be done.')
    
    # Check the mandatories keys and sections
    check_config_section(config, SECTION_ZONES_NAME)
    check_config_key(config, SECTION_DEFAULT_NAME, API_URL_NAME)
    check_config_key(config, SECTION_DEFAULT_NAME, ID_SERVER_NAME)
    check_config_key(config, SECTION_DEFAULT_NAME, POLLING_INTERVAL_NAME)
    check_config_key(config, SECTION_DEFAULT_NAME, LOG_LEVEL_NAME)

    # Check notifications sections
    if is_config_section(config, SECTION_HTTP_REQUEST_NAME):
        check_config_key(config, SECTION_HTTP_REQUEST_NAME, HTTP_REQUEST_FOUND_NAME)
        check_config_key(config, SECTION_HTTP_REQUEST_NAME, HTTP_REQUEST_NOT_FOUND_NAME)
    if is_config_section(config, SECTION_EMAIL_NAME):
        check_config_key(config, SECTION_EMAIL_NAME, EMAIL_SMTP_SERVER_NAME)
        check_config_key(config, SECTION_EMAIL_NAME, EMAIL_SMTP_PORT_NAME)
        check_config_key(config, SECTION_EMAIL_NAME, EMAIL_SMTP_FROM_NAME)
        check_config_key(config, SECTION_EMAIL_NAME, EMAIL_SMTP_PASSWORD_NAME)
        check_config_key(config, SECTION_EMAIL_NAME, EMAIL_SMTP_TO_NAME)
    if is_config_section(config, SECTION_TELEGRAM_NAME):
        check_config_key(config, SECTION_TELEGRAM_NAME, TELEGRAM_TOKEN_NAME)
        check_config_key(config, SECTION_TELEGRAM_NAME, TELEGRAM_CHATID_NAME)

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
        my_logger.log(FATAL, 'No section "{}" in config file'.format(section))

def check_config_key(config, section, key):
    if not is_config_key(config, section, key):
        my_logger.log(FATAL, 'No key "{}" in section "{}" in config file'.format(key, section))

def check_python_version():
    if version_info <= (3, 7):
        my_logger.log(FATAL, 'The script needs at least python 3.7')
