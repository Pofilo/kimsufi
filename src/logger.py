'''
logger.py: implementation of a simple logger.

kimsufi: Sends an alert when your kimsufi is available.
Copyright (C) 2018 pofilo <git@pofilo.fr>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

'''


import sys

from datetime import datetime

# LEVELS
FATAL = 'FATAL'
ERROR = 'ERROR'
WARN = 'WARN'
INFO = 'INFO'
DEBUG = 'DEBUG'

# Dictionary
weights = {DEBUG: 1, INFO: 2, WARN: 3, ERROR: 4, FATAL: 5}

class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		#else:
		#	cls._instances[cls].__init__(*args, **kwargs)
		return cls._instances[cls]

class Logger(metaclass=Singleton):

	def __init__(self):
		self._level_used = INFO

	@property
	def level_used(self): 
		return self._level_used

	@level_used.setter
	def level_used(self, value): 
		if value not in weights:
			self.log(FATAL, 'Bad level logging used: "{}"'.format(value))
		self._level_used = value

	def log(self, level, message):
		message = '{} ({}): {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), level, message)
		
		if level is FATAL:
			sys.exit(message)
		
		if weights[level] >= weights[self.level_used]:
			print(message)

