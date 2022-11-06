import json
from pathlib import Path

class ztConfig(object):
	"""
	Configuration
	"""
	def __init__(self):
		"""
		Set up config
		"""
		self.data = {
			'token': '',
			'networkId': ''
		}
		self.file = 'config.json'
		self.load()

	def load(self):
		"""
		"""
		if Path(self.file).is_file():
			with open(self.file) as configfile:
				newdata:dict = json.load(configfile)
				self.data.update(newdata)
				if newdata != self.data:
					self.store()
		else:
			self.store()

	def store(self):
		"""
		"""
		with open(self.file, 'w') as configfile:
			json.dump(self.data, configfile, indent='\t')

	@property
	def token(self):
		return self.data['token']

	@property
	def networkId(self):
		return self.data['networkId']
