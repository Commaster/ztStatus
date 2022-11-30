from random import choice
from requests import Session, Response

class ztAPI:
	def __init__(self, token:'str'):
		self.net = Session()
		self.net.headers.update({
			'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
			'Authorization': 'token ' + token
		})

	def listNetworks(self):
		response:'Response' = self.net.get('https://api.zerotier.com/api/v1/network', timeout=60)
		return {network["config"]["id"]: network["config"]["name"] for network in response.json()}

	def networkInfo(self, networkId:'str'):
		response:'Response' = self.net.get('https://api.zerotier.com/api/v1/network/' + networkId, timeout=60)
		return response.json()

	def _formatNetworkMember(self, data:'dict'):
		offlineForSeconds = (data['clock'] - data['lastOnline']) / 1000
		offlineTime = ''
		if offlineForSeconds < 120:
			offlineTime = ''
		else:
			rest, seconds = divmod(int(offlineForSeconds), 60)
			rest, minutes = divmod(rest, 60)
			days, hours = divmod(rest, 24)
			offlineTime = (str(days) + ' ' if days else '') + f'{hours:02d}:{minutes:02d}:{seconds:02d} ago'
		return {
			'name': data['name'],
			'description': data['description'],
			'lastOnline': offlineTime,
			'IP': data['physicalAddress'],
			'zIP': choice(data['config']['ipAssignments']) if data['config']['ipAssignments'] else None
		}

	def listNetworkMembers(self, networkId:'str'):
		response:'Response' = self.net.get('https://api.zerotier.com/api/v1/network/' + networkId + '/member', timeout=60)
		return {memberInfo['nodeId']: self._formatNetworkMember(memberInfo) for memberInfo in response.json()}

	def getNetworkMember(self, networkId:'str', memberId:'str'):
		response:'Response' = self.net.get('https://api.zerotier.com/api/v1/network/' + networkId + '/member/' + memberId, timeout=60)
		memberInfo = response.json()
		return {memberInfo['nodeId']: self._formatNetworkMember(memberInfo)}