'''
notifications.py: methods to send notifications by various ways.

kimsufi: Sends an alert when your kimsufi is available.
Copyright (C) 2018 pofilo <git@pofilo.fr>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

'''

import http1
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import telegram

import utils
from logger import Logger, FATAL, ERROR, WARN, INFO, DEBUG

my_logger = Logger()

def send_notifications(config, found):
    send_http_notification(config, found)
    send_email_notification(config, found)
    send_telegram_notification(config, found)

def send_http_notification(config, found):
    if utils.is_config_section(config, utils.SECTION_HTTP_REQUEST_NAME):
        my_logger.log(DEBUG, 'Sending HTTP request')
        request = config.get(utils.SECTION_HTTP_REQUEST_NAME, utils.HTTP_REQUEST_FOUND_NAME)
        if not found:
            request = config.get(utils.SECTION_HTTP_REQUEST_NAME, utils.HTTP_REQUEST_NOT_FOUND_NAME)
        notif_response = http1.get(request)
        if notif_response.status is not 200:
            my_logger.log(ERROR, 'Error calling HTTP request: "{}"'.format(request))

def send_email_notification(config, found):
    if utils.is_config_section(config, utils.SECTION_EMAIL_NAME):
        my_logger.log(DEBUG, 'Sending Email')
        subject = 'Hurry up, your kimsufi server is available!!'
        if not found:
            subject = 'Too late, your kimsufi is not available anymore..'
        try:
            smtp_server = config.get(utils.SECTION_EMAIL_NAME, utils.EMAIL_SMTP_SERVER_NAME)
            smtp_port = config.get(utils.SECTION_EMAIL_NAME, utils.EMAIL_SMTP_PORT_NAME)
            smtp_from = config.get(utils.SECTION_EMAIL_NAME, utils.EMAIL_SMTP_FROM_NAME)
            smtp_password = config.get(utils.SECTION_EMAIL_NAME, utils.EMAIL_SMTP_PASSWORD_NAME)
            smtp_to = config.get(utils.SECTION_EMAIL_NAME, utils.EMAIL_SMTP_TO_NAME)
            msg = MIMEMultipart()
            msg['From'] = smtp_from
            msg['To'] = utils.EMAIL_SMTP_TO_NAME
            msg['Subject'] = subject 
            msg.attach(MIMEText('EN: https://www.kimsufi.com/en/servers.xml\nFR: https://www.kimsufi.com/fr/serveurs.xml'))
            mailserver = smtplib.SMTP_SSL(smtp_server, smtp_port)
            mailserver.ehlo()
            mailserver.login(smtp_from, smtp_password)
            mailserver.sendmail(smtp_from, smtp_from, msg.as_string())
            mailserver.quit()
        except Exception as e:
            my_logger.log(ERROR, 'Sending email failed: {}'.format(str(e)))

def send_telegram_notification(config, found):
    if utils.is_config_section(config, utils.SECTION_TELEGRAM_NAME):
        my_logger.log(DEBUG, 'Sending Telegram message')
        token = config.get(utils.SECTION_TELEGRAM_NAME, utils.TELEGRAM_TOKEN_NAME)
        chatID = config.get(utils.SECTION_TELEGRAM_NAME, utils.TELEGRAM_CHATID_NAME)
        bot = telegram.Bot(token)
        message = 'Hurry up, your kimsufi server is available!!'
        if not found:
            message = 'Too late, your kimsufi is not available anymore..'
        bot.send_message(chatID, message)