#!/usr/bin/env python3
from source.modules._generic_module import *

class Module(GenericModule):
	def __init__(self):
		self.authors = [
			Author(name='Vitezslav Grygar', email='vitezslav.grygar@gmail.com', web='https://badsulog.blogspot.com'),
		]
		
		self.name = 'crypto.rot'
		self.short_description = 'Performs ROT substitution enciphering.'
		self.references = [
		#	'',
		]
		
		self.date = '2016-01-27'
		self.license = 'GNU GPLv2'
		self.version = '1.0'
		self.tags = [
			'cipher',
			'ROT', 'rot',
			'Caesar', 'Caesar\'s'
		]
		self.description = """

"""
		self.kb_access = [
			'DATA',
		]
		
		self.dependencies = {
		}
		self.changelog = """
"""

		self.reset_parameters()

	def reset_parameters(self):
		self.parameters = {
			'SILENT': Parameter(value='no', mandatory=True, description='Suppress the output'),
			'KEY': Parameter(value='', mandatory=True, description='Knowledge Base Data Key '),
			'ROT': Parameter(value='', mandatory=False, description='Specific ROT (empty = all from 0 to 26)'),
		}

	def check(self):
		silent = positive(self.parameters['SILENT'].value)
		if not silent:
			log.info('This module does not support check.')
		return False
	
	def run(self):
		silent = positive(self.parameters['SILENT'].value)
		# # # # # # # #
		uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		lowercase = 'abcdefghijklmnopqrstuvwxyz'
		
		# check key existence ( DATA > <key> > RAW)
		key = self.parameters['KEY'].value
		if not lib.kb.exists('DATA %s' % key):
			log.err('Key \'DATA %s\' does not exist in the Knowledge Base.' % key)
			return None

		
		# deal with message/messages
		data = {}
		datakey = lib.kb.find('DATA %s' % key)
		if type(datakey) is dict:
			for x in datakey:
				data['%s ' % (key) + x] = datakey[x]
		elif type(datakey) is list or type(datakey) is tuple:
			for i in range(len(datakey)):
				data['%s%d' % (key, i)] = datakey[i]
		elif type(datakey) is bytes:
			data[key] = datakey.decode('utf-8')
		elif type(datakey) is str:
			data[key] = datakey
		else:
			log.err('Unexpected message type %s, exiting...' % type(datakey))
			return None

		# prepare list of desired ROTS
		if self.parameters['ROT'].value == '':
			rots = list(range(1, 26))
		elif self.parameters['ROT'].value.isdigit():
			rots = []
			rots.append(int(self.parameters['ROT'].value))
		else:
			log.err('ROT value (%s) is weird.' % self.parameters['ROT'].value)
			return None

		for key in data:	
			message = data[key]
			# build result for each rot
			for i in rots:
				result = []
				for c in message:
					if c in uppercase:
						result.append(uppercase[(uppercase.index(c) + i) % len(uppercase)])
					elif c in lowercase:
						result.append(lowercase[(lowercase.index(c) + i) % len(lowercase)])
					else:
						result.append(c)
				
				if not silent:
					log.ok('ROT%d:' % i)
					for line in ''.join(result).splitlines():
						log.writeline(line)
					log.writeline()
				lib.kb.add('DATA %s-ROT%d' % (key, i), ''.join(result))
		# # # # # # # #
		return None
	

lib.module_objects.append(Module())
