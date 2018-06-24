'''
notifications.py: methods to send notifications by various ways.

kimsufi: Sends an alert when your kimsufi is available.
Copyright (C) 2018 pofilo <git@pofilo.fr>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

'''

import http1
import telegram

import utils
from logger import log, ERROR, WARN, INFO, DEBUG

def send_notifications(config):
	send_http_notification(config)
	send_email_notification(config)
	send_telegram_notification(config)
	
def send_http_notification(config):
	if utils.is_config_section(config, utils.SECTION_HTTP_REQUEST_NAME):
		log(DEBUG, 'Sending HTTP request')
		request = config.get(utils.SECTION_HTTP_REQUEST_NAME, utils.HTTP_REQUEST)
		notif_response = http1.get(request)
		if notif_response.status is not 200:
			log(ERROR, 'Error calling HTTP request: "{}"'.format(request))

def send_email_notification(config):
	if utils.is_config_section(config, utils.SECTION_EMAIL_NAME):
		log(WARN, 'Email is not implemented yet')
		# TODO

def send_telegram_notification(config):
	if utils.is_config_section(config, utils.SECTION_TELEGRAM_NAME):
		log(DEBUG, 'Sending Telegram message')
		token = config.get(utils.SECTION_TELEGRAM_NAME, utils.TELEGRAM_TOKEN_NAME)
		chatID = config.get(utils.SECTION_TELEGRAM_NAME, utils.TELEGRAM_CHATID_NAME)
		bot = telegram.Bot(token)
		bot.send_message(chatID, 'Hurry up, your kimsufi server is available!!')
